#!/usr/bin/env python3
"""
Complete Poetry Bot with Integrated Discovery System
Finds and extracts high-quality poems from 120+ sources
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlparse
from typing import List, Dict, Optional
import json

# Import the discovery system
from poem_link_discovery import (
    discover_all_poem_links, 
    SITE_CONFIGS,
    batch_validate_urls,
    filter_high_quality_poems
)

class PoetryBot:
    """Main Poetry Bot with discovery and extraction capabilities"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0; +https://github.com/poetrybot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })
        
        # Cache for discovered URLs
        self.discovered_urls = {}
        self.failed_urls = set()
        
    def validate_poem_content(self, poem_data, url=None):
        """Enhanced validation that poem content is real and complete"""
        if not poem_data:
            return False, "No poem data provided"
        
        # Check required fields
        required_fields = ['title', 'author', 'text', 'source']
        for field in required_fields:
            if not poem_data.get(field):
                return False, f"Missing required field: {field}"
        
        text = poem_data['text'].strip()
        title = poem_data['title'].strip()
        
        # ENHANCED: URL accessibility check
        if url:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
                response = self.session.head(url, headers=headers, timeout=5, allow_redirects=True)
                if response.status_code >= 400:
                    return False, f"URL not accessible: HTTP {response.status_code}"
            except Exception as e:
                return False, f"URL validation failed: {e}"
        
        # Basic length checks
        if len(text) < 30:
            return False, "Poem text too short (likely incomplete)"
        
        if len(text) > 3000:
            return False, "Content too long (likely essay, not poem)"
        
        # ENHANCED: Structure analysis for poetry vs prose
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if len(lines) < 2:
            return False, "Insufficient poem content (needs multiple lines)"
        
        # Check average line length (prose has much longer lines)
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        long_lines = sum(1 for line in lines if len(line) > 120)
        very_long_lines = sum(1 for line in lines if len(line) > 200)
        
        # If most lines are very long, it's likely prose
        if avg_line_length > 100 and long_lines > len(lines) * 0.6:
            return False, "Content appears to be prose, not poetry (very long lines)"
        
        if very_long_lines > len(lines) * 0.3:
            return False, "Content contains prose paragraphs, not poetry lines"
        
        # ENHANCED: Essay/review detection (much more comprehensive)
        text_lower = text.lower()
        title_lower = title.lower()
        
        # Strong essay indicators
        essay_patterns = [
            'in this essay', 'the author argues', 'according to', 'furthermore',
            'in conclusion', 'to summarize', 'for example', 'such as',
            'the collection', 'the poet writes', 'as mentioned earlier',
            'drawing on', 'in fiction', 'in poetry', 'the speaker',
            'voice is', 'equally accessible', 'compelling', 'transformation needs',
            'slow build-up', 'can be transformative', 'leaves us with',
            'american poetry landscape', 'increasingly dominated',
            'instagramable verse', 'present-day politics',
            'refreshing return', 'lyric poetry', 'opening poem',
            'intersection of myth', 'human body', 'covers a range of themes',
            'most compelling when writing', 'drawing from the wells',
            'storytelling and science', 'guided me while writing',
            'full-length poetry collection', 'chronicle of drifting'
        ]
        
        essay_count = sum(1 for pattern in essay_patterns if pattern in text_lower)
        if essay_count >= 2:  # Lowered threshold for stricter validation
            return False, f"Content appears to be essay/review about poetry ({essay_count} essay patterns found)"
        
        # ENHANCED: Title analysis for non-poetry content
        problematic_titles = [
            'review of', 'essay', 'interview', 'conversation with', 'profile',
            'announcement', 'winner', 'prize', 'award', 'selected poems',
            'new and selected', 'biography', 'memoir', 'critical essay',
            'marie howe', 'ruth lilly', 'building the perfect',
            'poetry and lightness', 'lightness', 'six memos',
            'calvino', 'italo calvino', 'craft essay', 'poetics'
        ]
        
        for indicator in problematic_titles:
            if indicator in title_lower:
                return False, f"Title indicates non-poem content: '{indicator}' in '{title}'"
        
        # ENHANCED: Navigation/metadata detection
        nav_patterns = [
            'table of contents', 'contents', 'browse', 'archive', 'search results',
            'subscription', 'newsletter', 'featured', 'latest', 'recent',
            'shortlist', 'issue', 'volume', 'submissions', 'contest',
            'author index', 'title index', 'editorial board',
            'macarthur', 'national book award', 'poet laureate', 'pulitzer prize'
        ]
        
        nav_count = sum(1 for pattern in nav_patterns if pattern in text_lower)
        if nav_count >= 2:
            return False, "Content appears to be navigation/metadata, not actual poetry"
        
        # ENHANCED: Biographical content detection
        bio_patterns = [
            'first book', 'second book', 'latest book', 'published in', 'appears in',
            'winner of', 'recipient of', 'teaches at', 'professor at', 'lives in',
            'born in', 'graduated from', 'mfa', 'phd', 'university', 'college',
            'press', 'publisher', 'publication', 'four way books', 'copper canyon'
        ]
        
        bio_count = sum(1 for pattern in bio_patterns if pattern in text_lower)
        if bio_count >= 3:
            return False, f"Content appears to be biographical information ({bio_count} bio indicators)"
        
        # ENHANCED: Check for error pages
        error_patterns = [
            'page not found', '404', 'error', 'access denied',
            'subscription required', 'login required', 'not available',
            'coming soon', 'under construction', 'temporarily unavailable'
        ]
        
        for pattern in error_patterns:
            if pattern in text_lower:
                return False, f"Content contains error pattern: {pattern}"
        
        # ENHANCED: Publication/book description detection
        publication_phrases = [
            'first book', 'latest collection', 'new book', 'forthcoming',
            'new and selected', 'building the perfect', 'four way books',
            'copper canyon press', 'sixth book of poetry', 'chronicle of drifting'
        ]
        
        for phrase in publication_phrases:
            if phrase in text_lower:
                return False, f"Content appears to be publication description: '{phrase}'"
        
        # ENHANCED: Check for reasonable title and author
        if len(title) > 100:
            return False, "Title too long (likely extracted wrong content)"
        
        author = poem_data['author'].strip()
        if author.lower() in ['unknown', 'anonymous', ''] and 'ai generated' not in poem_data['source'].lower():
            return False, "Missing author information"
        
        # ENHANCED: Word count validation (more specific ranges)
        word_count = len(text.split())
        if word_count < 20:
            return False, f"Too short ({word_count} words) - likely incomplete"
        elif word_count > 800:
            return False, f"Too long ({word_count} words) - likely essay or multiple poems"
        
        return True, "Poem content validated successfully"
    
    def extract_poem_from_url(self, url, source_name="Unknown"):
        """Extract poem from any supported URL"""
        if url in self.failed_urls:
            return None
            
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                self.failed_urls.add(url)
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = "Untitled"
            
            # Try page title first (Poetry Daily specific)
            page_title_elem = soup.find('title')
            if page_title_elem:
                page_title = page_title_elem.get_text().strip()
                if ' – Poetry Daily' in page_title:
                    title = page_title.replace(' – Poetry Daily', '').strip()
                elif ' | Poetry Foundation' in page_title:
                    title = page_title.replace(' | Poetry Foundation', '').strip()
                elif ' | ' in page_title:
                    title = page_title.split(' | ')[0].strip()
            
            # If that didn't work, try other selectors
            if title == "Untitled":
                title_selectors = [
                    'h2', 'h1', 'h2.title', '.poem-title', '.title', 
                    'h1.entry-title', 'h2.entry-title', '.post-title',
                    '.c-feature-hd', '.c-feature-title'
                ]
                
                for selector in title_selectors:
                    title_elem = soup.select_one(selector)
                    if title_elem:
                        candidate_title = title_elem.get_text().strip()
                        if candidate_title and candidate_title not in ['Featured Poet', 'Featured Translator', 'Receive POETRY DAILY']:
                            title = candidate_title
                            break
            
            # Extract author
            author = "Unknown"
            author_selectors = [
                '.daily_poem_author',  # Poetry Daily
                '.c-feature-sub',      # Poetry Foundation
                '.author', '.poet', '.byline', '.poem-author',
                'span.author', 'p.author', 'div.author',
                'a[href*="/poet"]', 'a[href*="/author"]'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    candidate_author = author_elem.get_text().strip()
                    candidate_author = re.sub(r'^(by\s+)', '', candidate_author, flags=re.IGNORECASE)
                    candidate_author = re.sub(r'(,.*$)', '', candidate_author)
                    # Fix double spaces
                    candidate_author = re.sub(r'\s+', ' ', candidate_author)
                    if candidate_author and candidate_author not in ['Instagram', 'Facebook', 'Twitter']:
                        author = candidate_author
                        break
            
            # Extract poem content
            poem_content = None
            poem_selectors = [
                '.elementor-widget-theme-post-content',  # Poetry Daily
                '.c-feature-bd',                          # Poetry Foundation
                '.poem', '.poetry', '.poem-text', '.poem-content', 
                '.verse', 'pre.poem', '.entry-content', 
                'main', 'article', '.post-content'
            ]
            
            for selector in poem_selectors:
                content = soup.select_one(selector)
                if content:
                    poem_content = content
                    break
            
            if not poem_content:
                self.failed_urls.add(url)
                return None
            
            # Clean poem text
            poem_text = poem_content.get_text(separator='\n').strip()
            lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
            
            # Filter out non-poem lines
            clean_lines = []
            exclude_patterns = [
                'subscribe', 'newsletter', 'archive', 'browse', 'search',
                'about', 'contact', 'home', 'menu', 'navigation',
                'read more', 'continue reading', 'full text',
                'print issues', 'buy now', 'purchase', 'add to cart',
                'interviews', 'reviews', 'submissions', 'guidelines',
                'www.', 'http', '.com', '.org'
            ]
            
            for line in lines:
                line_lower = line.lower()
                
                # Skip lines that contain title, author, or navigation
                if (title.lower() in line_lower or 
                    author.lower() in line_lower or
                    'by ' in line_lower[:10] or
                    any(pattern in line_lower for pattern in exclude_patterns) or
                    len(line.strip()) <= 5 or
                    (line.strip().startswith('(') and line.strip().endswith(')')) or
                    '//' in line):
                    continue
                    
                clean_lines.append(line)
            
            # Take first 20 lines of actual poem content
            poem_text = '\n'.join(clean_lines[:20])
            
            if len(poem_text) > 50 and len(clean_lines) >= 3:
                poem_data = {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': source_name,
                    'url': url
                }
                
                # Validate the extracted poem
                is_valid, message = self.validate_poem_content(poem_data, url)
                
                if is_valid:
                    return poem_data
                else:
                    print(f"❌ Validation failed for {url}: {message}")
                    self.failed_urls.add(url)
                    return None
            else:
                self.failed_urls.add(url)
                return None
                
        except Exception as e:
            print(f"❌ Extraction failed for {url}: {e}")
            self.failed_urls.add(url)
            return None
    
    def discover_poems_from_source(self, domain, max_poems=10):
        """Discover and extract poems from a specific domain"""
        print(f"🔍 Discovering poems from {domain}...")
        
        if domain in self.discovered_urls:
            urls = self.discovered_urls[domain]
        else:
            urls = discover_all_poem_links(domain, max_links=50)
            self.discovered_urls[domain] = urls
        
        poems = []
        for url in urls:
            if len(poems) >= max_poems:
                break
                
            if url not in self.failed_urls:
                source_name = SITE_CONFIGS.get(domain, {}).get('name', domain)
                poem = self.extract_poem_from_url(url, source_name)
                if poem:
                    poems.append(poem)
                    print(f"✅ Extracted: {poem['title']} by {poem['author']}")
                
                # Be respectful with delays
                time.sleep(1)
        
        return poems
    
    def get_daily_poem(self):
        """Get a high-quality daily poem from multiple sources"""
        print("🎯 Finding today's poem...")
        
        # Prioritized sources (best first)
        priority_sources = [
            'poems.com',           # Poetry Daily
            'poetryfoundation.org', # Poetry Foundation  
            'poets.org',           # Academy of American Poets
            'versedaily.org',      # Verse Daily
            'poetrymagazine.org'   # Poetry Magazine
        ]
        
        for domain in priority_sources:
            if domain in SITE_CONFIGS:
                poems = self.discover_poems_from_source(domain, max_poems=3)
                if poems:
                    # Return the first valid poem found
                    return random.choice(poems)
        
        # If priority sources fail, try other sources
        print("🔄 Trying backup sources...")
        backup_sources = [k for k in SITE_CONFIGS.keys() if k not in priority_sources]
        
        for domain in random.sample(backup_sources, min(5, len(backup_sources))):
            poems = self.discover_poems_from_source(domain, max_poems=2)
            if poems:
                return random.choice(poems)
        
        return None
    
    def run(self):
        """Main bot execution - get and display a poem"""
        try:
            poem = self.get_daily_poem()
            
            if poem:
                print("\n" + "="*50)
                print("📜 TODAY'S POEM")
                print("="*50)
                print(f"Title: {poem['title']}")
                print(f"Author: {poem['author']}")
                print(f"Source: {poem['source']}")
                print("\n" + "-"*50)
                print(poem['text'])
                print("-"*50)
                return poem
            else:
                print("❌ No poem found today. Please try again later.")
                return None
                
        except Exception as e:
            print(f"❌ Bot execution failed: {e}")
            return None

# Legacy support for Twitter bot
class TwitterPoetryBot(PoetryBot):
    """Twitter-specific poetry bot (extends main bot)"""
    
    def post_poem(self, poem):
        """Post poem to Twitter with elegant formatting - LIVE POSTING"""
        if not poem:
            return False
        
        # Create source hashtag (remove spaces and dots)
        source_hashtag = f"#{poem['source'].replace(' ', '').replace('.', '')}"
        
        # Base tweet format
        tweet_start = f'"{poem["title"]}" by {poem["author"]}\n\n'
        tweet_end = f'\n\n#Poetry #WritingCommunity {source_hashtag}'
        
        # Calculate available space for poem text
        base_length = len(tweet_start) + len(tweet_end)
        max_poem_length = 280 - base_length - 5  # Leave some buffer
        
        # Truncate poem if needed
        if len(poem['text']) > max_poem_length:
            poem_text = poem['text'][:max_poem_length].rstrip() + "..."
        else:
            poem_text = poem['text']
        
        # Construct final tweet
        tweet_text = f"{tweet_start}{poem_text}{tweet_end}"
        
        print(f"📱 Posting to Twitter LIVE ({len(tweet_text)} chars):")
        print("-" * 50)
        print(tweet_text)
        print("-" * 50)
        
        # LIVE TWITTER POSTING
        try:
            import tweepy
            import os
            
            # Get Twitter API credentials from environment
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                print("❌ Missing Twitter API credentials in environment variables")
                return False
            
            # Authenticate with Twitter
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            
            # Verify authentication
            try:
                api.verify_credentials()
                print("✅ Twitter authentication successful")
            except:
                print("❌ Twitter authentication failed")
                return False
            
            # Post the tweet
            response = api.update_status(tweet_text)
            print(f"🎉 SUCCESS! Posted to Twitter: https://twitter.com/user/status/{response.id}")
            return True
            
        except ImportError:
            print("❌ tweepy library not installed")
            return False
        except Exception as e:
            print(f"❌ Error posting to Twitter: {str(e)}")
            return False
    
    def run(self):
        """Twitter bot execution"""
        poem = self.get_daily_poem()
        if poem:
            self.post_poem(poem)
            return poem
        return None

if __name__ == "__main__":
    print("🤖 Poetry Bot Starting...")
    bot = PoetryBot()
    bot.run()