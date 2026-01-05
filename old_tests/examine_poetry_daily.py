#!/usr/bin/env python3
"""
Script to examine Poetry Daily HTML structure
"""

import requests
from bs4 import BeautifulSoup

def examine_poetry_daily():
    """Examine the structure of Poetry Daily"""
    url = 'https://poems.com/todays-poem/'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"Examining: {url}")
    print(f"Status: {response.status_code}")
    
    # Look for title
    print("\n=== TITLE SEARCH ===")
    title_elem = soup.find('title')
    if title_elem:
        page_title = title_elem.get_text()
        print(f"Page title: {page_title}")
        # Extract poem title from page title
        if ' – Poetry Daily' in page_title:
            poem_title = page_title.replace(' – Poetry Daily', '').strip()
            print(f"Extracted poem title: {poem_title}")
    
    # Look for h1, h2 elements
    for tag in ['h1', 'h2', 'h3']:
        elements = soup.find_all(tag)
        if elements:
            print(f"{tag.upper()} elements:")
            for elem in elements[:5]:
                text = elem.get_text().strip()
                if text:
                    print(f"  {text}")
    
    # Look for author information
    print("\n=== AUTHOR SEARCH ===")
    
    # Check all links for poet links
    poet_links = soup.find_all('a', href=True)
    for link in poet_links:
        href = link.get('href', '')
        text = link.get_text().strip()
        if '/poet/' in href and text and text != 'Instagram':
            print(f"Poet link found: {text} -> {href}")
    
    # Look for any text that might be author name
    all_text = soup.get_text()
    lines = [line.strip() for line in all_text.split('\n') if line.strip()]
    
    # Look for lines that might contain author info
    potential_authors = []
    for line in lines:
        # Skip very long lines (likely not author names)
        if len(line) > 50:
            continue
        # Look for lines that might be author names
        if any(word in line.lower() for word in ['by ', 'author', 'poet']):
            potential_authors.append(line)
        # Look for lines that are just names (2-4 words, proper case)
        words = line.split()
        if 2 <= len(words) <= 4:
            if all(word[0].isupper() for word in words if len(word) > 1):
                potential_authors.append(line)
    
    print("Potential author lines:")
    for author in potential_authors[:10]:
        print(f"  {author}")

if __name__ == "__main__":
    examine_poetry_daily() 