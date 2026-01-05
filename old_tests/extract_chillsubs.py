import requests
from bs4 import BeautifulSoup
import json
import time

def extract_chillsubs_magazines():
    """Extract literary magazines from Chill Subs website"""
    magazines = []
    base_url = "https://www.chillsubs.com/browse/magazines"
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
    
    # Try multiple pages
    for page in range(1, 11):  # Check first 10 pages
        url = f"{base_url}?page={page}&sortBy=az"
        print(f"Checking page {page}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to load page {page}: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for magazine cards/listings with various selectors
            magazine_elements = (
                soup.find_all('div', class_='magazine-card') or
                soup.find_all('div', class_='magazine') or
                soup.find_all('a', href=lambda x: x and '/magazine/' in str(x)) or
                soup.find_all('div', attrs={'data-magazine': True}) or
                soup.find_all('article') or
                soup.find_all('div', class_='card')
            )
            
            print(f"Found {len(magazine_elements)} elements on page {page}")
            
            if not magazine_elements:
                print(f"No magazines found on page {page}, stopping")
                break
            
            for element in magazine_elements:
                try:
                    # Extract magazine name
                    name_elem = (
                        element.find('h3') or 
                        element.find('h2') or 
                        element.find('a') or
                        element.find('div', class_='title') or
                        element.find('span', class_='name')
                    )
                    
                    if name_elem:
                        name = name_elem.get_text().strip()
                        
                        # Try to find website URL
                        website = None
                        link_elem = element.find('a', href=lambda x: x and ('http' in str(x) or 'www' in str(x)))
                        if link_elem:
                            website = link_elem.get('href')
                        
                        # Skip if we already have this magazine
                        if name and not any(mag['name'] == name for mag in magazines):
                            magazine_data = {
                                'name': name,
                                'url': website or f"https://www.google.com/search?q={name.replace(' ', '+')}+literary+magazine",
                                'selector': 'div.poem, .entry-content, article',
                                'has_online_poems': True,
                                'source': 'ChillSubs'
                            }
                            magazines.append(magazine_data)
                            print(f"Added: {name}")
                
                except Exception as e:
                    print(f"Error processing element: {e}")
                    continue
            
            # Be respectful with requests
            time.sleep(1)
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            continue
    
    return magazines

if __name__ == "__main__":
    print("Extracting literary magazines from Chill Subs...")
    magazines = extract_chillsubs_magazines()
    
    print(f"\nFound {len(magazines)} magazines total")
    
    # Save to JSON file
    with open('chillsubs_magazines.json', 'w') as f:
        json.dump(magazines, f, indent=2)
    
    # Print first 10 for preview
    print("\nFirst 10 magazines:")
    for i, mag in enumerate(magazines[:10]):
        print(f"{i+1}. {mag['name']} - {mag['url']}")
    
    print(f"\nSaved all magazines to chillsubs_magazines.json") 