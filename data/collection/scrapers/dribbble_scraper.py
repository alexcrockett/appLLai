"""
Dribbble Jobs Scraper
Scrapes job listings from dribbble.com/jobs
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import time


class DribbbleScraper:
    def __init__(self):
        self.base_url = "https://dribbble.com/jobs"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_jobs(self, max_pages: int = 1) -> List[Dict]:
        """
        Scrape job listings from Dribbble
        
        Args:
            max_pages: Number of pages to scrape (default: 1)
        
        Returns:
            List of job dictionaries
        """
        all_jobs = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}?page={page}" if page > 1 else self.base_url
            print(f"Scraping page {page}: {url}")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                jobs = self._parse_page(response.text, url)
                all_jobs.extend(jobs)
                
                print(f"  Found {len(jobs)} jobs on page {page}")
                
                # Be polite - don't hammer the server
                if page < max_pages:
                    time.sleep(2)
                    
            except requests.RequestException as e:
                print(f"  Error fetching page {page}: {e}")
                break
        
        return all_jobs
    
    def _parse_page(self, html: str, source_url: str) -> List[Dict]:
        """Parse job listings from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        # Looking for job listing structure
        # Based on the fetched content, jobs appear to be in a list format
        # Each job has: company, title, location, and a view job link
        
        # This is a first-pass parser - may need adjustment based on actual HTML structure
        job_elements = soup.find_all('li')  # Job listings appear to be in <li> elements
        
        for job_elem in job_elements:
            try:
                # Extract company name
                company_elem = job_elem.find('img')
                company = company_elem.get('alt', 'Unknown') if company_elem else 'Unknown'
                
                # Extract job title (looking for h4 or similar heading)
                title_elem = job_elem.find(['h4', 'h3', 'h2'])
                if not title_elem:
                    continue  # Skip if no title found
                title = title_elem.get_text(strip=True)
                
                # Extract location
                # Location often appears as plain text after title
                location_text = job_elem.get_text(strip=True)
                location = 'Remote' if 'Remote' in location_text else 'Unknown'
                
                # Extract job URL
                link_elem = job_elem.find('a', href=True)
                job_url = None
                if link_elem and '/jobs/' in link_elem['href']:
                    job_url = f"https://dribbble.com{link_elem['href']}"
                
                # Skip if we couldn't extract essential info
                if not job_url:
                    continue
                
                # Extract posted time
                posted_time = 'Unknown'
                posted_elem = job_elem.find(string=lambda t: 'Posted' in str(t) or 'ago' in str(t))
                if posted_elem:
                    posted_time = posted_elem.strip()
                
                # Check if featured
                is_featured = 'Featured' in job_elem.get_text()
                
                job = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'url': job_url,
                    'posted': posted_time,
                    'featured': is_featured,
                    'source': 'Dribbble',
                    'source_url': source_url,
                    'scraped_at': datetime.now().isoformat()
                }
                
                jobs.append(job)
                
            except Exception as e:
                # Skip jobs we can't parse properly
                print(f"    Warning: Could not parse job element: {e}")
                continue
        
        return jobs
    
    def save_to_json(self, jobs: List[Dict], filename: str = None):
        """Save jobs to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # data/collection/scrapers/dribbble_scraper.py -> parents[2] is data/
            data_dir = Path(__file__).resolve().parents[2] / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            filename = str(data_dir / f"dribbble_jobs_{timestamp}.json")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved {len(jobs)} jobs to {filename}")
        return filename


def main():
    """Run the scraper"""
    scraper = DribbbleScraper()
    
    print("Starting Dribbble job scraper...")
    print("=" * 60)
    
    # Scrape first page
    jobs = scraper.scrape_jobs(max_pages=1)
    
    print("=" * 60)
    print(f"\nTotal jobs scraped: {len(jobs)}")
    
    # Display first few jobs
    if jobs:
        print("\nFirst 3 jobs:")
        print("-" * 60)
        for job in jobs[:3]:
            print(f"\nTitle: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Posted: {job['posted']}")
            print(f"URL: {job['url']}")
            print(f"Featured: {job['featured']}")
    
    # Save to JSON
    if jobs:
        scraper.save_to_json(jobs)
    else:
        print("\nNo jobs found. The page structure may have changed or be JavaScript-rendered.")
        print("Consider using Selenium/Playwright for JavaScript-heavy sites.")
    
    return jobs


if __name__ == "__main__":
    main()
