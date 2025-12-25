from bs4 import BeautifulSoup
import re

def parse_trendyol(html):
    if not html:
        return None, None
    soup = BeautifulSoup(html, "html.parser")
    # try common selectors
    selectors = [".prc-box-dscntd", ".ds-price", ".price-amount", "[data-test='product-price']"]
    for sel in selectors:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            raw = el.get_text(" ", strip=True)
            price = _to_float(raw)
            if price is not None:
                return price, raw
    # fallback search numbers + TL
    text = soup.get_text(" ", strip=True)
    m = re.search(r'([0-9\.,]{2,}\s*(?:TL|₺))', text, flags=re.I)
    if m:
        raw = m.group(1)
        return _to_float(raw), raw
    return None, None

def _to_float(s):
    if not s:
        return None
    s = s.lower().replace("tl", "").replace("₺", "").strip()
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except:
        return None