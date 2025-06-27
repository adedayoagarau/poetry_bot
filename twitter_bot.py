#!/usr/bin/env python3
"""
Punchy Twitter Poetry Bot - Clean Format with Best 4 Lines
Title — Author Name + 4 punchiest consecutive lines
"""

import os
import re
from poetry_bot import TwitterPoetryBot
from bs4 import BeautifulSoup

class PunchyTwitterPoetryBot(TwitterPoetryBot):
    """Twitter bot that finds the punchiest 4 consecutive lines"""
    
    def extract_poem_from_url(self, url, source_name="Unknown"):
        """Enhanced extraction with better author detection"""
        if url in self.failed_urls:
            return None
            
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code != 200:
                self.failed_urls.add(url)
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements first
            unwanted_selectors = [
                '.date', '.posted-on', '.entry-meta', '.meta-data', '.byline-date',
                '.breadcrumb', '.navigation', '.nav', '.menu', '.header', '.footer',
                '.social-share', '.tags', '.categories', '.comments', '.related-posts',
                'time', '[datetime]', '.timestamp', '.copyright', '.newsletter'
            ]
            
            for selector in unwanted_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Better title extraction
            title = self.extract_better_title(soup, url)
            
            # Better author extraction
            author = self.extract_better_author(soup, url)
            
            # Clean poem text extraction
            poem_text = self.extract_clean_poem_text(soup)
            
            if poem_text and len(poem_text) > 50:
                poem_data = {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': source_name,
                    'url': url
                }
                
                is_valid, message = self.validate_poem_content(poem_data, url)
                if is_valid:
                    return poem_data
                else:
                    self.failed_urls.add(url)
                    return None
            else:
                self.failed_urls.add(url)
                return None
                
        except Exception as e:
            print(f"❌ Extraction failed for {url}: {e}")
            self.failed_urls.add(url)
            return None
    
    def extract_better_title(self, soup, url):
        """Enhanced title extraction with site-specific logic"""
        title = "Untitled"
        
        # Try page title first
        page_title_elem = soup.find('title')
        if page_title_elem:
            page_title = page_title_elem.get_text().strip()
            
            # Site-specific cleaning
            if 'poetryfoundation.org' in url:
                title = page_title.replace(' by ', ' | ').split(' | ')[0].strip()
            elif 'poets.org' in url:
                title = page_title.replace(' | Academy of American Poets', '').strip()
            elif 'poetrydaily.org' in url:
                title = page_title.replace(' – Poetry Daily', '').strip()
            else:
                # Generic cleaning
                suffixes = [' – Poetry Daily', ' | Poetry Foundation', ' | poets.org', ' - The New Yorker']
                for suffix in suffixes:
                    if suffix in page_title:
                        title = page_title.replace(suffix, '').strip()
                        break
                else:
                    if ' | ' in page_title:
                        title = page_title.split(' | ')[0].strip()
        
        # Try h1, h2 if title is still generic
        if title in ["Untitled", ""] or len(title) < 3:
            for selector in ['h1', 'h2', '.poem-title', '.title', '.entry-title']:
                elem = soup.select_one(selector)
                if elem:
                    candidate = elem.get_text().strip()
                    if candidate and len(candidate) > 3:
                        title = candidate
                        break
        
        # Remove dates from title
        title = re.sub(r'\d{1,2}/\d{1,2}/\d{4}', '', title)
        title = re.sub(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title if title else "Untitled"
    
    def extract_better_author(self, soup, url):
        """Enhanced author extraction with multiple strategies"""
        author = "Unknown"
        
        # Strategy 1: Look for common author selectors
        author_selectors = [
            '.daily_poem_author', '.c-feature-sub', '.author', '.poet', 
            '.byline', '.poem-author', 'span.author', 'p.author',
            '.entry-author', '.post-author', 'h3', 'h4'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                candidate = author_elem.get_text().strip()
                # Clean author name
                candidate = re.sub(r'^(by\s+)', '', candidate, flags=re.IGNORECASE)
                candidate = re.sub(r'(,.*$)', '', candidate)
                candidate = re.sub(r'\d{4}[-–]\d{4}', '', candidate)
                candidate = re.sub(r'\(\d{4}[-–]?\d{0,4}\)', '', candidate)
                candidate = re.sub(r'\s+', ' ', candidate).strip()
                
                if candidate and len(candidate) > 2 and candidate not in ['Instagram', 'Facebook', 'Twitter', 'Home', 'About']:
                    author = candidate
                    break
        
        # Strategy 2: Look in page title for "by Author"
        if author == "Unknown":
            page_title = soup.find('title')
            if page_title:
                title_text = page_title.get_text()
                by_match = re.search(r'\bby\s+([^|–-]+)', title_text, re.IGNORECASE)
                if by_match:
                    candidate = by_match.group(1).strip()
                    if len(candidate) > 2:
                        author = candidate
        
        # Strategy 3: Look for author links
        if author == "Unknown":
            author_links = soup.find_all('a', href=re.compile(r'/(author|poet|writer)/', re.IGNORECASE))
            for link in author_links:
                candidate = link.get_text().strip()
                if candidate and len(candidate) > 2:
                    author = candidate
                    break
        
        return author
    
    def extract_clean_poem_text(self, soup):
        """Extract clean poem text"""
        poem_selectors = [
            '.elementor-widget-theme-post-content', '.c-feature-bd',
            '.poem', '.poetry', '.poem-text', '.entry-content', 
            'main', 'article', '.post-content'
        ]
        
        poem_content = None
        for selector in poem_selectors:
            content = soup.select_one(selector)
            if content:
                poem_content = content
                break
        
        if not poem_content:
            return None
        
        poem_text = poem_content.get_text(separator='\n').strip()
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        # Aggressive filtering
        clean_lines = []
        exclude_patterns = [
            'subscribe', 'newsletter', 'posted on', 'published', 'updated',
            'read more', 'www.', 'http', '.com', 'copyright', 'share this',
            'about', 'contact', 'menu', 'navigation'
        ]
        
        for line in lines:
            line_lower = line.lower()
            
            # Skip dates
            if re.search(r'\d{1,2}/\d{1,2}/\d{4}', line):
                continue
            if re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', line):
                continue
            
            # Skip unwanted content
            if (any(pattern in line_lower for pattern in exclude_patterns) or
                len(line.strip()) <= 3 or
                '//' in line):
                continue
                
            clean_lines.append(line)
        
        return '\n'.join(clean_lines[:20])  # Keep more lines for selection
    
    def find_punchiest_4_lines(self, poem_text):
        """Find the most impactful 4 consecutive lines"""
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        if len(lines) <= 4:
            return lines
        
        # Score each possible 4-line segment
        best_score = 0
        best_segment = lines[:4]
        
        for i in range(len(lines) - 3):
            segment = lines[i:i+4]
            score = self.score_poem_segment(segment)
            
            if score > best_score:
                best_score = score
                best_segment = segment
        
        return best_segment
    
    def score_poem_segment(self, lines):
        """Score a 4-line segment for impact/interest"""
        score = 0
        text = ' '.join(lines).lower()
        
        # Positive indicators (punch/impact)
        impact_words = [
            'blood', 'heart', 'fire', 'dark', 'light', 'death', 'love', 'pain',
            'break', 'burn', 'fall', 'rise', 'scream', 'whisper', 'dream',
            'shadow', 'moon', 'sun', 'star', 'ocean', 'mountain', 'storm',
            'kiss', 'touch', 'hold', 'lost', 'found', 'wild', 'fierce',
            'beautiful', 'terrible', 'ancient', 'forever', 'never'
        ]
        
        for word in impact_words:
            if word in text:
                score += 2
        
        # Favor lines with good imagery/metaphor indicators
        imagery_indicators = ['like', 'as if', 'becomes', 'turns into', 'transforms']
        for indicator in imagery_indicators:
            if indicator in text:
                score += 3
        
        # Favor emotional content
        emotional_words = ['feel', 'remember', 'forget', 'hope', 'fear', 'wish', 'want', 'need']
        for word in emotional_words:
            if word in text:
                score += 1
        
        # Penalize overly abstract or boring content
        boring_indicators = ['the', 'and', 'but', 'or', 'so', 'then', 'when', 'where']
        boring_count = sum(1 for word in boring_indicators if text.count(word) > 2)
        score -= boring_count
        
        # Favor shorter, punchier lines
        avg_line_length = sum(len(line) for line in lines) / len(lines)
        if avg_line_length < 50:  # Shorter lines often more impactful
            score += 2
        
        # Favor segments with varied line lengths (more dynamic)
        line_lengths = [len(line) for line in lines]
        if max(line_lengths) - min(line_lengths) > 20:
            score += 1
        
        return score
    
    def post_poem(self, poem):
        """Create clean, punchy tweet format"""
        if not poem:
            return False
        
        # Get the punchiest 4 lines
        punchy_lines = self.find_punchiest_4_lines(poem['text'])
        
        # Simple, clean format: Title — Author Name
        header = f"{poem['title']} — {poem['author']}"
        
        # Join the 4 lines
        poem_excerpt = '\n'.join(punchy_lines)
        
        # Create tweet
        tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # If too long, try shorter title
        if len(tweet_text) > 280:
            # Try just first word of title if it's long
            words = poem['title'].split()
            if len(words) > 3:
                short_title = ' '.join(words[:2]) + '...'
                header = f"{short_title} — {poem['author']}"
                tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # If still too long, take only 3 lines
        if len(tweet_text) > 280:
            poem_excerpt = '\n'.join(punchy_lines[:3])
            tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # Final fallback
        if len(tweet_text) > 280:
            tweet_text = f"{poem['title']} — {poem['author']}\n\n{punchy_lines[0]}\n{punchy_lines[1]}\n\n#Poetry"
        
        print(f"📱 PUNCHY TWEET ({len(tweet_text)} chars):")
        print("=" * 60)
        print(tweet_text)
        print("=" * 60)
        print(f"🎯 Selected lines {punchy_lines}")
        
        # Twitter API code (same as before)
        try:
            import tweepy
            
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                print("❌ Missing Twitter API credentials - showing preview only")
                return True
            
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )
            
            response = client.create_tweet(text=tweet_text)
            print(f"🎉 Posted successfully!")
            return True
            
        except ImportError:
            print("❌ tweepy library not installed - showing preview only")
            return True
        except Exception as e:
            print(f"❌ Twitter error: {str(e)}")
            return False


if __name__ == "__main__":
    print("🎯 Punchy Twitter Poetry Bot starting...")
    bot = PunchyTwitterPoetryBot()
    result = bot.run()
    if result:
        print("✅ Punchy Twitter Poetry Bot finished successfully!")
    else:
        print("❌ No poem found today")