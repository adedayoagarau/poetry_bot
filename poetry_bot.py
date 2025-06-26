#!/usr/bin/env python3
"""
Enhanced Poetry Bot with Improved Rotation and State Tracking
Fixes repetition issues by expanding discovery and tracking posted poems
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urlparse
from typing import List, Dict, Optional
import json
import os
from datetime import datetime, timedelta

# Import the discovery system
from poem_link_discovery import (
    discover_all_poem_links, 
    SITE_CONFIGS,
    batch_validate_urls,
    filter_high_quality_poems
)

class EnhancedPoetryBot:
    """Enhanced Poetry Bot with better rotation and state tracking"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0; +https://github.com/poetrybot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })
        
        # Enhanced caching with expiration
        self.discovered_urls = {}
        self.failed_urls = set()
        
        # State tracking files
        self.posted_poems_file = 'posted_poems.json'
        self.url_cache_file = 'url_cache.json'
        
        # Load state
        self.posted_poems = self.load_posted_poems()
        self.load_url_cache()
        
    def load_posted_poems(self) -> set:
        """Load history of posted poems to avoid duplicates"""
        try:
            if os.path.exists(self.posted_poems_file):
                with open(self.posted_poems_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('posted_urls', []))
            return set()
        except Exception as e:
            print(f"⚠️  Error loading posted poems: {e}")
            return set()
    
    def save_posted_poem(self, poem_data: dict):
        """Save a posted poem to avoid future duplicates"""
        try:
            self.posted_poems.add(poem_data['url'])
            
            # Load existing data
            posted_data = {'posted_urls': list(self.posted_poems), 'poems': []}
            if os.path.exists(self.posted_poems_file):
                with open(self.posted_poems_file, 'r') as f:
                    posted_data = json.load(f)
            
            # Add new poem with metadata
            posted_data['posted_urls'] = list(self.posted_poems)
            posted_data['poems'].append({
                'url': poem_data['url'],
                'title': poem_data['title'],
                'author': poem_data['author'],
                'source': poem_data['source'],
                'posted_at': datetime.now().isoformat()
            })
            
            # Keep only last 500 poems to prevent file bloat
            posted_data['poems'] = posted_data['poems'][-500:]
            
            with open(self.posted_poems_file, 'w') as f:
                json.dump(posted_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Error saving posted poem: {e}")
    
    def load_url_cache(self):
        """Load cached URLs with expiration check"""
        try:
            if os.path.exists(self.url_cache_file):
                with open(self.url_cache_file, 'r') as f:
                    cache_data = json.load(f)
                    
                current_time = datetime.now()
                
                # Filter out expired entries (older than 7 days)
                for domain, data in cache_data.items():
                    cached_time = datetime.fromisoformat(data.get('cached_at', '2020-01-01'))
                    if current_time - cached_time < timedelta(days=7):
                        self.discovered_urls[domain] = data['urls']
                    else:
                        print(f"🗑️  Expired cache for {domain}")
                        
        except Exception as e:
            print(f"⚠️  Error loading URL cache: {e}")
    
    def save_url_cache(self):
        """Save discovered URLs with timestamp"""
        try:
            cache_data = {}
            for domain, urls in self.discovered_urls.items():
                cache_data[domain] = {
                    'urls': urls,
                    'cached_at': datetime.now().isoformat()
                }
            
            with open(self.url_cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️  Error saving URL cache: {e}")

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
        
        # URL accessibility check
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
        
        # Structure analysis for poetry vs prose
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
        
        # Essay/review detection
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
        if essay_count >= 2:
            return False, f"Content appears to be essay/review about poetry ({essay_count} essay patterns found)"
        
        # Word count validation
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
    
    def discover_poems_from_source(self, domain, max_poems=70):  # MASSIVE INCREASE FOR VARIETY
        """Discover and extract poems from a specific domain with huge pool"""
        print(f"🔍 Discovering poems from {domain}...")
        
        # Check if we need to refresh the cache
        refresh_cache = False
        if domain not in self.discovered_urls:
            refresh_cache = True
        else:
            # Use cached URLs but consider refreshing if we've used too many
            cached_urls = self.discovered_urls[domain]
            unused_urls = [url for url in cached_urls if url not in self.posted_poems]
            if len(unused_urls) < 20:  # Refresh if less than 20 unused URLs (was 5)
                print(f"🔄 Refreshing cache for {domain} (only {len(unused_urls)} unused URLs)")
                refresh_cache = True
        
        if refresh_cache:
            # Discover even more URLs to support 70 poems per source
            urls = discover_all_poem_links(domain, max_links=200)  # INCREASED for 70 poems
            self.discovered_urls[domain] = urls
            self.save_url_cache()
        else:
            urls = self.discovered_urls[domain]
        
        # Filter out already posted URLs
        unused_urls = [url for url in urls if url not in self.posted_poems]
        
        if not unused_urls:
            print(f"⚠️  No unused URLs for {domain}, refreshing...")
            urls = discover_all_poem_links(domain, max_links=200)  # INCREASED for 70 poems
            self.discovered_urls[domain] = urls
            self.save_url_cache()
            unused_urls = [url for url in urls if url not in self.posted_poems]
        
        print(f"📊 {domain}: {len(unused_urls)} unused URLs available")
        
        # Randomize order to avoid always picking the same ones
        random.shuffle(unused_urls)
        
        poems = []
        for url in unused_urls:
            if len(poems) >= max_poems:
                break
                
            if url not in self.failed_urls:
                source_name = SITE_CONFIGS.get(domain, {}).get('name', domain)
                poem = self.extract_poem_from_url(url, source_name)
                if poem:
                    poems.append(poem)
                    print(f"✅ Extracted: {poem['title']} by {poem['author']}")
                
                # Be respectful with delays
                time.sleep(0.5)  # Reduced delay since we're doing more requests
        
        return poems
    
    def get_daily_poem(self):
        """Get a high-quality daily poem with better rotation"""
        print("🎯 Finding today's poem with improved rotation...")
        
        # Get all available domains and randomize order
        all_domains = list(SITE_CONFIGS.keys())
        random.shuffle(all_domains)
        
        # Try to get poems from multiple sources
        for domain in all_domains:
            poems = self.discover_poems_from_source(domain, max_poems=70)  # MASSIVE pool per source
            if poems:
                # Filter out already posted poems
                unposted_poems = [p for p in poems if p['url'] not in self.posted_poems]
                if unposted_poems:
                    selected_poem = random.choice(unposted_poems)
                    print(f"🎉 Selected poem from {selected_poem['source']}")
                    return selected_poem
        
        print("⚠️  All discovered poems have been posted. Trying fresh discovery...")
        
        # If all poems have been posted, clear some cache and try again
        priority_sources = ['poems.com', 'poetryfoundation.org', 'poets.org']
        for domain in priority_sources:
            if domain in self.discovered_urls:
                del self.discovered_urls[domain]  # Force fresh discovery
            
            poems = self.discover_poems_from_source(domain, max_poems=70)  # Maintain consistency
            if poems:
                return random.choice(poems)
        
        return None
    
    def run(self):
        """Main bot execution with state tracking"""
        try:
            poem = self.get_daily_poem()
            
            if poem:
                print("\n" + "="*50)
                print("📜 TODAY'S POEM")
                print("="*50)
                print(f"Title: {poem['title']}")
                print(f"Author: {poem['author']}")
                print(f"Source: {poem['source']}")
                print(f"URL: {poem['url']}")
                print("\n" + "-"*50)
                print(poem['text'])
                print("-"*50)
                
                # Save to posted history
                self.save_posted_poem(poem)
                print(f"💾 Saved to posted history ({len(self.posted_poems)} total posted)")
                
                return poem
            else:
                print("❌ No poem found today. Please try again later.")
                return None
                
        except Exception as e:
            print(f"❌ Bot execution failed: {e}")
            return None


class TwitterPoetryBot(EnhancedPoetryBot):
    """Twitter-specific enhanced poetry bot"""
    
    def post_poem(self, poem):
        """Post poem to Twitter using API v2 - 4-6 lines with link"""
        if not poem:
            return False
        
        # Create source hashtag
        source_hashtag = f"#{poem['source'].replace(' ', '').replace('.', '')}"
        
        # Extract 4-6 lines from the poem
        poem_lines = [line.strip() for line in poem['text'].split('\n') if line.strip()]
        
        # Select 4-6 lines (prefer 4-5 for better Twitter format)
        if len(poem_lines) >= 6:
            selected_lines = poem_lines[:5]  # Take first 5 lines
            has_more = True
        elif len(poem_lines) >= 4:
            selected_lines = poem_lines[:4]  # Take first 4 lines
            has_more = len(poem_lines) > 4
        else:
            selected_lines = poem_lines  # Use all available lines
            has_more = False
        
        # Join selected lines
        poem_excerpt = '\n'.join(selected_lines)
        
        # Add continuation indicator if there are more lines
        if has_more:
            poem_excerpt += '\n...'
        
        # Tweet format with link
        tweet_start = f'"{poem["title"]}" by {poem["author"]}\n\n'
        tweet_middle = f'{poem_excerpt}\n\n'
        
        # Add link to full poem
        read_more = f'Read full poem: {poem["url"]}\n\n'
        
        tweet_end = f'#Poetry #WritingCommunity {source_hashtag}'
        
        # Construct tweet
        tweet_text = f"{tweet_start}{tweet_middle}{read_more}{tweet_end}"
        
        # If still too long, remove some lines
        while len(tweet_text) > 280 and len(selected_lines) > 2:
            selected_lines = selected_lines[:-1]  # Remove last line
            poem_excerpt = '\n'.join(selected_lines)
            if has_more or len(poem_lines) > len(selected_lines):
                poem_excerpt += '\n...'
            tweet_middle = f'{poem_excerpt}\n\n'
            tweet_text = f"{tweet_start}{tweet_middle}{read_more}{tweet_end}"
        
        # Final length check and fallback
        if len(tweet_text) > 280:
            # Emergency fallback: just title, author, and link
            tweet_text = f'"{poem["title"]}" by {poem["author"]}\n\nRead full poem: {poem["url"]}\n\n#Poetry {source_hashtag}'
            
        print(f"📱 Posting to Twitter ({len(tweet_text)} chars):")
        print("-" * 50)
        print(tweet_text)
        print("-" * 50)
        print(f"📊 Excerpt: {len(selected_lines)} lines from {len(poem_lines)} total lines")
        
        # Twitter API posting code
        try:
            import tweepy
            import os
            
            # Get credentials
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                print("❌ Missing Twitter API credentials")
                return False
            
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )
            
            # Verify authentication
            me = client.get_me()
            print(f"✅ Authenticated as @{me.data.username}")
            
            # Post tweet
            response = client.create_tweet(text=tweet_text)
            tweet_id = response.data['id']
            print(f"🎉 Posted: https://twitter.com/{me.data.username}/status/{tweet_id}")
            
            return True
            
        except ImportError:
            print("❌ tweepy library not installed")
            return False
        except Exception as e:
            print(f"❌ Twitter error: {str(e)}")
            return False
    
    def run(self):
        """Enhanced Twitter bot execution"""
        poem = self.get_daily_poem()
        if poem:
            success = self.post_poem(poem)
            if success:
                # Save to posted history
                self.save_posted_poem(poem)
            return poem
        return None


if __name__ == "__main__":
    print("🤖 Enhanced Poetry Bot Starting...")
    bot = EnhancedPoetryBot()
    bot.run()