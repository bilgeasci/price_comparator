"""
Scraper module: fetch HTML (via ScraperAPI if API key present) and parse site-specific.
"""

import os
import time
import logging
import requests
from urllib.parse import quote_plus
from .parser_trendyol import parse_trendyol
from .parser_hepsiburada import parse_hepsiburada
from .parser_amazon import parse_amazon
from dotenv import load_dotenv

# Bu satır, .env dosyanızı yükler
load_dotenv() 

logger = logging.getLogger(__name__)


SCRAPER_KEY = os.getenv("SCRAPER_API_KEY")  # from .env
print("--- KOD BAŞLANGICI BAŞARILI! ---") 
print(f"Anahtar Yüklendi mi? {bool(SCRAPER_KEY)}")

REQUEST_TIMEOUT =25
RETRIES = 2
BACKOFF = 0.5

DEMO = {
    "trendyol": 299.0,
    "hepsiburada": 449.0,
    "amazon": 399.0
}

def _fetch_via_scraperapi(url):
    if not SCRAPER_KEY:
        return None
    api = "http://api.scraperapi.com"
    params = {
        "api_key": SCRAPER_KEY,
        "url": url,
        "render": "true"  # render JS
    }
    try:
        r = requests.get(api, params=params, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.text
        logger.warning("ScraperAPI status %s for %s", r.status_code, url)
    except Exception as e:
        logger.warning("ScraperAPI fetch error %s", e)
    return None

# scraper.py dosyanızda _fetch_direct(url) fonksiyonunun güncel hali

def _fetch_direct(url):
    # Bu başlıkları kullanın
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Connection": "keep-alive"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.text
        logger.warning("Direct fetch status %s for %s", r.status_code, url)
    except Exception as e:
        logger.warning("Direct fetch error %s", e)
    return None

def _fetch(url):
    html = _fetch_via_scraperapi(url)
    if html:
        return html
    return _fetch_direct(url)

def _search_url_trendyol(product):
    return f"https://www.trendyol.com/sr?q={quote_plus(product)}"

def _search_url_hepsiburada(product):
    return f"https://www.hepsiburada.com/ara?q={quote_plus(product)}"

def _search_url_amazon(product):
    # Amazon search (locale-agnostic). For local may need region-specific
    return f"https://www.amazon.com.tr/s?k={quote_plus(product)}"

def scrape_site(site_key, product):
    url_map = {
        "trendyol": _search_url_trendyol,
        "hepsiburada": _search_url_hepsiburada,
        "amazon": _search_url_amazon
    }
    parser_map = {
        "trendyol": parse_trendyol,
        "hepsiburada": parse_hepsiburada,
        "amazon": parse_amazon
    }
    url = url_map[site_key](product)
    html = _fetch(url)
    note = "no-html"
    price = None
    raw = None
    if html:
        try:
            price, raw = parser_map[site_key](html)
            if price is not None:
                note = "scraped"
            else:
                note = "no-data"
        except Exception as e:
            logger.exception("parse error %s", e)
            note = "parse-error"
    else:
        note = "fetch-failed"

    # fallback demo value if scraping failed
    if price is None:
        price = DEMO.get(site_key)
        if price is not None:
            note = "fallback-demo"

    return {
        "site": site_key,
        "price": price,
        "raw": raw,
        "note": note,
        "source_url": url
    }

def scrape_all(product):
    product = (product or "").strip()
    if not product:
        raise ValueError("product cannot be empty")
    results = {}
    for s in ["trendyol", "hepsiburada", "amazon"]:
        results[s] = scrape_site(s, product)
        # tiny delay to be gentle
        time.sleep(0.3)
    return results



