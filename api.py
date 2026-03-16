"""
Gazete Hacettepe Haber Web Servisi / API
========================================
Endpoints:
  GET /api/news           -> JSON haber listesi (tüm haberler)
  GET /api/news/<id>      -> JSON tek haber detayı
  GET /api/news.xml       -> XML haber listesi (Web Servisi)
  GET /api/news/<id>.xml  -> XML tek haber detayı
  GET /api/news?category=araştırma -> Kategoriye göre filtre
  GET /api/news?q=arama   -> Başlık/özette arama
  GET /                   -> API dökümantasyon arayüzü
"""

from flask import Flask, request, jsonify, Response, render_template_string
from flask_cors import CORS
from news_data import SAMPLE_NEWS
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)


# ─── Yardımcı Fonksiyonlar ───────────────────────────────────────────────────

def filter_news(category=None, query=None):
    items = SAMPLE_NEWS[:]
    if category:
        items = [n for n in items if category.lower() in n.get("category", "").lower()
                 or category.lower() in n.get("author", "").lower()]
    if query:
        q = query.lower()
        items = [n for n in items if q in n["title"].lower() or q in n["summary"].lower()]
    return items


def news_to_xml_element(news_item, parent=None):
    """Bir haber dict'ini XML elementine çevirir."""
    if parent is not None:
        item = ET.SubElement(parent, "haber")
    else:
        item = ET.Element("haber")

    ET.SubElement(item, "id").text = str(news_item.get("id", ""))
    ET.SubElement(item, "baslik").text = news_item.get("title", "")
    ET.SubElement(item, "ozet").text = news_item.get("summary", "")
    ET.SubElement(item, "yazar").text = news_item.get("author", "")
    ET.SubElement(item, "tarih").text = news_item.get("date", "")
    ET.SubElement(item, "gorsel_url").text = news_item.get("image_url", "")
    ET.SubElement(item, "haber_url").text = news_item.get("url", "")
    ET.SubElement(item, "kategori").text = news_item.get("category", "")
    return item


def pretty_xml(element):
    """XML'i güzel formatta döndürür."""
    rough = ET.tostring(element, encoding="unicode")
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode("utf-8")


# ─── JSON API Endpoints ───────────────────────────────────────────────────────

@app.route("/api/news", methods=["GET"])
def api_news_list():
    """
    Haber listesini JSON olarak döndürür.
    Query params:
      - category: Kategori filtresi (örn: arastirma, yonetim, spor)
      - q: Arama terimi
      - limit: Döndürülecek haber sayısı (default: 10)
      - page: Sayfa numarası (default: 1)
    """
    category = request.args.get("category")
    query = request.args.get("q")
    limit = int(request.args.get("limit", 10))
    page = int(request.args.get("page", 1))

    items = filter_news(category, query)
    total = len(items)
    start = (page - 1) * limit
    items = items[start: start + limit]

    return jsonify({
        "servis": "Gazete Hacettepe Haber API",
        "kaynak": "https://gazete.hacettepe.edu.tr",
        "toplam_haber": total,
        "sayfa": page,
        "limit": limit,
        "haberler": items
    })


@app.route("/api/news/<int:news_id>", methods=["GET"])
def api_news_detail(news_id):
    """Tek haberin JSON detayını döndürür."""
    item = next((n for n in SAMPLE_NEWS if n["id"] == news_id), None)
    if not item:
        return jsonify({"hata": "Haber bulunamadı", "id": news_id}), 404
    return jsonify(item)


# ─── XML Web Servisi Endpoints ────────────────────────────────────────────────

@app.route("/api/news.xml", methods=["GET"])
def api_news_xml():
    """
    Haber listesini XML Web Servisi formatında döndürür.
    XSD şemasına uygun yapı:
      <haberler>
        <haber>
          <id>, <baslik>, <ozet>, <yazar>, <tarih>,
          <gorsel_url>, <haber_url>, <kategori>
        </haber>
        ...
      </haberler>
    """
    category = request.args.get("category")
    query = request.args.get("q")
    limit = int(request.args.get("limit", 10))

    items = filter_news(category, query)[:limit]

    # XML kök elementi
    root = ET.Element("haberler")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "/api/schema.xsd")
    root.set("kaynak", "https://gazete.hacettepe.edu.tr")
    root.set("toplam", str(len(items)))
    root.set("tarih", datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

    for news_item in items:
        news_to_xml_element(news_item, root)

    xml_str = pretty_xml(root)
    return Response(xml_str, mimetype="application/xml; charset=utf-8")


@app.route("/api/news/<int:news_id>.xml", methods=["GET"])
def api_news_detail_xml(news_id):
    """Tek haberin XML detayını döndürür."""
    item = next((n for n in SAMPLE_NEWS if n["id"] == news_id), None)
    if not item:
        root = ET.Element("hata")
        ET.SubElement(root, "mesaj").text = "Haber bulunamadı"
        ET.SubElement(root, "id").text = str(news_id)
        return Response(pretty_xml(root), mimetype="application/xml"), 404

    element = news_to_xml_element(item)
    xml_str = pretty_xml(element)
    return Response(xml_str, mimetype="application/xml; charset=utf-8")


# ─── XSD Schema ──────────────────────────────────────────────────────────────

@app.route("/api/schema.xsd", methods=["GET"])
def api_schema():
    """XML Schema Definition (XSD) dosyasını döndürür."""
    xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <!-- Haber listesi root elementi -->
  <xs:element name="haberler">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="haber" type="HaberType"
                    minOccurs="0" maxOccurs="unbounded"/>
      </xs:sequence>
      <xs:attribute name="kaynak" type="xs:anyURI" use="optional"/>
      <xs:attribute name="toplam" type="xs:nonNegativeInteger" use="optional"/>
      <xs:attribute name="tarih" type="xs:dateTime" use="optional"/>
    </xs:complexType>
  </xs:element>

  <!-- Tek haber elementi (doğrudan da kullanılabilir) -->
  <xs:element name="haber" type="HaberType"/>

  <!-- Haber veri tipi -->
  <xs:complexType name="HaberType">
    <xs:sequence>
      <xs:element name="id" type="xs:positiveInteger"/>
      <xs:element name="baslik" type="xs:string"/>
      <xs:element name="ozet" type="xs:string"/>
      <xs:element name="yazar" type="xs:string"/>
      <xs:element name="tarih" type="xs:string"/>
      <xs:element name="gorsel_url" type="xs:anyURI"/>
      <xs:element name="haber_url" type="xs:anyURI"/>
      <xs:element name="kategori" type="KategoriType"/>
    </xs:sequence>
  </xs:complexType>

  <!-- Geçerli kategori değerleri -->
  <xs:simpleType name="KategoriType">
    <xs:restriction base="xs:string">
      <xs:enumeration value="arastirma"/>
      <xs:enumeration value="yonetim"/>
      <xs:enumeration value="ogrenci"/>
      <xs:enumeration value="spor"/>
      <xs:enumeration value="odul"/>
      <xs:enumeration value="uluslararasi"/>
      <xs:enumeration value="kultur"/>
      <xs:enumeration value="diger"/>
    </xs:restriction>
  </xs:simpleType>

</xs:schema>'''
    return Response(xsd, mimetype="application/xml; charset=utf-8")


# ─── Ana Sayfa ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(open("templates/index.html").read())


@app.route("/health")
def health():
    return jsonify({"durum": "aktif", "servis": "Gazete Hacettepe API", "versiyon": "1.0"})


if __name__ == "__main__":
    print("=" * 55)
    print("  Gazete Hacettepe Haber Web Servisi")
    print("=" * 55)
    print("  JSON API :  http://localhost:5000/api/news")
    print("  XML API  :  http://localhost:5000/api/news.xml")
    print("  XSD      :  http://localhost:5000/api/schema.xsd")
    print("  Arayüz   :  http://localhost:5000/")
    print("=" * 55)
    app.run(debug=True, port=5000)
