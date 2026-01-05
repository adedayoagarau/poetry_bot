import requests
from bs4 import BeautifulSoup

def debug_poetry_daily():
    """Debug Poetry Daily page structure"""
    url = 'https://poems.com/todays-poem/'
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
    response = requests.get(url, headers=headers, timeout=10)
    
    print(f"Status: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    print(f"Title: {soup.title.text if soup.title else 'No title'}")
    
    # Look for different content containers
    print("\n🔍 Looking for content containers:")
    
    containers = [
        ('div.poem', soup.find('div', class_='poem')),
        ('div#poem', soup.find('div', id='poem')),
        ('main', soup.find('main')),
        ('article', soup.find('article')),
        ('div.content', soup.find('div', class_='content')),
        ('div.entry-content', soup.find('div', class_='entry-content')),
        ('div.post-content', soup.find('div', class_='post-content')),
    ]
    
    for name, container in containers:
        if container:
            print(f"✅ Found {name}")
            text = container.get_text()[:200]
            print(f"   Preview: {text}...")
        else:
            print(f"❌ No {name}")
    
    # Look for all divs with classes
    print("\n📋 All div classes found:")
    divs = soup.find_all('div', class_=True)
    classes = set()
    for div in divs:
        classes.update(div.get('class', []))
    
    for cls in sorted(classes)[:20]:
        print(f"   .{cls}")
    
    # Look for headings
    print("\n📝 Headings found:")
    for i in range(1, 7):
        headings = soup.find_all(f'h{i}')
        for h in headings:
            print(f"   H{i}: {h.get_text().strip()}")
    
    # Look for paragraphs
    print("\n📄 First few paragraphs:")
    paragraphs = soup.find_all('p')
    for i, p in enumerate(paragraphs[:5]):
        text = p.get_text().strip()
        if text:
            print(f"   P{i+1}: {text[:100]}...")

if __name__ == "__main__":
    debug_poetry_daily() 