#!/usr/bin/env python3
"""
Test script for reliable poetry sources with known good poem URLs
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def test_poetry_foundation_specific_poems():
    """Test extraction from specific Poetry Foundation poem URLs that we know work"""
    
    # These are actual poem URLs from Poetry Foundation that we discovered earlier
    test_urls = [
        'https://www.poetryfoundation.org/poetrymagazine/poems/1668174/self-portrait-as-the-mountain',
        'https://www.poetryfoundation.org/poetrymagazine/poems/1668156/petition-for-reintroduction',
        'https://www.poetryfoundation.org/poetrymagazine/poems/1668158/street-food',
        'https://www.poetryfoundation.org/poetrymagazine/poems/1668160/working-with-jimmy-above-a-drop-ceiling',
        'https://www.poetryfoundation.org/poems/42749/love-in-the-weathers-bells'
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = "Untitled"
            title_selectors = [
                'h1', 'h1.c-hdgSerif', '.c-feature-hd', '.poem-title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text().strip()
                    break
            
            # Extract author
            author = "Unknown"
            author_selectors = [
                '.c-feature-sub', '.c-txt_attribution', '.author', 
                'a[href*="/poets/"]', '.byline'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author = author_elem.get_text().strip()
                    # Clean up author name
                    author = re.sub(r'^(by\\s+)', '', author, flags=re.IGNORECASE)
                    author = re.sub(r'(,.*$)', '', author)
                    break
            
            # Extract poem content
            poem_content = None
            poem_selectors = [
                '.c-feature-bd', '.poem-content', '.c-txt', 
                'div[data-view="poem"]', '.entry-content'
            ]
            
            for selector in poem_selectors:
                content = soup.select_one(selector)
                if content:
                    poem_content = content
                    break
            
            if not poem_content:
                print(f"⚠️  No poem content found")
                continue
            
            # Extract and clean poem text
            poem_text = poem_content.get_text(separator='\\n').strip()
            lines = [line.strip() for line in poem_text.split('\\n') if line.strip()]
            
            # Clean up lines - remove navigation, metadata, etc.
            clean_lines = []
            exclude_patterns = [
                'subscribe', 'newsletter', 'archive', 'browse', 'search',
                'about', 'contact', 'home', 'menu', 'navigation',
                'read more', 'continue reading', 'full text',
                'print issues', 'buy now', 'purchase', 'add to cart',
                'interviews', 'reviews', 'submissions', 'guidelines',
                'editorial', 'editor', 'staff', 'masthead',
                'winner', 'finalist', 'contest', 'award',
                'university', 'college', 'press', 'publisher',
                'www.', 'http', '.com', '.org', 'poetry foundation',
                'poetry magazine', 'poetryfoundation.org'
            ]
            
            for line in lines:
                line_lower = line.lower()
                
                # Skip if contains title, author, or excluded patterns
                if (title.lower() not in line_lower and 
                    author.lower() not in line_lower and
                    'by ' not in line_lower[:10] and
                    not any(pattern in line_lower for pattern in exclude_patterns) and
                    len(line.strip()) > 5 and
                    not line.strip().startswith('(') and
                    not line.strip().endswith(')') and
                    '//' not in line and
                    not line.isdigit()):
                    clean_lines.append(line)
            
            # Take first 15 lines of actual poem content
            poem_text = '\\n'.join(clean_lines[:15])
            
            print(f"📝 Title: {title}")
            print(f"👤 Author: {author}")
            print(f"📖 Content preview: {poem_text[:200]}...")
            print(f"📊 Clean lines: {len(clean_lines)}")
            
            if len(poem_text) > 50 and len(clean_lines) >= 3:
                print("✅ Valid poem extracted!")
                
                # Show first few lines as sample
                sample_lines = clean_lines[:4]
                print(f"🎭 Sample lines:")
                for line in sample_lines:
                    print(f"   {line}")
                    
                return {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': 'Poetry Foundation',
                    'url': url
                }
            else:
                print(f"⚠️  Insufficient content: {len(poem_text)} chars, {len(clean_lines)} lines")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None

def test_poems_com_specific():
    """Test extraction from Poetry Daily specific poem URLs"""
    
    # Test the specific poem URLs we found from Poetry Daily
    test_urls = [
        'https://poems.com/poem/daughter/',
        'https://poems.com/poem/ahshinayo/',
        'https://poems.com/poem/visitation/',
        'https://poems.com/poem/salam-to-gaza/',
        'https://poems.com/poem/in-reverse/'
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
    
    for url in test_urls:
        print(f"\n🔍 Testing Poetry Daily: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title from URL or page
            title = url.split('/')[-2].replace('-', ' ').title()
            
            # Look for title in page
            title_elem = soup.find('h1') or soup.find('h2') or soup.find('title')
            if title_elem:
                page_title = title_elem.get_text().strip()
                if len(page_title) < 100:  # Reasonable title length
                    title = page_title
            
            # Extract author
            author = "Unknown"
            author_patterns = [
                r'by\\s+([^\\n,]+)',
                r'—\\s*([A-Z][a-zA-Z\\s\\.]+)',
                r'\\n([A-Z][a-zA-Z\\s\\.]+)\\s*$'
            ]
            
            text_content = soup.get_text()
            for pattern in author_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    author = match.group(1).strip()
                    break
            
            # Extract poem content
            poem_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            
            if poem_content:
                poem_text = poem_content.get_text(separator='\\n').strip()
                lines = [line.strip() for line in poem_text.split('\\n') if line.strip()]
                
                # Clean lines
                clean_lines = []
                for line in lines:
                    if (len(line) > 5 and 
                        'poetry daily' not in line.lower() and
                        'poems.com' not in line.lower() and
                        'subscribe' not in line.lower() and
                        'newsletter' not in line.lower()):
                        clean_lines.append(line)
                
                poem_text = '\\n'.join(clean_lines[:15])
                
                print(f"📝 Title: {title}")
                print(f"👤 Author: {author}")
                print(f"📖 Content preview: {poem_text[:200]}...")
                
                if len(poem_text) > 50:
                    print("✅ Valid poem extracted!")
                    return {
                        'title': title,
                        'author': author,
                        'text': poem_text,
                        'source': 'Poetry Daily',
                        'url': url
                    }
                else:
                    print(f"⚠️  Insufficient content")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return None

if __name__ == "__main__":
    print("🧪 Testing Reliable Poetry Sources")
    print("=" * 50)
    
    print("\\n1. Testing Poetry Foundation specific poems...")
    pf_poem = test_poetry_foundation_specific_poems()
    
    print("\\n2. Testing Poetry Daily specific poems...")
    pd_poem = test_poems_com_specific()
    
    if pf_poem or pd_poem:
        print("\\n✅ SUCCESS: Found working poem sources!")
        if pf_poem:
            print(f"   Poetry Foundation: {pf_poem['title']} by {pf_poem['author']}")
        if pd_poem:
            print(f"   Poetry Daily: {pd_poem['title']} by {pd_poem['author']}")
    else:
        print("\\n❌ No working sources found") 