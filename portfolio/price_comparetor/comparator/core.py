import sys
import os 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import logging
logger = logging.getLogger(__name__)

def run_comparison(product: str) -> dict:
    """
    Kullanıcıdan gelen ürün sorgusunu alır ve scraping işlemini başlatır.
    Bu fonksiyon, views.py tarafından çağrılacaktır.
    """
    from .scraper import scrape_all
    logger.info("Karşılaştırma başlatılıyor: %s", product)
    
    # scrape_all fonksiyonunu çağır
    try:
        results = scrape_all(product)
        return results
    except Exception as e:
        logger.error("Scraping sırasında hata oluştu: %s", e)
        # Hata durumunda boş bir sözlük döndür
        return {}
