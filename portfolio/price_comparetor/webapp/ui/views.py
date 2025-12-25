
from pathlib import Path
from django.shortcuts import render
import logging
import sys # sys.path manipülasyonu yapılmayacağı için sadece gerektiğinde kalsın
from pathlib import Path

# comparator klasörünün yolunu Python path'e ekle



logger = logging.getLogger(__name__)


def home(request):
    return render(request, "ui/compare.html")


def compare(request):
    from comparator import core
    product = request.GET.get("product", "").strip()

    results = []
    if product:
        try:
            # scrape_all fonksiyonunu tek bir yerden doğru şekilde çağırıyoruz
            raw = core.run_comparison(product)
            # normalize for template
            for site, data in raw.items():
                results.append({
                    "store": site.capitalize(),
                    "price": data.get("price"),
                    "url": data.get("source_url"),
                    "note": data.get("note")
                })
        except Exception as e:
            logger.exception("Scraper hata verdi: %s", e)

    return render(request, "ui/compare.html", {
        "product": product,
        "results": results
    })

if __name__ == "__main__":
    # Basit bir test için
    test_product = "örnek ürün"
    print(f"Testing run_comparison with product: {test_product}")
    try:
        from comparator import core
        test_results = core.run_comparison(test_product)
        for site, data in test_results.items():
            print(f"{site}: {data}")
    except Exception as e:
        logger.exception("Test çalıştırılırken hata oluştu: %s", e)