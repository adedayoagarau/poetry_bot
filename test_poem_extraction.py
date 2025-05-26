#!/usr/bin/env python3
"""
Test poem extraction from different literary journals
"""

from poetry_bot import PoetryBot
from config import LITERARY_JOURNALS
import random
import requests
from bs4 import BeautifulSoup
import sys

def test_poem_sources():
    print("🔍 Testing Poem Extraction from Literary Journals")
    print("=" * 60)
    
    bot = PoetryBot()
    
    # Test a few different sources
    test_sources = [
        'Poetry Daily',
        'Verse Daily', 
        'Poetry Foundation',
        'The Paris Review',
        'Rattle Magazine'
    ]
    
    for source_name in test_sources:
        print(f"\n📚 Testing: {source_name}")
        print("-" * 40)
        
        # Find the journal config
        journal = None
        for j in LITERARY_JOURNALS:
            if j['name'] == source_name:
                journal = j
                break
        
        if not journal:
            print(f"❌ Journal config not found for {source_name}")
            continue
            
        try:
            poem = bot.fetch_from_journal(journal)
            if poem:
                print(f"✅ Found poem: '{poem['title'][:50]}...'")
                print(f"👤 Author: {poem['author']}")
                print(f"📝 Text preview: {poem['text'][:100]}...")
                print(f"🔗 URL: {poem.get('url', 'No URL')}")
                
                # Test the formatting
                tweet_text = bot.format_tweet_text(poem)
                print(f"🐦 Tweet preview ({len(tweet_text)} chars):")
                print(tweet_text[:200] + "..." if len(tweet_text) > 200 else tweet_text)
            else:
                print(f"❌ No poem found from {source_name}")
                
        except Exception as e:
            print(f"❌ Error with {source_name}: {e}")
    
    print(f"\n🎯 Recommendation: Use sources that successfully extract real poem content")
    print(f"📝 Format: Your exact format is now implemented!")

def test_poem_extraction(url, source_name):
    """Test poem extraction from a specific URL"""
    print(f"\n🔍 Testing: {source_name}")
    print(f"📍 URL: {url}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # For Poetry Daily - get today's featured poem
        if 'poems.com' in url:
            print("📝 Extracting from Poetry Daily...")
            poem_content = soup.find('div', class_='poem') or soup.find('div', id='poem') or soup.find('main')
            
            if poem_content:
                # Extract title
                title_elem = poem_content.find('h1') or poem_content.find('h2')
                title = title_elem.text.strip() if title_elem else "Daily Poem"
                
                # Extract author
                author_elem = poem_content.find('span', class_='author') or poem_content.find('p', class_='author')
                if not author_elem:
                    text_content = poem_content.get_text()
                    import re
                    author_match = re.search(r'by\s+([^\n]+)', text_content, re.IGNORECASE)
                    author = author_match.group(1).strip() if author_match else "Unknown"
                else:
                    author = author_elem.text.strip()
                
                # Extract poem text
                poem_text = poem_content.get_text(separator='\n').strip()
                lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
                
                # Clean up - remove title/author/navigation
                clean_lines = []
                for line in lines:
                    if (title.lower() not in line.lower() and 
                        author.lower() not in line.lower() and
                        'by ' not in line.lower()[:10] and
                        len(line.strip()) > 10):
                        clean_lines.append(line)
                
                poem_text = '\n'.join(clean_lines[:10])
                
                print(f"📖 Title: {title}")
                print(f"✍️  Author: {author}")
                print(f"📝 Text preview: {poem_text[:200]}...")
                
                return {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': source_name
                }
        
        # For Verse Daily
        elif 'versedaily.org' in url:
            print("📝 Extracting from Verse Daily...")
            # Similar extraction logic
            
        print("⚠️  No poem content found")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Test the most reliable sources"""
    reliable_sources = [
        ('Poetry Daily', 'https://poems.com/'),
        ('Verse Daily', 'https://www.versedaily.org/'),
        ('Poetry Foundation', 'https://www.poetryfoundation.org/poems/browse'),
        ('Rattle Magazine', 'https://rattle.com/poetry/'),
    ]
    
    print("🧪 Testing poem extraction from reliable sources...")
    
    for name, url in reliable_sources:
        poem = test_poem_extraction(url, name)
        if poem:
            print(f"✅ Success! Found poem from {name}")
            # Test validation
            print(f"📏 Text length: {len(poem['text'])} chars")
            print(f"📄 Lines: {len(poem['text'].split())}")
        else:
            print(f"❌ Failed to extract from {name}")
        
        print("-" * 60)

if __name__ == "__main__":
    main() 