#!/usr/bin/env python3
"""
Find author structure in Poetry Daily
"""

import requests
from bs4 import BeautifulSoup

def find_author_structure():
    """Find where the author information is located"""
    url = 'https://poems.com/todays-poem/'
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(f"Examining: {url}")
    
    # Get the main content area
    main_content = soup.find('div', class_='elementor-widget-theme-post-content')
    if main_content:
        print("\n=== MAIN CONTENT STRUCTURE ===")
        
        # Look at the parent structure
        parent = main_content.parent
        while parent and parent.name != 'body':
            print(f"Parent: {parent.name} with classes: {parent.get('class', [])}")
            
            # Look for siblings that might contain author info
            for sibling in parent.find_all(['div', 'h1', 'h2', 'h3', 'p', 'span']):
                text = sibling.get_text().strip()
                if text and len(text) < 100:  # Reasonable length for author info
                    # Check if it looks like an author name
                    words = text.split()
                    if 2 <= len(words) <= 4:
                        if all(word[0].isupper() for word in words if len(word) > 1):
                            print(f"  Potential author: {text} (in {sibling.name} with classes {sibling.get('class', [])})")
            
            parent = parent.parent
            if parent and 'elementor-column' in str(parent.get('class', [])):
                break  # Stop at column level
    
    # Look for all text that might be author names in the entire page
    print("\n=== ALL POTENTIAL AUTHORS ===")
    all_text = soup.get_text()
    lines = [line.strip() for line in all_text.split('\n') if line.strip()]
    
    potential_authors = set()
    for line in lines:
        # Skip very long lines
        if len(line) > 50:
            continue
        
        # Look for proper names (2-4 words, title case)
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if all words start with capital letters
            if all(word[0].isupper() for word in words if len(word) > 1):
                # Exclude common non-author phrases
                exclude_phrases = [
                    'poetry daily', 'today poem', 'book features', 'what sparks',
                    'editorial board', 'contact us', 'media kit', 'about poetry',
                    'featured poet', 'featured translator', 'receive poetry',
                    'each morning', 'share this', 'print this', 'feature date',
                    'selected by', 'four way', 'way books', 'new directions'
                ]
                
                if not any(phrase in line.lower() for phrase in exclude_phrases):
                    potential_authors.add(line)
    
    print("Potential author names found:")
    for author in sorted(potential_authors):
        print(f"  {author}")
    
    # Look specifically in the poem content area for author info
    print("\n=== AUTHOR IN POEM CONTENT ===")
    if main_content:
        content_text = main_content.get_text()
        lines = content_text.split('\n')
        
        # Look for author attribution patterns
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check if line looks like author attribution
            if (len(line) < 50 and 
                not line.startswith('(') and 
                not any(word in line.lower() for word in ['operation', 'surgery', 'risks', 'discussed'])):
                
                words = line.split()
                if 2 <= len(words) <= 4:
                    if all(word[0].isupper() for word in words if len(word) > 1):
                        print(f"  Line {i}: {line}")

if __name__ == "__main__":
    find_author_structure() 