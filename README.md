# Job Search Aggregator (appLLai)

An intelligent job search tool that aggregates UX/design job listings and uses LLM to filter and present relevant opportunities.

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
```

2. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Running the Scrapers

### Dribbble Scraper
```bash
python scrapers/dribbble_scraper.py
```

This will:
- Scrape the first page of Dribbble jobs
- Display results in terminal
- Save to `data/dribbble_jobs_TIMESTAMP.json`

## Project Structure

```
appLLai/
├── scrapers/           # Web scrapers for different job boards
│   └── dribbble_scraper.py
├── data/              # Scraped job data (JSON files)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Next Steps

- [ ] Test Dribbble scraper
- [ ] Add Authentic Jobs scraper
- [ ] Add AIGA scraper
- [ ] Set up SQLite database
- [ ] Build Streamlit UI
- [ ] Integrate Claude API for job enrichment

## Notes

If the basic scraper doesn't work (JavaScript-rendered content), we'll need to use Selenium or Playwright.
