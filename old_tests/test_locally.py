#!/usr/bin/env python3
"""
Test script for Poetry Bot - run this locally before deploying
Now supports testing two posts per day with diversity tracking
"""

import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from dotenv import load_dotenv
from poetry_bot import PoetryBot
from config import BOT_SETTINGS

def test_environment():
    """Test if all environment variables are set"""
    print("🔍 Checking environment variables...")
    
    required_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET', 
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET'
    ]
    
    optional_vars = [
        'OPENAI_API_KEY',
        'GEMINI_API_KEY', 
        'CLAUDE_API_KEY'
    ]
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    if missing_required:
        print(f"❌ Missing required variables: {', '.join(missing_required)}")
        print("Please add them to your .env file")
        return False
    else:
        print("✅ All required Twitter API keys found")
    
    # Check optional AI API keys
    ai_keys_found = []
    for var in optional_vars:
        if os.getenv(var):
            ai_keys_found.append(var.replace('_API_KEY', ''))
    
    if ai_keys_found:
        print(f"✅ AI APIs available: {', '.join(ai_keys_found)}")
    else:
        print("⚠️  No AI API keys found - bot will only fetch from web sources")
    
    return True

def test_bot_dry_run():
    """Test the bot without actually posting"""
    print("\n🤖 Testing Poetry Bot (dry run)...")
    
    # Create bot instance
    bot = PoetryBot()
    
    # Test poem fetching
    print("📚 Testing poem fetching from literary journals...")
    poem = bot.fetch_poem_from_journals()
    
    if poem:
        print(f"✅ Fetched poem: '{poem['title']}' by {poem['author']} from {poem['source']}")
        print(f"Preview: {poem['text'][:100]}...")
    else:
        print("⚠️  Journal poem fetching failed, trying AI generation...")
        poem = bot.generate_ai_poem()
        
        if poem:
            print(f"✅ AI generated poem: '{poem['title']}' from {poem['source']}")
            print(f"Preview: {poem['text'][:100]}...")
        else:
            print("❌ Both journal fetching and AI generation failed")
            return False
    
    # Test image creation
    print("\n🖼️  Testing image creation...")
    image_path = bot.create_poem_image(poem)
    
    if image_path:
        print(f"✅ Image created: {image_path}")
        print("(Check your project folder for the image file)")
    else:
        print("❌ Image creation failed")
    
    # Test tweet formatting
    print("\n📝 Testing tweet formatting...")
    tweet_text = bot.format_tweet_text(poem)
    print(f"Tweet preview ({len(tweet_text)} chars):")
    print("-" * 50)
    print(tweet_text)
    print("-" * 50)
    
    if len(tweet_text) > 280:
        print("⚠️  Tweet is too long!")
    else:
        print("✅ Tweet length is good")
    
    # Clean up test image
    if image_path and os.path.exists(image_path):
        os.remove(image_path)
        print("🧹 Cleaned up test image")
    
    return True

def extract_poetry_daily():
    """Extract today's poem from Poetry Daily"""
    try:
        url = 'https://poems.com/todays-poem/'
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Poetry Daily HTTP {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main poem content
        poem_content = soup.find('div', class_='poem') or soup.find('div', id='poem') or soup.find('main')
        
        if not poem_content:
            print("❌ No poem content found on Poetry Daily")
            return None
        
        # Extract title - look for h1 or h2
        title_elem = poem_content.find('h1') or poem_content.find('h2')
        title = title_elem.text.strip() if title_elem else "Daily Poem"
        
        # Extract author - look for author patterns
        author = "Unknown"
        
        # Try different author selectors
        author_elem = (poem_content.find('span', class_='author') or 
                      poem_content.find('p', class_='author') or
                      poem_content.find('div', class_='author') or
                      poem_content.find('cite'))
        
        if author_elem:
            author = author_elem.text.strip()
        else:
            # Look for "by Author Name" pattern in text
            text_content = poem_content.get_text()
            author_match = re.search(r'by\s+([^\n,]+)', text_content, re.IGNORECASE)
            if author_match:
                author = author_match.group(1).strip()
        
        # Clean up author (remove common prefixes/suffixes)
        author = re.sub(r'^(by\s+)', '', author, flags=re.IGNORECASE)
        author = re.sub(r'(,.*$)', '', author)  # Remove everything after comma
        
        # If author extraction failed, try to find it in the text more carefully
        if author == "Unknown" or len(author) > 50 or '"' in author:
            # Look for author name patterns in the full text
            full_text = soup.get_text()
            # Try to find author after poem content
            author_patterns = [
                r'—\s*([A-Z][a-zA-Z\s\.]+)',  # — Author Name
                r'by\s+([A-Z][a-zA-Z\s\.]+)',  # by Author Name
                r'([A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z\.]+(?:\s+Jr\.?)?)\s*$',  # Author Name at end
            ]
            
            for pattern in author_patterns:
                match = re.search(pattern, full_text, re.MULTILINE)
                if match:
                    potential_author = match.group(1).strip()
                    # Validate it looks like a real name
                    if (len(potential_author) < 50 and 
                        not any(word in potential_author.lower() for word in ['the', 'and', 'book', 'poem', 'read'])):
                        author = potential_author
                        break
        
        # Extract poem text
        poem_text = poem_content.get_text(separator='\n').strip()
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        # Clean up lines - remove title, author, and navigation
        clean_lines = []
        navigation_words = [
            'poetry daily', 'poems.com', 'subscribe', 'newsletter', 'archive',
            'browse', 'search', 'about', 'contact', 'home', 'menu', 'read today',
            'interview', 'from the book', 'books', 'press', 'publisher', 'pdnews',
            'poet laureate', 'macarthur', 'national book award', 'www.', 'http',
            'grant', 'winner', 'signature project', 'connect', 'appearance'
        ]
        
        for line in lines:
            line_lower = line.lower()
            # Skip if contains title, author, navigation, or metadata
            if (title.lower() not in line_lower and 
                author.lower() not in line_lower and
                'by ' not in line_lower[:10] and
                not any(nav_word in line_lower for nav_word in navigation_words) and
                len(line.strip()) > 5 and
                not line.strip().startswith('(') and  # Skip parenthetical notes
                not line.strip().endswith(')') and   # Skip parenthetical notes
                '//' not in line):  # Skip lines with // (poem formatting)
                clean_lines.append(line)
        
        # Take first 15 lines of actual poem content
        poem_text = '\n'.join(clean_lines[:15])
        
        if len(poem_text) > 50:  # Ensure we have substantial content
            return {
                'title': title,
                'author': author,
                'text': poem_text,
                'source': 'Poetry Daily',
                'url': url
            }
        
        print("❌ Insufficient poem content after cleaning")
        return None
        
    except Exception as e:
        print(f"❌ Poetry Daily extraction failed: {e}")
        return None

def extract_verse_daily():
    """Extract today's poem from Verse Daily"""
    try:
        url = 'https://www.versedaily.org/'
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Verse Daily HTTP {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find today's poem
        poem_content = soup.find('div', class_='poem') or soup.find('main') or soup.find('article')
        
        if not poem_content:
            print("❌ No poem content found on Verse Daily")
            return None
        
        # Similar extraction logic as Poetry Daily
        title_elem = poem_content.find('h1') or poem_content.find('h2')
        title = title_elem.text.strip() if title_elem else "Daily Verse"
        
        # Extract author
        author = "Unknown"
        author_elem = poem_content.find('span', class_='author') or poem_content.find('p', class_='author')
        if author_elem:
            author = author_elem.text.strip()
        else:
            text_content = poem_content.get_text()
            author_match = re.search(r'by\s+([^\n,]+)', text_content, re.IGNORECASE)
            if author_match:
                author = author_match.group(1).strip()
        
        # Clean author
        author = re.sub(r'^(by\s+)', '', author, flags=re.IGNORECASE)
        author = re.sub(r'(,.*$)', '', author)
        
        # Extract and clean poem text
        poem_text = poem_content.get_text(separator='\n').strip()
        lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
        
        clean_lines = []
        for line in lines:
            line_lower = line.lower()
            if (title.lower() not in line_lower and 
                author.lower() not in line_lower and
                'verse daily' not in line_lower and
                len(line.strip()) > 5):
                clean_lines.append(line)
        
        poem_text = '\n'.join(clean_lines[:15])
        
        if len(poem_text) > 50:
            return {
                'title': title,
                'author': author,
                'text': poem_text,
                'source': 'Verse Daily',
                'url': url
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Verse Daily extraction failed: {e}")
        return None

def select_striking_lines(poem_text):
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
    
    # Words that indicate metadata/non-poem content
    metadata_indicators = [
        'book', 'press', 'publisher', 'interview', 'award', 'winner',
        'laureate', 'grant', 'university', 'college', 'from the', 'jr.',
        'www.', 'http', '.com', '.org', 'read today', 'pdnews'
    ]
    
    scored_lines = []
    for i, line in enumerate(lines):
        score = 0
        line_lower = line.lower()
        
        # Skip lines that contain metadata indicators
        if any(indicator in line_lower for indicator in metadata_indicators):
            continue
        
        # Skip lines that look like author names or titles
        if (line.strip().endswith('Jr.') or 
            line.strip().endswith('Jr') or
            'from the book' in line_lower or
            line.count('.') > 2):  # Likely a website or complex metadata
            continue
        
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
        
        # Bonus for lines that look like actual poetry
        if any(char in line for char in ',."\''):
            score += 1
            
        scored_lines.append((score, i, line))
    
    # Sort by score and select best lines (up to 4)
    scored_lines.sort(reverse=True, key=lambda x: x[0])
    
    # Take up to 4 best lines, maintaining original order
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

def format_tweet_text(poem):
    """Format poem in exact format requested"""
    # Extract up to 4 striking lines from the poem
    striking_lines = select_striking_lines(poem['text'])
    
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
    
    # Read more link
    read_more = f"Read more: {poem_url}"
    
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

def main():
    """Test focused extraction from reliable sources"""
    print("🧪 Testing focused poem extraction...")
    
    # Try Poetry Daily first
    print("\n📰 Trying Poetry Daily...")
    poem = extract_poetry_daily()
    
    if not poem:
        print("\n📰 Trying Verse Daily...")
        poem = extract_verse_daily()
    
    if poem:
        print(f"\n✅ Successfully extracted poem!")
        print(f"📖 Title: {poem['title']}")
        print(f"✍️  Author: {poem['author']}")
        print(f"📍 Source: {poem['source']}")
        print(f"🔗 URL: {poem['url']}")
        
        print(f"\n📝 Full poem text:")
        print("-" * 50)
        print(poem['text'])
        print("-" * 50)
        
        # Test striking lines selection
        striking_lines = select_striking_lines(poem['text'])
        print(f"\n✨ Selected striking lines:")
        print(striking_lines)
        
        # Test tweet formatting
        tweet_text = format_tweet_text(poem)
        print(f"\n🐦 Tweet preview ({len(tweet_text)} chars):")
        print("-" * 50)
        print(tweet_text)
        print("-" * 50)
        
    else:
        print("❌ Failed to extract poem from reliable sources")

if __name__ == "__main__":
    main()