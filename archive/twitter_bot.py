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
    
    def is_actually_a_poem(self, text, title=""):
        """Validate that extracted content is actually a poem, not prose/essay"""
        if not text or len(text.strip()) < 20:
            return False, "Content too short"
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if len(lines) < 3:
            return False, "Too few lines for a poem"
        
        # Calculate line statistics
        line_lengths = [len(line) for line in lines]
        avg_line_length = sum(line_lengths) / len(line_lengths)
        max_line_length = max(line_lengths)
        
        # Check for prose indicators (very long lines)
        very_long_lines = sum(1 for length in line_lengths if length > 120)
        if very_long_lines > len(lines) * 0.4:
            return False, "Too many long lines - likely prose"
        
        # Check average line length (poems usually shorter)
        if avg_line_length > 80:
            return False, f"Average line too long ({avg_line_length}) - likely prose"
        
        # Check for essay/review patterns
        text_lower = text.lower()
        title_lower = title.lower()
        
        # Strong essay/review indicators
        essay_patterns = [
            'in this essay', 'the author argues', 'according to', 'furthermore',
            'in conclusion', 'to summarize', 'for example', 'such as',
            'the collection', 'the poet writes', 'as mentioned earlier',
            'this book', 'this volume', 'the work', 'the reader',
            'published by', 'press', 'university', 'copyright',
            'review', 'analysis', 'critique', 'examination',
            'drawing on', 'building upon', 'in contrast', 'similarly'
        ]
        
        essay_count = sum(1 for pattern in essay_patterns if pattern in text_lower)
        if essay_count >= 3:
            return False, f"Contains essay patterns ({essay_count} found)"
        
        # Check for list/navigation patterns
        list_patterns = ['home', 'about', 'contact', 'subscribe', 'archive', 'browse']
        list_count = sum(1 for pattern in list_patterns if pattern in text_lower)
        if list_count >= 3:
            return False, "Contains navigation/list content"
        
        # Check for poetic indicators (positive signs)
        poetic_indicators = [
            'metaphor', 'imagery', 'stanza', 'verse', 'rhythm',
            'like', 'as if', 'becomes', 'transforms', 'whispers',
            'shadows', 'dreams', 'memory', 'heart', 'soul'
        ]
        
        poetic_count = sum(1 for indicator in poetic_indicators if indicator in text_lower)
        
        # Check line structure - poems have intentional line breaks
        short_lines = sum(1 for length in line_lengths if length < 60)
        line_variety = max(line_lengths) - min(line_lengths)
        
        # Poems typically have more short lines and varied structure
        if short_lines < len(lines) * 0.3 and line_variety < 20:
            return False, "Lacks poetic line structure"
        
        # Check for excessive repetition (might be navigation)
        unique_lines = set(lines)
        if len(unique_lines) < len(lines) * 0.7:
            return False, "Too much repetition - likely navigation"
        
        # Final validation: looks like a poem
        poem_score = 0
        
        # Positive indicators
        poem_score += poetic_count * 2
        poem_score += short_lines  # Short lines are good
        poem_score += min(line_variety // 10, 5)  # Line variety is good
        
        # Negative indicators
        poem_score -= essay_count * 3
        poem_score -= list_count * 2
        poem_score -= very_long_lines * 2
        
        if poem_score < 0:
            return False, f"Poem score too low ({poem_score})"
        
        return True, "Content validated as poem"
    
    def extract_poem_from_url(self, url, source_name="Unknown"):
        """Enhanced extraction with poem validation"""
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
                # VALIDATE IT'S ACTUALLY A POEM
                is_poem, poem_message = self.is_actually_a_poem(poem_text, title)
                if not is_poem:
                    print(f"❌ Not a poem: {poem_message} - {url}")
                    self.failed_urls.add(url)
                    return None
                
                poem_data = {
                    'title': title,
                    'author': author,
                    'text': poem_text,
                    'source': source_name,
                    'url': url
                }
                
                # Original validation (keep this too)
                is_valid, message = self.validate_poem_content(poem_data, url)
                if is_valid:
                    print(f"✅ Poem validated: {title} by {author}")
                    return poem_data
                else:
                    print(f"❌ Validation failed: {message} - {url}")
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
        """Enhanced author extraction with duplicate prevention"""
        author = "Unknown"
        
        # Strategy 1: Look for common author selectors
        author_selectors = [
            '.daily_poem_author', '.c-feature-sub', '.author', '.poet', 
            '.byline', '.poem-author', 'span.author', 'p.author',
            '.entry-author', '.post-author'
        ]
        
        # Try each selector once and take the first valid result
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
                
                # Validate candidate
                if (candidate and len(candidate) > 2 and len(candidate) < 50 and
                    candidate not in ['Instagram', 'Facebook', 'Twitter', 'Home', 'About', 'Poetry', 'Poems']):
                    author = candidate
                    break
        
        # Strategy 2: Look in page title for "by Author" (only if still unknown)
        if author == "Unknown":
            page_title = soup.find('title')
            if page_title:
                title_text = page_title.get_text()
                by_match = re.search(r'\bby\s+([^|–-]+)', title_text, re.IGNORECASE)
                if by_match:
                    candidate = by_match.group(1).strip()
                    if len(candidate) > 2 and len(candidate) < 50:
                        author = candidate
        
        # Strategy 3: Look for specific heading patterns (h3, h4 that might be authors)
        if author == "Unknown":
            for heading in ['h3', 'h4']:
                heading_elem = soup.select_one(heading)
                if heading_elem:
                    candidate = heading_elem.get_text().strip()
                    # Check if it looks like an author name (2-3 words, proper case)
                    words = candidate.split()
                    if (len(words) >= 2 and len(words) <= 3 and 
                        all(word[0].isupper() for word in words if word) and
                        len(candidate) < 50):
                        author = candidate
                        break
        
        return author
    
    def extract_clean_poem_text(self, soup):
        """Extract clean poem text with aggressive metadata filtering"""
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
        
        # AGGRESSIVE filtering for metadata
        clean_lines = []
        exclude_patterns = [
            'subscribe', 'newsletter', 'posted on', 'published', 'updated',
            'read more', 'www.', 'http', '.com', 'copyright', 'share this',
            'about', 'contact', 'menu', 'navigation', 'productions', 'film',
            'magazine', 'press', 'review', 'book', 'collection', 'university'
        ]
        
        for line in lines:
            line_lower = line.lower()
            
            # Skip dates and years (like "1936")
            if re.search(r'\d{4}', line):
                continue
            if re.search(r'\d{1,2}/\d{1,2}/\d{4}', line):
                continue
            if re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b', line):
                continue
            
            # Skip lines that repeat the title or author
            title_words = self.extract_better_title(soup, "").lower().split()
            if any(word in line_lower for word in title_words if len(word) > 3):
                continue
            
            # Skip unwanted content
            if (any(pattern in line_lower for pattern in exclude_patterns) or
                len(line.strip()) <= 3 or
                '//' in line or
                line.count(',') > 3):  # Likely metadata if many commas
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
        """Create clean, punchy tweet format with link"""
        if not poem:
            return False
        
        # Get the punchiest 4 lines
        punchy_lines = self.find_punchiest_4_lines(poem['text'])
        
        # Ensure we have at least 2 lines
        if len(punchy_lines) < 2:
            print("❌ Not enough clean lines found")
            return False
        
        # Simple format: Title — Author Name
        title = poem['title'][:40] + '...' if len(poem['title']) > 40 else poem['title']
        header = f"{title} — {poem['author']}"
        
        # Join the lines (aim for 4, but at least 2)
        poem_excerpt = '\n'.join(punchy_lines[:4])
        
        # Create tweet with link
        tweet_text = f"{header}\n{poem_excerpt}\n\n{poem['url']}\n\n#Poetry"
        
        # If too long, try without link first
        if len(tweet_text) > 280:
            tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # If still too long, use only 3 lines
        if len(tweet_text) > 280 and len(punchy_lines) >= 3:
            poem_excerpt = '\n'.join(punchy_lines[:3])
            tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # If still too long, use only 2 lines
        if len(tweet_text) > 280:
            poem_excerpt = '\n'.join(punchy_lines[:2])
            tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        # Final fallback - shorten title
        if len(tweet_text) > 280:
            short_title = title.split()[0] if title else "Poem"
            header = f"{short_title} — {poem['author']}"
            tweet_text = f"{header}\n{poem_excerpt}\n\n#Poetry"
        
        print(f"📱 PUNCHY TWEET ({len(tweet_text)} chars):")
        print("=" * 60)
        print(tweet_text)
        print("=" * 60)
        print(f"🎯 Selected {len(punchy_lines)} lines: {[line[:30] + '...' if len(line) > 30 else line for line in punchy_lines[:4]]}")
        
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