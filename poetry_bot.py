import os
import random
import requests
import tweepy
from datetime import datetime, timedelta
import openai
import google.generativeai as genai
import anthropic
from PIL import Image, ImageDraw, ImageFont
import textwrap
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
from config import *
from poem_link_discovery import get_poem_links, SITE_CONFIGS
from urllib.parse import urlparse
import re

# Load environment variables from .env file
load_dotenv()

class PoetryBot:
    def __init__(self):
        # Initialize Twitter API
        self.setup_twitter()
        
        # Initialize AI APIs
        self.setup_ai_apis()
        
        # Initialize Instagram
        self.setup_instagram()
        
        # Track daily posts to avoid duplicates
        self.daily_posts = {
            'authors': [],
            'sources': [],
            'poems_posted': [],
            'ai_posts_count': 0,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Cache discovered poem URLs to avoid repeated discovery
        self.poem_url_cache = {}
        
    def setup_twitter(self):
        """Set up Twitter API v2 connection"""
        try:
            # Use Twitter API v2 client (compatible with free tier)
            self.twitter_client = tweepy.Client(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
                wait_on_rate_limit=True
            )
            
            # Also keep v1.1 API for media upload if needed
            auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET')
            )
            auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_api = tweepy.API(auth)
            print("✅ Twitter API v2 connected successfully")
        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
            self.twitter_client = None
            self.twitter_api = None
            
    def setup_ai_apis(self):
        """Set up AI API connections"""
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            print("✅ OpenAI API connected")
        
        # Gemini
        if os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            print("✅ Gemini API connected")
            
        # Claude
        if os.getenv('CLAUDE_API_KEY'):
            self.claude_client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
            print("✅ Claude API connected")
        else:
            self.claude_client = None

    def setup_instagram(self):
        """Set up Instagram client"""
        try:
            from instagrapi import Client
            username = os.getenv('INSTAGRAM_USERNAME')
            password = os.getenv('INSTAGRAM_PASSWORD')
            if username and password:
                self.instagram = Client()
                self.instagram.login(username, password)
                print("✅ Instagram connected successfully")
            else:
                print("ℹ️ Instagram credentials not found, Instagram features disabled.")
                self.instagram = None
        except ImportError:
            print("⚠️ instagrapi library not found, Instagram features disabled.")
            self.instagram = None
        except Exception as e:
            print(f"❌ Instagram connection failed: {e}")
            self.instagram = None

    def check_daily_reset(self):
        """Reset daily tracking if it's a new day"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if self.daily_posts['date'] != current_date:
            self.daily_posts = {
                'authors': [],
                'sources': [],
                'poems_posted': [],
                'ai_posts_count': 0,
                'date': current_date
            }
            print(f"🔄 Reset for new day: {current_date}")

    def should_avoid_source(self, source_name):
        """Check if we should avoid this source for diversity"""
        if not BOT_SETTINGS.get('avoid_repeat_sources', True):
            return False
        return source_name in self.daily_posts['sources']

    def should_avoid_author(self, author_name):
        """Check if we should avoid this author for diversity"""
        if not BOT_SETTINGS.get('avoid_repeat_authors', True):
            return False
        return author_name in self.daily_posts['authors']

    def can_use_ai_generation(self):
        """Check if we can generate AI content based on daily limits"""
        max_ai_posts = BOT_SETTINGS.get('max_ai_posts_per_day', 1)
        return self.daily_posts['ai_posts_count'] < max_ai_posts

    def get_post_number_today(self):
        """Determine which post of the day this is"""
        return len(self.daily_posts['poems_posted']) + 1

    def get_poem_urls_for_domain(self, domain):
        """Get cached poem URLs for a domain or discover them"""
        if domain not in self.poem_url_cache:
            print(f"🔍 Discovering poem URLs for {domain}...")
            
            if domain in SITE_CONFIGS:
                config = SITE_CONFIGS[domain]
                all_urls = []
                
                # Try each base URL
                for base_url in config['base_urls']:
                    try:
                        urls = get_poem_links(base_url, config)
                        all_urls.extend(urls)
                    except Exception as e:
                        print(f"⚠️  Failed to discover from {base_url}: {e}")
                
                # Remove duplicates and cache
                unique_urls = list(set(all_urls))
                self.poem_url_cache[domain] = unique_urls
                print(f"✅ Cached {len(unique_urls)} poem URLs for {domain}")
            else:
                self.poem_url_cache[domain] = []
                print(f"⚠️  No configuration found for {domain}")
        
        return self.poem_url_cache[domain]

    def fetch_poem_from_journals(self):
        """Fetch a poem from curated literary journals using discovered URLs"""
        from config import get_weighted_journal_list
        
        # Get weighted list (preferred sources appear more frequently)  
        weighted_journals = get_weighted_journal_list()
        
        # Shuffle for true randomness
        random.shuffle(weighted_journals)
        
        # Try journals randomly, applying diversity filters
        for journal in weighted_journals:
            # Skip if we've already used this source today
            if self.should_avoid_source(journal['name']):
                continue
                
            try:
                print(f"🎲 Randomly selected: {journal['name']}")
                
                # Get domain from journal URL
                domain = urlparse(journal['url']).netloc
                
                # Get poem URLs for this domain
                poem_urls = self.get_poem_urls_for_domain(domain)
                
                if not poem_urls:
                    print(f"⚠️  No poem URLs found for {domain}")
                    continue
                
                # Try random poem URLs from this domain
                random.shuffle(poem_urls)
                
                for poem_url in poem_urls[:5]:  # Try up to 5 URLs
                    print(f"  📄 Trying poem at: {poem_url}")
                    poem = self.extract_poem_from_url(poem_url, journal['name'])
                    
                    if poem:
                        # Apply diversity filters (only if enabled)
                        if self.should_avoid_author(poem['author']):
                            print(f"⏭️  Skipping poem by {poem['author']} - author already featured today")
                            continue
                        
                        # Validate the poem content
                        is_valid, message = self.validate_poem_content(poem, poem_url)
                        if is_valid:
                            print(f"✅ Found valid poem from {journal['name']}")
                            # Track this selection
                            self.daily_posts['sources'].append(journal['name'])
                            self.daily_posts['authors'].append(poem['author'])
                            poem['url'] = poem_url  # Store the source URL
                            return poem
                        else:
                            print(f"⚠️  Poem from {journal['name']} failed validation: {message}")
                            continue
                
            except Exception as e:
                print(f"❌ {journal['name']} failed with error: {e}")
                continue
        
        print("📚 No valid poems found from literary journals")
        return None

    def extract_poem_from_url(self, url, source_name="Unknown"):
        """Extract poem content from a specific URL"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code} for {url}")
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title - try multiple selectors
            title = "Untitled"
            
            # First try to extract from page title (Poetry Daily specific)
            page_title_elem = soup.find('title')
            if page_title_elem:
                page_title = page_title_elem.get_text().strip()
                if ' – Poetry Daily' in page_title:
                    title = page_title.replace(' – Poetry Daily', '').strip()
            
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
                            break
            
            # Extract author - try multiple selectors
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
                        break
            
            # If no author found, try text patterns
            if author == "Unknown":
                text_content = soup.get_text()
                author_match = re.search(r'by\s+([^\n,]+)', text_content, re.IGNORECASE)
                if author_match:
                    author = author_match.group(1).strip()
            
            # Extract poem text - try multiple selectors
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
                    break
            
            if not poem_content:
                print(f"⚠️  No poem content found at {url}")
                return None
            
            # Extract and clean poem text
            poem_text = poem_content.get_text(separator='\n').strip()
            lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
            
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
                    '//' not in line):
                    clean_lines.append(line)
            
            # Take first 20 lines of actual poem content
            poem_text = '\n'.join(clean_lines[:20])
            
            if len(poem_text) > 50 and len(clean_lines) >= 3:
                return {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': source_name
                }
            
            print(f"⚠️  Insufficient poem content after cleaning from {url}")
            return None
            
        except Exception as e:
            print(f"❌ Poem extraction failed for {url}: {e}")
            return None

    def select_striking_lines(self, poem_text):
        """Select up to 4 most striking lines from a poem"""
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        if not lines:
            return poem_text[:100] + "..." if len(poem_text) > 100 else poem_text
        
        # If poem is very short (1-4 lines), use it all
        if len(lines) <= 4:
            return '\n'.join(lines)
        
        # Look for lines with striking imagery, emotion, or memorable phrases
        striking_indicators = [
            # Imagery words
            'light', 'shadow', 'moon', 'sun', 'star', 'ocean', 'fire', 'wind',
            'silence', 'whisper', 'thunder', 'rain', 'snow', 'flower', 'tree',
            # Emotional words  
            'love', 'heart', 'soul', 'dream', 'hope', 'fear', 'joy', 'pain',
            'remember', 'forget', 'lost', 'found', 'broken', 'whole',
            # Action/movement
            'dance', 'sing', 'fly', 'fall', 'rise', 'run', 'walk', 'breathe'
        ]
        
        scored_lines = []
        for i, line in enumerate(lines):
            score = 0
            line_lower = line.lower()
            
            # Score based on striking words
            for word in striking_indicators:
                if word in line_lower:
                    score += 1
            
            # Prefer lines that aren't too short or too long
            if 10 <= len(line) <= 100:
                score += 2
            
            # Prefer lines with interesting punctuation
            if any(char in line for char in '!?—;:'):
                score += 1
                
            # Avoid very generic or connecting lines
            generic_starters = ['and', 'but', 'the', 'it', 'this', 'that', 'or', 'if']
            if not any(line_lower.startswith(starter) for starter in generic_starters):
                score += 1
            
            scored_lines.append((score, i, line))
        
        # Sort by score and select best lines (up to 4)
        scored_lines.sort(reverse=True, key=lambda x: x[0])
        
        # Take up to 4 best lines, preferring consecutive ones when possible
        selected_lines = []
        used_indices = set()
        
        for score, index, line in scored_lines:
            if len(selected_lines) >= 4:
                break
            if index not in used_indices:
                selected_lines.append((index, line))
                used_indices.add(index)
        
        # Sort selected lines by their original order in the poem
        selected_lines.sort(key=lambda x: x[0])
        return '\n'.join([line[1] for line in selected_lines])

    def validate_poem_content(self, poem_data, url=None):
        """Validate that poem content is real and complete"""
        if not poem_data:
            return False, "No poem data provided"
        
        # Check required fields
        required_fields = ['title', 'author', 'text', 'source']
        for field in required_fields:
            if not poem_data.get(field):
                return False, f"Missing required field: {field}"
        
        # Validate poem text quality
        text = poem_data['text'].strip()
        title = poem_data['title'].strip()
        
        # Check minimum length (avoid fragments)
        if len(text) < 30:
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
                return False, f"Title indicates essay/review content: '{indicator}' in '{title}'"
        
        # Check that it looks like actual poetry (not just navigation text or prose)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if len(lines) < 2:
            return False, "Insufficient poem content (needs multiple lines)"
        
        # Avoid poems that are just titles/headers
        if all(len(line) < 10 for line in lines):
            return False, "Lines too short (likely navigation text)"
        
        # ENHANCED: Check for prose vs poetry indicators
        # Poetry typically has shorter lines, more line breaks, less dense text
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        long_lines = sum(1 for line in lines if len(line) > 100)
        very_long_lines = sum(1 for line in lines if len(line) > 200)
        
        # If most lines are very long, it's likely prose, not poetry
        if avg_line_length > 80 and long_lines > len(lines) * 0.7:
            return False, "Content appears to be prose, not poetry (long lines)"
        
        # If we have very long lines (200+ chars), it's almost certainly prose
        if very_long_lines > len(lines) * 0.3:
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
        
        # ENHANCED: Lower thresholds for stricter validation
        if prose_count >= 2:  # Reduced from 3
            return False, f"Content appears to be prose/essay about poetry, not actual poetry (prose indicators: {prose_count})"
        
        if nav_count >= 2:
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
        
        for line in lines:
            line_lower = line.lower()
            if any(pattern in line_lower for pattern in problematic_patterns):
                return False, f"Content contains essay/review pattern: {line[:50]}..."
        
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
                return False, f"Content starts like an essay: '{starter}'"
        
        # Additional check: if all lines look like titles (title case, short)
        title_like_lines = 0
        for line in lines:
            # Check if line looks like a title (mostly title case, reasonable length)
            words = line.split()
            if len(words) >= 2 and len(words) <= 8:  # Typical title length
                capitalized_words = sum(1 for word in words if word[0].isupper() and len(word) > 2)
                if capitalized_words >= len(words) * 0.7:  # Most words capitalized
                    title_like_lines += 1
        
        if title_like_lines >= len(lines) * 0.8:  # 80% of lines look like titles
            return False, "Content appears to be a list of titles, not actual poetry"
        
        # ENHANCED: Check for biographical/publication information
        bio_indicators = [
            'first book', 'second book', 'latest book', 'published in', 'appears in',
            'winner of', 'recipient of', 'teaches at', 'professor at', 'lives in',
            'born in', 'graduated from', 'mfa', 'phd', 'university', 'college',
            'press', 'publisher', 'publication', 'review', 'magazine', 'journal',
            'holds degrees', 'boston university', 'new and selected poems',
            'building the perfect animal', 'four way books', 'sixth book'
        ]
        
        bio_count = sum(1 for indicator in bio_indicators if indicator in text_lower)
        if bio_count >= 2:  # Reduced from 3
            return False, f"Content appears to be biographical/publication information, not actual poetry (bio indicators: {bio_count})"
        
        # Check if content looks like a book/publication description
        publication_phrases = [
            'first book', 'latest collection', 'new book', 'forthcoming',
            'new and selected', 'building the perfect', 'four way books',
            'copper canyon press', 'sixth book of poetry'
        ]
        
        for phrase in publication_phrases:
            if phrase in text_lower:
                return False, f"Content appears to be publication information: '{phrase}'"
        
        # ENHANCED: Check for reasonable title and author
        if len(title) > 100:
            return False, "Title too long (likely extracted wrong content)"
        
        author = poem_data['author'].strip()
        if author.lower() in ['unknown', 'anonymous', ''] and 'ai generated' not in poem_data['source'].lower():
            return False, "Missing author information"
        
        # ENHANCED: Check if content is too long to be a typical poem excerpt
        if len(text) > 2000:  # Most poems are shorter than this
            return False, "Content too long (likely essay or review, not poem)"
        
        # If URL provided, validate it exists and is accessible
        if url:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
                response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
                if response.status_code >= 400:
                    return False, f"URL not accessible: {response.status_code}"
            except Exception as e:
                return False, f"URL validation failed: {e}"
        
        return True, "Poem content validated successfully"

    def validate_tweet_content(self, tweet_text, poem_data, url=None):
        """Validate that tweet content is appropriate and complete"""
        if not tweet_text or len(tweet_text.strip()) < 20:
            return False, "Tweet text too short"
        
        if len(tweet_text) > 280:
            return False, "Tweet text too long for Twitter"
        
        # Ensure tweet contains actual poem content (more flexible check)
        poem_text = poem_data['text'].lower()
        tweet_lower = tweet_text.lower()
        
        # Check if any significant words from poem appear in tweet
        poem_words = [word.strip('.,!?;:"()[]') for word in poem_text.split() if len(word) > 3]
        significant_words = [word for word in poem_words if word not in ['the', 'and', 'but', 'for', 'with', 'from', 'that', 'this', 'they', 'have', 'been', 'were', 'said']]
        
        if significant_words:
            # Check ALL significant words, not just the first 5
            poem_content_found = any(word in tweet_lower for word in significant_words)
            if not poem_content_found:
                return False, "Tweet doesn't contain poem content"
        
        # If URL included, make sure it's valid
        if url and url in tweet_text:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
                response = requests.head(url, headers=headers, timeout=5)
                if response.status_code >= 400:
                    return False, f"Tweet contains broken URL: {response.status_code}"
            except:
                return False, "Tweet contains invalid URL"
        
        return True, "Tweet content validated successfully"

    def generate_ai_poem(self):
        """Generate a poem using AI APIs - equal opportunity themes"""
        if not self.can_use_ai_generation():
            print(f"⚠️  AI generation limit reached for today ({self.daily_posts['ai_posts_count']}/{BOT_SETTINGS.get('max_ai_posts_per_day', 1)})")
            return None
        
        # Random theme selection - all themes have equal opportunity
        theme = random.choice(POETRY_THEMES)
        
        # Simple, universal prompt
        prompt = f"Write a beautiful, evocative poem about {theme}. Keep it under 300 characters. Focus on striking imagery and memorable lines."
        
        # Try different AI services
        poem = None
        
        # Try Gemini first (free tier available)
        if os.getenv('GEMINI_API_KEY') and not poem:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                poem_text = response.text.strip()
                
                poem = {
                    'title': f"Inspired by {theme}",
                    'author': 'AI Generated',
                    'text': poem_text,
                    'source': 'Gemini AI'
                }
            except Exception as e:
                print(f"Gemini generation failed: {e}")
        
        # Try Claude
        if self.claude_client and not poem:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                poem_text = response.content[0].text.strip()
                
                poem = {
                    'title': f"Inspired by {theme}",
                    'author': 'AI Generated',
                    'text': poem_text,
                    'source': 'Claude AI'
                }
            except Exception as e:
                print(f"Claude generation failed: {e}")
        
        # Try OpenAI as fallback
        if os.getenv('OPENAI_API_KEY') and not poem:
            try:
                client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                poem_text = response.choices[0].message.content.strip()
                
                poem = {
                    'title': f"Inspired by {theme}",
                    'author': 'AI Generated',
                    'text': poem_text,
                    'source': 'OpenAI'
                }
            except Exception as e:
                print(f"OpenAI generation failed: {e}")
        
        if poem:
            # Track AI usage
            self.daily_posts['ai_posts_count'] += 1
            self.daily_posts['sources'].append(poem['source'])
        
        return poem

    def create_poem_image(self, poem):
        """Create a beautiful image with the poem text"""
        try:
            # Create image
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color=random.choice(IMAGE_COLORS['backgrounds']))
            draw = ImageDraw.Draw(img)
            
            # Try to load a nice font, fallback to default
            try:
                font_title = ImageFont.truetype("Arial.ttf", 24)
                font_text = ImageFont.truetype("Arial.ttf", 18)
                font_author = ImageFont.truetype("Arial.ttf", 16)
            except:
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
                font_author = ImageFont.load_default()
            
            # Prepare text
            title = poem['title'][:50]  # Limit title length
            author = f"— {poem['author']}"
            
            # Wrap poem text
            poem_lines = []
            for line in poem['text'].split('\n'):
                wrapped = textwrap.fill(line, width=40)
                poem_lines.extend(wrapped.split('\n'))
            
            # Limit to fit on image
            poem_lines = poem_lines[:15]
            
            # Calculate positions
            y_position = 50
            
            # Draw title
            title_bbox = draw.textbbox((0, 0), title, font=font_title)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text(((width - title_width) // 2, y_position), title, 
                     fill=random.choice(IMAGE_COLORS['text']), font=font_title)
            y_position += 60
            
            # Draw poem text
            for line in poem_lines:
                if line.strip():
                    line_bbox = draw.textbbox((0, 0), line, font=font_text)
                    line_width = line_bbox[2] - line_bbox[0]
                    draw.text(((width - line_width) // 2, y_position), line, 
                             fill=random.choice(IMAGE_COLORS['text']), font=font_text)
                y_position += 25
            
            # Draw author
            y_position += 30
            author_bbox = draw.textbbox((0, 0), author, font=font_author)
            author_width = author_bbox[2] - author_bbox[0]
            draw.text(((width - author_width) // 2, y_position), author, 
                     fill=random.choice(IMAGE_COLORS['text']), font=font_author)
            
            # Save image
            img_path = f"poem_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(img_path)
            return img_path
            
        except Exception as e:
            print(f"Image creation failed: {e}")
            return None

    def format_tweet_text(self, poem):
        """Format poem in exact format: "lines" - Author Name \n\n Read more: URL \n\n #WritingCommunity #PoetryCommunity"""
        # Extract up to 4 striking lines from the poem
        striking_lines = self.select_striking_lines(poem['text'])
        
        # Build the tweet components
        author = poem['author'][:50]  # Limit author length
        poem_url = poem.get('url', '')
        
        # Format exactly as requested:
        # "lines from the poem: at most 4 lines"
        # - Name of the author
        # 
        # Read more: Link to the poem
        # 
        # #WritingCommunity #PoetryCommunity
        
        # Put lines in quotes
        quoted_lines = f'"{striking_lines}"'
        
        # Author attribution
        attribution = f"- {author}"
        
        # Read more link (if available)
        if poem_url:
            read_more = f"Read more: {poem_url}"
        else:
            read_more = f"Source: {poem.get('source', 'Literary Journal')}"
        
        # Hashtags
        hashtags = "#WritingCommunity #PoetryCommunity"
        
        # Combine all parts with proper spacing
        tweet_text = f"{quoted_lines}\n{attribution}\n\n{read_more}\n\n{hashtags}"
        
        # Final length check - prioritize the poem content
        if len(tweet_text) > 280:
            # Try shorter lines if too long
            lines = striking_lines.split('\n')
            if len(lines) > 2:
                # Reduce to 2 lines if we have more
                shorter_lines = '\n'.join(lines[:2])
                quoted_lines = f'"{shorter_lines}"'
                tweet_text = f"{quoted_lines}\n{attribution}\n\n{read_more}\n\n{hashtags}"
                
                if len(tweet_text) > 280:
                    # Try just 1 line
                    single_line = lines[0]
                    quoted_lines = f'"{single_line}"'
                    tweet_text = f"{quoted_lines}\n{attribution}\n\n{read_more}\n\n{hashtags}"
        
        return tweet_text[:280]  # Final safety truncation

    def post_to_twitter(self, poem, image_path=None):
        """Post poem to Twitter using API v2 with validation"""
        if not hasattr(self, 'twitter_client') or not self.twitter_client:
            print("❌ Twitter API v2 not available")
            return False
            
        try:
            # Format the tweet
            tweet_text = self.format_tweet_text(poem)
            poem_url = poem.get('url')  # URL where poem was found
            
            # Validate tweet content before posting
            is_valid, message = self.validate_tweet_content(tweet_text, poem, poem_url)
            if not is_valid:
                print(f"❌ Tweet validation failed: {message}")
                return False
            
            print(f"📝 Tweet preview ({len(tweet_text)} chars):")
            print("-" * 50)
            print(tweet_text)
            print("-" * 50)
            
            # Post with image if available (v2 API)
            media_ids = None
            if image_path and os.path.exists(image_path) and self.twitter_api:
                try:
                    media = self.twitter_api.media_upload(image_path)
                    media_ids = [media.media_id]
                    print("✅ Image uploaded successfully")
                except Exception as e:
                    print(f"⚠️  Image upload failed, posting text only: {e}")
            
            # Post using Twitter API v2
            response = self.twitter_client.create_tweet(
                text=tweet_text,
                media_ids=media_ids
            )
            
            if response.data:
                tweet_id = response.data['id']
                if media_ids:
                    print(f"✅ Posted to Twitter with image: {tweet_id}")
                else:
                    print(f"✅ Posted to Twitter: {tweet_id}")
                return True
            else:
                print("❌ Tweet creation failed - no response data")
                return False
            
        except Exception as e:
            print(f"❌ Twitter posting failed: {e}")
            return False

    def create_instagram_image(self, poem):
        """Create Instagram-ready square image"""
        width, height = 1080, 1080
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        for y in range(height):
            ratio = y / height
            r = int(255 * (1 - ratio * 0.1))
            g = int(182 + (218 - 182) * ratio)
            b = int(193 + (185 - 193) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        y_pos = 200
        lines = poem['text'].split('\n')[:6]
        for line in lines:
            if line.strip():
                bbox = draw.textbbox((0, 0), line, font=font_large)
                text_width = bbox[2] - bbox[0]
                x_pos = (width - text_width) // 2
                draw.text((x_pos, y_pos), line, fill=(60, 60, 60), font=font_large)
                y_pos += 60
        author_text = f"— {poem['author']}"
        bbox = draw.textbbox((0, 0), author_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        x_pos = (width - text_width) // 2
        draw.text((x_pos, height - 200), author_text, fill=(100, 100, 100), font=font_small)
        img_path = f"insta_poem_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        img.save(img_path, 'JPEG', quality=95)
        return img_path

    def post_to_instagram(self, poem):
        """Post poem to Instagram"""
        if not hasattr(self, 'instagram') or not self.instagram:
            print("ℹ️ Instagram client not available or not configured. Skipping Instagram post.")
            return False
        try:
            img_path = self.create_instagram_image(poem)
            caption = f"'{poem['title']}' by {poem['author']}\n\n"
            caption += "What's your favorite line? 💭\n\n"
            caption += "#poetry #dailypoem #poetrycommunity #poetrylovers #instapoetry #writersofinstagram #poems #literature #poetrygram #poetryislife"
            media = self.instagram.photo_upload(img_path, caption)
            print(f"✅ Posted to Instagram successfully!")
            if os.path.exists(img_path):
                os.remove(img_path)
            return True
        except Exception as e:
            print(f"❌ Instagram posting failed: {e}")
            return False

    def run(self):
        """Main bot execution with random selection and excerpt posting"""
        print("🤖 Poetry Bot starting...")
        
        # Check if we need to reset daily tracking
        self.check_daily_reset()
        
        # Determine which post of the day this is
        post_number = self.get_post_number_today()
        total_posts = BOT_SETTINGS.get('posts_per_day', 2)
        
        print(f"📊 Starting post {post_number} of {total_posts} for today")
        print(f"🎲 Using random selection from {len(LITERARY_JOURNALS)} curated sources")
        print("🎯 Equal opportunity for all poets!")
        
        # Try to fetch a poem from curated literary journals (random selection)
        poem = self.fetch_poem_from_journals()
        
        # NO AI FALLBACK - Only real poems from literary journals
        if not poem:
            print("❌ Failed to get any valid poem from literary journals")
            print("🚫 AI generation is disabled - only real poems allowed")
            return False
            
        print(f"📝 Selected poem: '{poem['title']}' by {poem['author']}")
        print(f"📍 Source: {poem['source']}")
        if poem.get('url'):
            print(f"🔗 URL: {poem['url']}")
        
        # Show selected lines
        striking_lines = self.select_striking_lines(poem['text'])
        print(f"✨ Selected lines: {striking_lines}")
        
        # Add to daily tracking
        self.daily_posts['poems_posted'].append({
            'title': poem['title'],
            'author': poem['author'],
            'source': poem['source'],
            'timestamp': datetime.now().isoformat(),
            'post_number': post_number
        })
        
        # Skip image creation (we're focusing on text excerpts with links)
        image_path = None
        if BOT_SETTINGS.get('create_images', False):
            print("🖼️  Creating poem image...")
            image_path = self.create_poem_image(poem)
            if image_path:
                print(f"✅ Image created: {image_path}")
            else:
                print("⚠️  Image creation failed, will post text only")
        
        # Post to Twitter with validation
        print("🐦 Posting excerpt to Twitter...")
        success = self.post_to_twitter(poem, image_path)

        # Post to Instagram (guarded, so errors here do not affect Twitter)
        if hasattr(self, 'instagram') and self.instagram:
            try:
                print("📱 Posting to Instagram...")
                self.post_to_instagram(poem)
            except Exception as e:
                print(f"⚠️  Instagram posting failed, but Twitter post unaffected: {e}")
        else:
            print("ℹ️  Instagram not configured or skipped. Only Twitter posting performed.")
        
        # Clean up image file
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            print("🧹 Cleaned up image file")
            
        # Print daily summary
        self.print_daily_summary()
            
        if success:
            print(f"🎉 Poetry bot completed successfully! (Post {post_number}/{total_posts})")
            print(f"✨ Posted excerpt from '{poem['title']}' by {poem['author']} from {poem['source']}")
        else:
            print("❌ Poetry bot encountered errors during posting")
            
        return success

    def print_daily_summary(self):
        """Print summary of today's posting activity"""
        post_count = len(self.daily_posts['poems_posted'])
        target_posts = BOT_SETTINGS.get('posts_per_day', 2)
        
        print(f"\n📈 Daily Summary ({self.daily_posts['date']}):")
        print(f"   Posts completed: {post_count}/{target_posts}")
        print(f"   Sources used: {', '.join(set(self.daily_posts['sources']))}")
        authors_list = list(set(self.daily_posts['authors']))
        print(f"   Authors featured: {', '.join(authors_list[:3])}{'...' if len(authors_list) > 3 else ''}")
        print(f"   AI generations: {self.daily_posts['ai_posts_count']}/{BOT_SETTINGS.get('max_ai_posts_per_day', 1)}")
        print(f"   🎲 Selection method: Random (equal opportunity)")
        print(f"   📝 Format: Poetry excerpts with links")
        
        remaining_posts = target_posts - post_count
        if remaining_posts > 0:
            next_times = BOT_SETTINGS.get('post_times_utc', ['09:00', '21:00'])
            if post_count < len(next_times):
                print(f"   Next post scheduled: {next_times[post_count]} UTC")
        else:
            print("   ✅ All posts completed for today!")
        print()

if __name__ == "__main__":
    bot = PoetryBot()
    bot.run()