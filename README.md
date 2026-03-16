# Gazete Hacettepe — Haber Web Servisi

BBY464 Semantik Bilgi Yönetimi — XML ve Web Servisi Ödevi

## Kurulum

```bash
pip install -r requirements.txt
python api.py
```

Tarayıcıda açın: http://localhost:5000

## Endpoint'ler

| URL | Format | Açıklama |
|-----|--------|----------|
| `/api/news` | JSON | Tüm haber listesi |
| `/api/news.xml` | XML | XML Web Servisi |
| `/api/news/<id>` | JSON | Tek haber detayı |
| `/api/news/<id>.xml` | XML | Tek haber (XML) |
| `/api/schema.xsd` | XSD | XML Şema Tanımı |

## Query Parametreleri

- `?q=tubitak` — Başlık/özette arama
- `?category=arastirma` — Kategori filtresi
- `?limit=5` — Sonuç sayısı
- `?page=2` — Sayfalama

## Proje Yapısı

```
gazete_hacettepe_api/
├── api.py          # Flask REST API + XML Web Servisi
├── scraper.py      # Gerçek ortam scraper (BeautifulSoup4)
├── news_data.py    # Statik test verisi
├── requirements.txt
└── templates/
    └── index.html  # API dökümantasyon arayüzü
```
