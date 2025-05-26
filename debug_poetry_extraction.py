#!/usr/bin/env python3
"""
Debug script to test poem extraction and validation
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from poem_link_discovery import get_poem_links, SITE_CONFIGS

def validate_poem_content_debug(poem_data, url=None):
    """Debug version of validate_poem_content with detailed logging"""
    print(f"\n🔍 VALIDATING POEM CONTENT:")
    print("=" * 50)
    
    if not poem_data:
        print("❌ No poem data provided")
        return False, "No poem data provided"
    
    # Check required fields
    required_fields = ['title', 'author', 'text', 'source']
    for field in required_fields:
        if not poem_data.get(field):
            print(f"❌ Missing required field: {field}")
            return False, f"Missing required field: {field}"
    
    # Validate poem text quality
    text = poem_data['text'].strip()
    title = poem_data['title'].strip()
    
    print(f"📝 Title: {title}")
    print(f"👤 Author: {poem_data['author']}")
    print(f"📊 Text length: {len(text)} characters")
    
    # Check minimum length (avoid fragments)
    if len(text) < 30:
        print("❌ Poem text too short (likely incomplete)")
        return False, "Poem text too short (likely incomplete)"
    
    # Check for common error patterns
    error_patterns = [
        'page not found', '404', 'error', 'access denied',
        'subscription required', 'login required', 'not available',
        'coming soon', 'under construction', 'temporarily unavailable'
    ]
    
    text_lower = text.lower()
    title_lower = title.lower()
    
    for pattern in error_patterns:
        if pattern in text_lower:
            print(f"❌ Content contains error pattern: {pattern}")
            return False, f"Content contains error pattern: {pattern}"
    
    # ENHANCED: Check for essay/review/critical content in title
    essay_title_indicators = [
        'review of', 'a review', 'essay', 'critical essay', 'interview',
        'conversation with', 'profile', 'announcement', 'news', 'wins',
        'winner', 'prize', 'award', 'selected poems', 'new and selected',
        'building the perfect', 'poetry and lightness', 'lightness',
        'six memos', 'memoir', 'biography', 'about', 'on writing',
        'craft essay', 'poetics', 'ars poetica'
    ]
    
    for indicator in essay_title_indicators:
        if indicator in title_lower:
            print(f"❌ Title indicates essay/review content: '{indicator}' in '{title}'")
            return False, f"Title indicates essay/review content: '{indicator}' in '{title}'"
    
    # Check that it looks like actual poetry (not just navigation text or prose)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) < 2:
        print("❌ Insufficient poem content (needs multiple lines)")
        return False, "Insufficient poem content (needs multiple lines)"
    
    # Avoid poems that are just titles/headers
    if all(len(line) < 10 for line in lines):
        print("❌ Lines too short (likely navigation text)")
        return False, "Lines too short (likely navigation text)"
    
    # ENHANCED: Check for prose vs poetry indicators
    # Poetry typically has shorter lines, more line breaks, less dense text
    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
    long_lines = sum(1 for line in lines if len(line) > 100)
    very_long_lines = sum(1 for line in lines if len(line) > 200)
    
    print(f"📊 Average line length: {avg_line_length:.1f}")
    print(f"📊 Long lines (>100 chars): {long_lines}/{len(lines)}")
    print(f"📊 Very long lines (>200 chars): {very_long_lines}/{len(lines)}")
    
    # If most lines are very long, it's likely prose, not poetry
    if avg_line_length > 80 and long_lines > len(lines) * 0.7:
        print("❌ Content appears to be prose, not poetry (long lines)")
        return False, "Content appears to be prose, not poetry (long lines)"
    
    # If we have very long lines (200+ chars), it's almost certainly prose
    if very_long_lines > len(lines) * 0.3:
        print("❌ Content appears to be prose, not poetry (very long lines)")
        return False, "Content appears to be prose, not poetry (very long lines)"
    
    # ENHANCED: Check for essay/article indicators (more comprehensive)
    prose_indicators = [
        'paragraph', 'essay', 'article', 'chapter', 'section',
        'in this piece', 'the author', 'the writer', 'the poet writes',
        'according to', 'as mentioned', 'furthermore', 'however',
        'in conclusion', 'to summarize', 'for example', 'such as',
        'calvino', 'italo calvino', 'six memos', 'lightness',
        'collection', 'book of poetry', 'draws from', 'covers a range',
        'most compelling when', 'we find', 'therein we find',
        'what begins as', 'american poetry landscape', 'increasingly dominated',
        'feel like a refreshing', 'return to', 'lyric poetry',
        'the opening poem', 'the collection', 'in fiction',
        'transformation needs', 'slow build-up', 'in poetry',
        'can be transformative', 'as wordsworth writes',
        'the speaker', 'voice is', 'casually disarming',
        'equally accessible', 'compelling', 'occasionally',
        'drawing on', 'richard drew', 'infamous', 'two refrains',
        'evoke the compulsive', 'leaves us with'
    ]
    
    # Check for navigation/table of contents indicators
    navigation_indicators = [
        'shortlist', 'table of contents', 'contents', 'issue', 'volume',
        'poem of the year', 'winner', 'finalist', 'submission', 'contest',
        'featured', 'latest', 'recent', 'archive', 'browse', 'category',
        'genre', 'author index', 'title index', 'search results',
        'subscriptions', 'international orders', 'support us', 'bananas, sweetheart',
        'pdnews', 'hot off the presses', 'what sparks poetry', 'book features',
        'features', 'news', 'archives', 'media kit', 'editorial board',
        'welcome publishers', 'messages to readers', 'essay:', 'announcement:',
        'profile:', 'interview:', 'from the book', 'read today', 'connect',
        'appearance', 'signature project', 'macarthur', 'national book award',
        'poet laureate', 'pulitzer prize', 'griffin poetry prize'
    ]
    
    prose_count = sum(1 for indicator in prose_indicators if indicator in text_lower)
    nav_count = sum(1 for indicator in navigation_indicators if indicator in text_lower)
    
    print(f"📊 Prose indicators found: {prose_count}")
    print(f"📊 Navigation indicators found: {nav_count}")
    
    # ENHANCED: Lower thresholds for stricter validation
    if prose_count >= 2:  # Reduced from 3
        print(f"❌ Content appears to be prose/essay about poetry, not actual poetry (prose indicators: {prose_count})")
        return False, f"Content appears to be prose/essay about poetry, not actual poetry (prose indicators: {prose_count})"
    
    if nav_count >= 2:
        print("❌ Content appears to be navigation/table of contents, not actual poetry")
        return False, "Content appears to be navigation/table of contents, not actual poetry"
    
    # ENHANCED: Check for specific problematic line patterns we've encountered
    problematic_patterns = [
        'essay:', 'announcement:', 'profile:', 'interview:', 'mentions of',
        'scientists use', 'atwood with be', 'marie howe wins', 'double dreaming',
        'if i were to choose one principle', 'guided me while writing',
        'full-length poetry collection', 'chronicle of drifting',
        'copper canyon press', 'calvino celebrates', 'practice lightness',
        'subtraction of weight', 'poets practice lightness',
        'american poetry landscape', 'increasingly dominated',
        'instagramable verse', 'present-day politics',
        'erotically charged', 'philosophical meditations',
        'refreshing return', 'lyric poetry', 'four way books',
        'sixth book of poetry', 'draws from three decades',
        'covers a range of themes', 'most compelling when writing',
        'intersection of myth', 'human body', 'opening poem',
        'collection', 'drawing from the wells', 'storytelling and science'
    ]
    
    problematic_found = []
    for line in lines:
        line_lower = line.lower()
        for pattern in problematic_patterns:
            if pattern in line_lower:
                problematic_found.append(pattern)
    
    if problematic_found:
        print(f"❌ Content contains essay/review patterns: {problematic_found}")
        return False, f"Content contains essay/review pattern: {problematic_found[0]}"
    
    # ENHANCED: Check if content starts like an essay
    first_few_lines = ' '.join(lines[:3]).lower()
    essay_starters = [
        'if i were to choose', 'in an american poetry', 'what begins as',
        'the speaker', 'this might seem', 'in our moment',
        'to practice lightness', 'poets practice', 'take simile',
        'in fiction', 'in poetry', 'as wordsworth writes',
        'at first', 'while simile', 'in my mind'
    ]
    
    for starter in essay_starters:
        if starter in first_few_lines:
            print(f"❌ Content starts like an essay: '{starter}'")
            return False, f"Content starts like an essay: '{starter}'"
    
    # ENHANCED: Check if content is too long to be a typical poem excerpt
    if len(text) > 2000:  # Most poems are shorter than this
        print(f"❌ Content too long ({len(text)} chars) - likely essay or review, not poem")
        return False, "Content too long (likely essay or review, not poem)"
    
    print("✅ POEM CONTENT VALIDATION PASSED")
    return True, "Poem content validated successfully"

def debug_poem_extraction(url, source_name="Test"):
    """Debug version of extract_poem_from_url with detailed logging"""
    print(f"\n🔍 DEBUGGING POEM EXTRACTION FROM: {url}")
    print("=" * 80)
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code} for {url}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Debug: Show page title
        page_title = soup.find('title')
        if page_title:
            print(f"📄 Page Title: {page_title.get_text().strip()}")
        
        # Extract title - try multiple selectors
        print("\n🏷️  EXTRACTING TITLE:")
        title = "Untitled"
        
        # First try to extract from page title (Poetry Daily specific)
        page_title_elem = soup.find('title')
        if page_title_elem:
            page_title = page_title_elem.get_text().strip()
            if ' – Poetry Daily' in page_title:
                title = page_title.replace(' – Poetry Daily', '').strip()
                print(f"  ✅ Found title from page title: {title}")
        
        # If that didn't work, try other selectors
        if title == "Untitled":
            title_selectors = [
                'h2',  # Poetry Daily uses h2 for poem titles
                'h1', 'h2.title', '.poem-title', '.title', 
                'h1.entry-title', 'h2.entry-title', '.post-title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    candidate_title = title_elem.get_text().strip()
                    # Skip generic titles
                    if candidate_title and candidate_title not in ['Featured Poet', 'Featured Translator', 'Receive POETRY DAILY']:
                        title = candidate_title
                        print(f"  ✅ Found title with '{selector}': {title}")
                        break
                    else:
                        print(f"  ⚠️  Skipped generic title with '{selector}': {candidate_title}")
                else:
                    print(f"  ❌ No title found with '{selector}'")
        
        # Extract author - try multiple selectors
        print("\n👤 EXTRACTING AUTHOR:")
        author = "Unknown"
        author_selectors = [
            '.daily_poem_author',  # Poetry Daily specific
            '.author', '.poet', '.byline', '.poem-author',
            'span.author', 'p.author', 'div.author',
            'a[href*="/poet"]', 'a[href*="/author"]'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                candidate_author = author_elem.get_text().strip()
                # Clean up author name
                candidate_author = re.sub(r'^(by\s+)', '', candidate_author, flags=re.IGNORECASE)
                candidate_author = re.sub(r'(,.*$)', '', candidate_author)
                # Skip non-author text
                if candidate_author and candidate_author not in ['Instagram', 'Facebook', 'Twitter']:
                    author = candidate_author
                    print(f"  ✅ Found author with '{selector}': {author}")
                    break
                else:
                    print(f"  ⚠️  Skipped non-author text with '{selector}': {candidate_author}")
            else:
                print(f"  ❌ No author found with '{selector}'")
        
        # If no author found, try text patterns
        if author == "Unknown":
            print("  🔍 Searching for author in text patterns...")
            text_content = soup.get_text()
            author_match = re.search(r'by\s+([^\n,]+)', text_content, re.IGNORECASE)
            if author_match:
                author = author_match.group(1).strip()
                print(f"  ✅ Found author in text: {author}")
        
        # Extract poem text - try multiple selectors
        print("\n📝 EXTRACTING POEM CONTENT:")
        poem_content = None
        poem_selectors = [
            '.elementor-widget-theme-post-content',  # Poetry Daily specific
            '.poem', '.poetry', '.poem-text', '.poem-content', 
            '.verse', 'pre.poem', '.entry-content', 
            'main', 'article', '.post-content'
        ]
        
        for selector in poem_selectors:
            content = soup.select_one(selector)
            if content:
                poem_content = content
                print(f"  ✅ Found content with '{selector}'")
                # Show first 200 chars of raw content
                raw_text = content.get_text()[:200]
                print(f"  📄 Raw content preview: {raw_text}...")
                break
            else:
                print(f"  ❌ No content found with '{selector}'")
        
        if not poem_content:
            print("❌ No poem content found at all!")
            return None
        
        # Extract and clean poem text
        print("\n🧹 CLEANING POEM TEXT:")
        poem_text = poem_content.get_text(separator='\n').strip()
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        print(f"  📊 Total lines before cleaning: {len(lines)}")
        print("  📄 First 10 lines before cleaning:")
        for i, line in enumerate(lines[:10]):
            print(f"    {i+1}: {line}")
        
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
            'www.', 'http', '.com', '.org'
        ]
        
        print("\n  🔍 Filtering lines:")
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check exclusion reasons
            excluded = False
            reason = ""
            
            if title.lower() in line_lower:
                excluded = True
                reason = "contains title"
            elif author.lower() in line_lower:
                excluded = True
                reason = "contains author"
            elif 'by ' in line_lower[:10]:
                excluded = True
                reason = "starts with 'by '"
            elif any(pattern in line_lower for pattern in exclude_patterns):
                excluded = True
                reason = "matches exclude pattern"
            elif len(line.strip()) <= 5:
                excluded = True
                reason = "too short"
            elif line.strip().startswith('(') and line.strip().endswith(')'):
                excluded = True
                reason = "parenthetical"
            elif '//' in line:
                excluded = True
                reason = "contains //"
            
            if excluded:
                print(f"    ❌ Line {i+1}: {line[:50]}... (EXCLUDED: {reason})")
            else:
                clean_lines.append(line)
                print(f"    ✅ Line {i+1}: {line[:50]}...")
        
        # Take first 20 lines of actual poem content
        poem_text = '\n'.join(clean_lines[:20])
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"  Clean lines count: {len(clean_lines)}")
        print(f"  Final poem text length: {len(poem_text)}")
        print(f"  Title: {title}")
        print(f"  Author: {author}")
        print(f"  Source: {source_name}")
        
        if len(poem_text) > 50 and len(clean_lines) >= 3:
            poem_data = {
                'title': title,
                'author': author,
                'text': poem_text,
                'source': source_name
            }
            
            # Test validation
            is_valid, message = validate_poem_content_debug(poem_data, url)
            
            if is_valid:
                print("✅ POEM EXTRACTION AND VALIDATION SUCCESSFUL")
                return poem_data
            else:
                print(f"❌ POEM VALIDATION FAILED: {message}")
                return None
        else:
            print("❌ POEM EXTRACTION FAILED - Insufficient content")
            return None
            
    except Exception as e:
        print(f"❌ Poem extraction failed for {url}: {e}")
        return None

def test_specific_urls():
    """Test specific URLs that have been problematic"""
    test_urls = [
        "https://theadroitjournal.org/2024/12/02/critical-essays-marie-howe-wins-the-2024-ruth-lilly-poetry-prize/",
        "https://poems.com/poem/the-guest-house/",
        "https://www.poetryfoundation.org/poems/46473/the-road-not-taken"
    ]
    
    for url in test_urls:
        poem = debug_poem_extraction(url)
        if poem:
            print(f"\n📝 EXTRACTED POEM:")
            print(f"Title: {poem['title']}")
            print(f"Author: {poem['author']}")
            print(f"Text preview: {poem['text'][:200]}...")
        print("\n" + "="*80 + "\n")

def test_poem_discovery():
    """Test the poem discovery system"""
    print("🔍 TESTING POEM DISCOVERY SYSTEM")
    print("=" * 80)
    
    # Test The Adroit Journal specifically
    domain = 'theadroitjournal.org'
    if domain in SITE_CONFIGS:
        config = SITE_CONFIGS[domain]
        print(f"Testing {config['name']} ({domain})")
        
        for base_url in config['base_urls']:
            print(f"\n📡 Discovering from: {base_url}")
            urls = get_poem_links(base_url, config)
            print(f"Found {len(urls)} URLs")
            
            # Test first few URLs
            for i, url in enumerate(urls[:3]):
                print(f"\n🧪 Testing URL {i+1}: {url}")
                poem = debug_poem_extraction(url, config['name'])
                if poem:
                    print("✅ Successfully extracted poem")
                else:
                    print("❌ Failed to extract poem")

if __name__ == "__main__":
    print("🤖 POETRY BOT EXTRACTION DEBUGGER")
    print("=" * 80)
    
    # Test specific problematic URLs
    test_specific_urls()
    
    # Test poem discovery system
    test_poem_discovery() 