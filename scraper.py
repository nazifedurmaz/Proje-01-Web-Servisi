"""
Gazete Hacettepe - Haber Toplayıcı (Scraper)
Bu modül, gazete.hacettepe.edu.tr sitesinden haberleri çeker.
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

BASE_URL = "https://gazete.hacettepe.edu.tr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; HacettepeNewsAPI/1.0)"
}


def get_news_list(page=1, limit=10):
    """
    Ana sayfadan haber listesini çeker.
    Her haberde: başlık, özet, link, görsel, tarih, yazar alanları bulunur.
    """
    url = f"{BASE_URL}/tr/haberler"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return {"error": str(e), "items": []}

    soup = BeautifulSoup(resp.text, "lxml")
    news_items = []

    # Haberleri ana sayfadan topla
    # Ana sayfadan link topla
    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/tr/haber/" in href and href not in links:
            full = href if href.startswith("http") else BASE_URL + href
            links.add(full)

    links = list(links)[(page - 1) * limit: page * limit]

    for link in links:
        item = get_news_detail(link)
        if item and not item.get("error"):
            news_items.append(item)

    return {
        "total": len(news_items),
        "page": page,
        "items": news_items
    }


def get_news_detail(url):
    """
    Tek bir haberin detaylarını çeker.
    Döndürdüğü alanlar:
      - title: Başlık
      - summary: Kısa özet (ilk paragraf)
      - author: Yazar/Kategori
      - date: Tarih
      - image_url: Görsel URL
      - url: Haberin tam linki
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return {"error": str(e), "url": url}

    soup = BeautifulSoup(resp.text, "lxml")

    # Başlık
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Kategori/Yazar (alt menü linkleri veya yazar bilgisi)
    author = ""
    # Haberin kategori linkini yazar olarak al (örn: "Yönetim", "Araştırma" vb.)
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        if "/tr/haberler/" in href:
            candidate = a.get_text(strip=True)
            if candidate and len(candidate) < 50 and candidate not in ["HABERLER", "ANA SAYFA"]:
                author = candidate
                break

    # Tarih - "Son Başlıklar" bölümünden en yakın tarihe bak
    # ya da sayfa içinde tarih formatı ara
    date_str = ""
    date_pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}")
    for text in soup.stripped_strings:
        m = date_pattern.search(text)
        if m:
            date_str = m.group()
            break

    # Görseller - sadece haber içeriğine ait olanlar
    image_url = ""
    # fs_/ veya uploads/ klasörlerinden gelen görselleri ara
    for img in soup.find_all("img", src=True):
        src = img["src"]
        if any(x in src for x in ["/fs_/", "/uploads/", "HABERLER"]):
            if src.startswith("http"):
                image_url = src
            else:
                image_url = BASE_URL + src
            break

    # Özet - ilk anlamlı paragraf
    summary = ""
    # İçerik paragraflarını bul (nav/header dışında)
    body = soup.find("body")
    if body:
        paragraphs = body.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            # En az 50 karakter, menü metni değil
            if len(text) > 50 and title[:20] not in text:
                summary = text[:300] + ("..." if len(text) > 300 else "")
                break

    # Eğer paragraf bulunamazsa h1 sonrası ilk metin bloğunu al
    if not summary and title:
        all_text = soup.get_text(separator="\n")
        lines = [l.strip() for l in all_text.splitlines() if l.strip()]
        for i, line in enumerate(lines):
            if title[:20] in line and i + 1 < len(lines):
                for j in range(i + 1, min(i + 10, len(lines))):
                    if len(lines[j]) > 50:
                        summary = lines[j][:300] + ("..." if len(lines[j]) > 300 else "")
                        break
                break

    return {
        "title": title,
        "summary": summary,
        "author": author if author else "Gazete Hacettepe",
        "date": date_str,
        "image_url": image_url,
        "url": url
    }


def get_recent_news(limit=10):
    """Ana sayfadaki son haberleri daha hızlı çeker."""
    url = f"{BASE_URL}/tr"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return {"error": str(e), "items": []}

    soup = BeautifulSoup(resp.text, "lxml")
    news_items = []
    seen_links = set()

    # Başlık + özet + link kombinasyonlarını bul
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/tr/haber/" not in href:
            continue
        full_url = href if href.startswith("http") else BASE_URL + href
        if full_url in seen_links:
            continue
        seen_links.add(full_url)

        # Linkin etrafındaki başlık ve özeti al
        parent = a.find_parent()
        title = a.get_text(strip=True)
        summary = ""

        # Bir üst veya kardeş elementten özet bul
        if parent:
            sibling = a.find_next_sibling()
            if sibling:
                summary = sibling.get_text(strip=True)[:300]

        if title and len(title) > 10:
            news_items.append({
                "title": title,
                "summary": summary,
                "author": "Gazete Hacettepe",
                "date": "",
                "image_url": "",
                "url": full_url
            })

        if len(news_items) >= limit:
            break

    return {"total": len(news_items), "items": news_items}


if __name__ == "__main__":
    print("Test: Son haberler çekiliyor...")
    result = get_recent_news(5)
    for item in result["items"]:
        print(f"- {item['title'][:60]} -> {item['url']}")
