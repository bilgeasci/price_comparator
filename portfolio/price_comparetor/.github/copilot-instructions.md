p# Price Comparator - AI Coding Agent Instructions

## Project Overview
A multi-interface price comparison tool for Turkish e-commerce sites (Hepsiburada, N11, Trendyol). Supports three interface modes: CLI, GUI (Tkinter), and REST API (FastAPI). The core comparison logic is abstracted into `comparator.py` to enable reuse across all interfaces.

## Architecture & Data Flow

### Component Structure
- **`src/main.py`**: Entry point; uses argparse for `--gui` flag to route between CLI and GUI modes
- **`src/comparator.py`**: Core business logic with two functions:
  - `compare_prices(price1, price2)`: Compares two prices and returns comparison result string
  - `compare_product_prices(product)`: Gets prices from all sites and returns list of tuples `[(site, price), ...]`
- **`src/scraper.py`**: Data retrieval layer; `fake_scrape(product)` returns hardcoded mock data dict
- **`src/gui.py`**: Tkinter-based GUI; calls `compare_product_prices()` and displays results in messagebox
- **`src/api.py`**: FastAPI server; `create_app()` factory returns app with `/compare` endpoint
- **`data/sample_site.json`**: E-commerce site URLs for reference (Hepsiburada, N11, Trendyol)

### Data Format
- Scraper returns dict: `{"site_name": price_as_int, ...}` 
- `compare_product_prices()` converts to list of tuples: `[(site, price), ...]`
- All prices are in Turkish Lira (TL)

## Key Patterns & Conventions

### Testing
- Run tests with: `pytest`
- Test file: `tests/test_comparator.py`
- Import paths are configured in `tests/conftest.py` to allow relative imports
- Currently tests only basic comparison logic (not scraping or UI)

### Turkish Language
- UI labels and error messages use Turkish (e.g., "Ürün adı:", "Fiyat Karşılaştırıcı")
- When adding features, maintain Turkish naming in user-facing strings

### Extensibility Points
- **Adding new e-commerce sites**: Update `data/sample_site.json` and modify `scraper.py` to parse each site
- **Adding new interfaces**: Create new module that imports `compare_prices()` from `comparator.py`
- **Enhancing comparator logic**: `compare_prices()` currently returns raw results; consider adding filtering/sorting without breaking API contracts

## Development Workflow

### Installation
```bash
pip install -r requirements.txt
```

### Running Price Comparator (CLI, GUI, API)
**Always run using `-m` flag to enable relative imports:**

**Option A: Using convenience scripts (from project root):**
```bash
# CLI mode
./run-cli.sh

# GUI mode (requires graphical environment)
./run-gui.sh

# FastAPI server (port 8000)
./run-api.sh
# Then: curl "http://localhost:8000/compare?product=laptop"
```

**Option B: Manual commands (from project root):**
```bash
# CLI mode
python -m src.main

# GUI mode
python -m src.main --gui

# API mode with factory pattern
uvicorn src.api:create_app --reload --factory
```

### Running Django Web App
```bash
# Navigate to Django project directory
cd webapp/webapp/comparator

# Start development server (port 8000)
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

Or use convenience script from project root:
```bash
./run-django.sh
```

### Testing
```bash
pytest
```

## Known Limitations & Future Work
- `scraper.py` returns hardcoded mock data; real web scraping not yet implemented
- `comparator.py` currently compares only two prices; doesn't aggregate or filter multiple site results
- No error handling for invalid/missing price data
- GUI lacks async support for long scraping operations
