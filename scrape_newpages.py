import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('magazine_scraper.log'),
        logging.StreamHandler()
    ]
)

class NewPagesScraper:
    BASE_URL = "https://www.newpages.com/magazines-c/literary/?_sft_genres=poetry"
    
    def __init__(self):
        self.magazines = []
        self.setup_driver()
        
    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def scrape_magazines(self):
        try:
            logging.info(f"Starting scrape of {self.BASE_URL}")
            self.driver.get(self.BASE_URL)
            
            # Wait for the content to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "post-title"))
            )
            
            # Let the page fully render
            time.sleep(5)
            
            # Get the page source after JavaScript has rendered
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find all magazine entries
            magazine_entries = soup.find_all("article", class_="post")
            
            for entry in magazine_entries:
                magazine_info = {}
                
                # Get title
                title_elem = entry.find("h2", class_="post-title")
                if title_elem and title_elem.find('a'):
                    magazine_info['title'] = title_elem.find('a').text.strip()
                    magazine_info['url'] = title_elem.find('a')['href']
                
                # Get description
                desc_elem = entry.find("div", class_="post-content")
                if desc_elem:
                    magazine_info['description'] = desc_elem.text.strip()
                
                if magazine_info:
                    self.magazines.append(magazine_info)
                    logging.info(f"Found magazine: {magazine_info['title']}")
            
            logging.info(f"Found {len(self.magazines)} magazines total")
            
            # Save to JSON file
            self.save_results()
            
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")
        finally:
            self.driver.quit()
    
    def save_results(self):
        output_file = 'poetry_magazines.json'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'magazines': self.magazines,
                    'scraped_at': datetime.now().isoformat(),
                    'total_count': len(self.magazines)
                }, f, indent=2, ensure_ascii=False)
            logging.info(f"Results saved to {output_file}")
        except Exception as e:
            logging.error(f"Error saving results: {str(e)}")

if __name__ == "__main__":
    scraper = NewPagesScraper()
    scraper.scrape_magazines() 