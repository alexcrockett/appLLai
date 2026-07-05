# Job Search Aggregator (appLLai)

An intelligent job search tool that aggregates UX/design job listings and uses LLM to filter and present relevant opportunities.

## Setup

This project uses [pixi](https://pixi.sh) to manage its environment and dependencies.

1. **Install dependencies:**
```bash
pixi install
```

## Running the Scrapers

### Dribbble Scraper
```bash
pixi run scrape
```

This will:
- Scrape the first page of Dribbble jobs
- Display results in terminal
- Save to `data/dribbble_jobs_TIMESTAMP.json`

## Project Structure

```
appLLai/
├── data/
│   ├── collection/scrapers/   # Web scrapers for different job boards
│   │   └── dribbble_scraper.py
│   └── data/                 # Scraped job data (JSON files)
├── pixi.toml                 # Pixi project & dependencies
└── README.md                 # This file
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
