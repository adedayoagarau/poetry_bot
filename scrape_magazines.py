import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
import time

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more info
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('magazine_scraper.log'),
        logging.StreamHandler()
    ]
)

class MagazineScraper:
    def __init__(self):
        self.url = "https://www.newpages.com/magazines-c/literary/?_sft_genres=poetry"
        self.magazines = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
    def scrape_magazines(self):
        """Scrape poetry magazines from NewPages"""
        try:
            logging.info("Starting magazine scraping...")
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Print the entire HTML for inspection
            print("HTML Content:")
            print(soup.prettify())
            
            # Find all possible container elements
            containers = soup.find_all(['div', 'article', 'section'])
            logging.info(f"Found {len(containers)} potential containers")
            
            for container in containers:
                logging.debug(f"Container classes: {container.get('class', [])}")
                logging.debug(f"Container content:\n{container.prettify()[:500]}")
            
            # Try to find magazine entries with broader selectors
            magazine_entries = soup.find_all(['article', 'div', 'section'])
            logging.info(f"Found {len(magazine_entries)} potential magazine entries")
            
            for entry in magazine_entries:
                try:
                    # Look for any links that might contain magazine titles
                    links = entry.find_all('a')
                    for link in links:
                        href = link.get('href', '')
                        if 'magazine' in href.lower() or 'journal' in href.lower():
                            title = link.text.strip()
                            if title:
                                magazine_info = {
                                    'title': title,
                                    'url': href,
                                    'description': entry.text.strip(),
                                    'scraped_at': datetime.now().isoformat()
                                }
                                self.magazines.append(magazine_info)
                                logging.info(f"Found magazine: {title}")
                    
                except Exception as e:
                    logging.error(f"Error processing entry: {str(e)}")
                    continue
            
            logging.info(f"Successfully scraped {len(self.magazines)} magazines")
            self.save_results()
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
    
    def save_results(self):
        """Save scraped magazines to JSON file"""
        try:
            with open('poetry_magazines.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'magazines': self.magazines,
                    'total_count': len(self.magazines),
                    'scraped_at': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            logging.info("Saved results to poetry_magazines.json")
        except Exception as e:
            logging.error(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    scraper = MagazineScraper()
    scraper.scrape_magazines() 