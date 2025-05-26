#!/usr/bin/env python3
"""
Poem Link Discovery System
Discovers actual poem URLs from poetry websites by analyzing link patterns
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Set
import json

# Site-specific configurations for poem link discovery
SITE_CONFIGS = {
    'poems.com': {
        'name': 'Poetry Daily',
        'base_urls': [
            'https://poems.com/',
            'https://poems.com/archive/',
            'https://poems.com/poems/'
        ],
        'poem_patterns': [
            r'^/poem/[^/]+/$',  # Individual poem pages only
            r'^/todays-poem/?$'  # Today's poem only
        ],
        'css_selectors': [
            'a[href*="/poem/"]'
        ],
        'exclude_patterns': [
            r'/about',
            r'/contact',
            r'/subscribe',
            r'/newsletter',
            r'/search',
            r'/browse',
            r'/submit',
            r'/features',
            r'/archives',
            r'/what-sparks-poetry',
            r'/news',
            r'/support'
        ]
    },
    'versedaily.org': {
        'name': 'Verse Daily',
        'base_urls': [
            'https://www.versedaily.org/',
            'https://www.versedaily.org/archive.html'
        ],
        'poem_patterns': [
            r'^/\d{4}/.*\.html$',
            r'^/poems/.*\.html$'
        ],
        'css_selectors': [
            'a[href$=".html"]',
            'div.archive a'
        ],
        'exclude_patterns': [
            r'/about',
            r'/contact',
            r'/submit',
            r'/index'
        ]
    },
    'poetryfoundation.org': {
        'name': 'Poetry Foundation',
        'base_urls': [
            'https://www.poetryfoundation.org/poems/browse',
            'https://www.poetryfoundation.org/poems'
        ],
        'poem_patterns': [
            r'^/poems/\d+/[^/]+$',  # Individual poem pages with ID and title
            r'^/poetrymagazine/poems/\d+/[^/]+$'  # Poetry Magazine poems
        ],
        'css_selectors': [
            'a[href*="/poems/"][href*="/"]',
            'a[href*="/poetrymagazine/poems/"]'
        ],
        'exclude_patterns': [
            r'/poets',
            r'/articles',
            r'/browse',
            r'/search',
            r'/about',
            r'/guides',
            r'/poem-of-the-day',
            r'/programs'
        ]
    },
    'poetrymagazine.org': {
        'name': 'Poetry Magazine',
        'base_urls': [
            'https://www.poetrymagazine.org/',
            'https://www.poetrymagazine.org/poems'
        ],
        'poem_patterns': [
            r'^/poems/.*$',
            r'^/poem/.*$'
        ],
        'css_selectors': [
            'a[href*="/poems/"]',
            'div.poem-listing a'
        ],
        'exclude_patterns': [
            r'/articles',
            r'/reviews',
            r'/about',
            r'/subscribe'
        ]
    },
    'rattle.com': {
        'name': 'Rattle Magazine',
        'base_urls': [
            'https://rattle.com/poetry/',
            'https://rattle.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about',
            r'/submit',
            r'/subscribe',
            r'/category'
        ]
    },
    'theadroitjournal.org': {
        'name': 'The Adroit Journal',
        'base_urls': [
            'https://theadroitjournal.org/',
            'https://theadroitjournal.org/category/poetry/'
        ],
        'poem_patterns': [
            r'^/\d{4}/\d{2}/\d{2}/[^/]*poem[^/]*/$',  # Only URLs with "poem" in the path
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about',
            r'/submit',
            r'/category',
            r'/review',
            r'/interview',
            r'/essay',
            r'/critical-essays',
            r'/conversation',
            r'/profile',
            r'/announcement',
            r'review-of',
            r'conversation-with',
            r'interview-with',
            r'critical-essays',
            r'marie-howe',
            r'ruth-lilly',
            r'poetry-prize',
            r'building-the-perfect',
            r'new-and-selected',
            r'poetry-and-lightness',
            r'lightness',
            r'wins',
            r'winner',
            r'prize',
            r'award',
            r'selected-poems'
        ]
    },
    'www.poetrynw.org': { 
        'name': 'Poetry Northwest',
        'base_urls': [
            'https://www.poetrynw.org/' 
        ],
        'poem_patterns': [
            r'/poems/.*/$' # Placeholder - needs review
        ],
        'css_selectors': [
            'a[href*="/poems/"]' # Placeholder - needs review
        ],
        'exclude_patterns': [
            r'/about',
            r'/submit'
        ]
    },
    'barrenmagazine.com': {
        'name': 'Barren Magazine',
        'base_urls': ['https://barrenmagazine.com/'], 
        'poem_patterns': [r'/[^/]+/[^/]+/?$'], # Placeholder - needs review, very generic
        'css_selectors': ['article a'], # Placeholder - needs review
        'exclude_patterns': [r'/about', r'/submissions']
    },
    'greensbororeview.org': {
        'name': 'Greensboro Review',
        'base_urls': ['https://greensbororeview.org/'], 
        'poem_patterns': [r'/issue-\d+/.*html$'], # Placeholder - needs review
        'css_selectors': ['a[href*=".html"]'], # Placeholder - needs review
        'exclude_patterns': [r'/about', r'/contests']
    }
}

def get_poem_links(base_url: str, site_config: Dict) -> List[str]:
    """
    Discover actual poem URLs from a poetry website
    
    Args:
        base_url: The base URL to start discovery from
        site_config: Configuration dict with patterns and selectors
        
    Returns:
        List of discovered poem URLs
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0; +https://github.com/poetrybot)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    discovered_links = set()
    
    try:
        print(f"🔍 Discovering poem links from {base_url}")
        
        # Fetch the page
        response = requests.get(base_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code} for {base_url}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Use CSS selectors if provided
        if 'css_selectors' in site_config:
            for selector in site_config['css_selectors']:
                try:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get('href')
                        if href:
                            # Convert relative URLs to absolute
                            absolute_url = urljoin(base_url, href)
                            discovered_links.add(absolute_url)
                            print(f"  📎 CSS selector found: {absolute_url}")
                except Exception as e:
                    print(f"⚠️  CSS selector '{selector}' failed: {e}")
        
        # Method 2: Pattern matching on all links
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href', '')
            
            # Skip empty hrefs
            if not href:
                continue
            
            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)
            
            # Check if URL matches poem patterns
            if 'poem_patterns' in site_config:
                for pattern in site_config['poem_patterns']:
                    if re.match(pattern, parsed_url.path):
                        # Check if it should be excluded
                        should_exclude = False
                        if 'exclude_patterns' in site_config:
                            for exclude_pattern in site_config['exclude_patterns']:
                                if re.search(exclude_pattern, parsed_url.path):
                                    should_exclude = True
                                    break
                        
                        if not should_exclude:
                            discovered_links.add(absolute_url)
                            print(f"  📝 Pattern match found: {absolute_url}")
                            break
        
        # Method 3: Look for common poem indicators in link text (ENHANCED)
        poem_text_indicators = [
            'poem', 'poetry', 'verse', 'sonnet', 'haiku', 'ballad',
            'elegy', 'ode', 'limerick', 'free verse'
        ]
        
        # ENHANCED: Exclude terms that indicate non-poem content
        exclude_text_indicators = [
            'review', 'essay', 'interview', 'conversation', 'profile',
            'announcement', 'news', 'winner', 'prize', 'award', 'wins',
            'selected poems', 'new and selected', 'building the perfect',
            'lightness', 'marie howe', 'ruth lilly', 'critical essay',
            'about', 'biography', 'memoir', 'craft essay', 'poetics'
        ]
        
        for link in all_links:
            href = link.get('href', '')
            link_text = link.get_text().lower().strip()
            
            # Check if link text contains poem indicators
            has_poem_indicator = any(indicator in link_text for indicator in poem_text_indicators)
            
            # Check if link text contains exclusion indicators
            has_exclude_indicator = any(indicator in link_text for indicator in exclude_text_indicators)
            
            if href and has_poem_indicator and not has_exclude_indicator:
                absolute_url = urljoin(base_url, href)
                parsed_url = urlparse(absolute_url)
                
                # Enhanced exclusion check
                exclude_terms = [
                    'about', 'contact', 'submit', 'subscribe', 'search', 'browse',
                    'review', 'essay', 'interview', 'conversation', 'profile',
                    'announcement', 'news', 'winner', 'prize', 'award', 'wins',
                    'lightness', 'marie-howe', 'ruth-lilly', 'critical-essay',
                    'building-the-perfect', 'new-and-selected'
                ]
                
                if not any(term in parsed_url.path.lower() for term in exclude_terms):
                    discovered_links.add(absolute_url)
                    print(f"  📖 Text indicator found: {absolute_url}")
        
    except Exception as e:
        print(f"❌ Error discovering links from {base_url}: {e}")
    
    # Convert to sorted list and remove duplicates
    unique_links = list(discovered_links)
    unique_links.sort()
    
    print(f"✅ Discovered {len(unique_links)} potential poem links from {base_url}")
    return unique_links

def discover_all_poem_links(domain: str, max_links: int = 50) -> List[str]:
    """
    Discover poem links from all configured URLs for a domain
    
    Args:
        domain: Domain name (e.g., 'poems.com')
        max_links: Maximum number of links to return
        
    Returns:
        List of discovered poem URLs
    """
    if domain not in SITE_CONFIGS:
        print(f"❌ No configuration found for domain: {domain}")
        return []
    
    config = SITE_CONFIGS[domain]
    all_links = set()
    
    print(f"🌐 Discovering poem links for {config['name']} ({domain})")
    
    # Try each base URL
    for base_url in config['base_urls']:
        try:
            links = get_poem_links(base_url, config)
            all_links.update(links)
            
            # Add delay between requests to be respectful
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Failed to discover links from {base_url}: {e}")
    
    # Convert to list and limit results
    final_links = list(all_links)[:max_links]
    
    print(f"🎯 Total discovered links for {domain}: {len(final_links)}")
    return final_links

def validate_poem_url(url: str) -> bool:
    """
    Validate that a URL actually contains a poem
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL contains a poem, False otherwise
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)',
        'Accept': 'text/html,application/xhtml+xml'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text().lower()
        
        # Look for poem indicators
        poem_indicators = [
            'poem', 'poetry', 'verse', 'stanza', 'line break',
            'metaphor', 'imagery', 'rhythm', 'rhyme'
        ]
        
        # Look for non-poem indicators (essays, news, etc.)
        non_poem_indicators = [
            'essay', 'article', 'review', 'interview', 'news',
            'announcement', 'press release', 'biography', 'about the author',
            'table of contents', 'subscribe', 'newsletter'
        ]
        
        poem_score = sum(1 for indicator in poem_indicators if indicator in text)
        non_poem_score = sum(1 for indicator in non_poem_indicators if indicator in text)
        
        # Simple scoring: more poem indicators than non-poem indicators
        return poem_score > non_poem_score
        
    except Exception as e:
        print(f"⚠️  Validation failed for {url}: {e}")
        return False

def test_poem_discovery():
    """Test the poem discovery system"""
    print("🧪 Testing Poem Link Discovery System")
    print("=" * 60)
    
    # Test each configured domain
    for domain in SITE_CONFIGS.keys():
        print(f"\n🔍 Testing {domain}...")
        
        links = discover_all_poem_links(domain, max_links=10)
        
        if links:
            print(f"✅ Found {len(links)} potential poem links")
            
            # Test validation on first few links
            print("🔬 Validating first 3 links...")
            for i, link in enumerate(links[:3]):
                is_valid = validate_poem_url(link)
                status = "✅ Valid poem" if is_valid else "❌ Not a poem"
                print(f"   {i+1}. {status}: {link}")
        else:
            print("❌ No links discovered")
        
        print("-" * 40)

def save_discovered_links(output_file: str = 'discovered_poem_links.json'):
    """
    Discover and save all poem links to a JSON file
    
    Args:
        output_file: Output filename for the JSON file
    """
    all_discovered = {}
    
    for domain in SITE_CONFIGS.keys():
        print(f"\n🔍 Processing {domain}...")
        links = discover_all_poem_links(domain, max_links=100)
        
        if links:
            # Validate a sample of links
            validated_links = []
            for link in links[:20]:  # Validate first 20 links
                if validate_poem_url(link):
                    validated_links.append(link)
                time.sleep(0.5)  # Be respectful with validation requests
            
            all_discovered[domain] = {
                'site_name': SITE_CONFIGS[domain]['name'],
                'total_discovered': len(links),
                'all_links': links,
                'validated_links': validated_links,
                'validation_sample_size': min(20, len(links))
            }
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(all_discovered, f, indent=2)
    
    print(f"\n💾 Saved discovered links to {output_file}")
    
    # Print summary
    print("\n📊 Discovery Summary:")
    for domain, data in all_discovered.items():
        print(f"   {data['site_name']}: {data['total_discovered']} discovered, {len(data['validated_links'])} validated")

if __name__ == "__main__":
    # Run the test
    test_poem_discovery()
    
    # Optionally save all discovered links
    # save_discovered_links() 