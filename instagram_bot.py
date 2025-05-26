#!/usr/bin/env python3
"""
Instagram Poetry Bot - Hourly Posts
Posts beautiful poetry content to Instagram every hour
"""

import os
import random
import requests
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
from instagrapi import Client

# Load environment variables
load_dotenv()

class InstagramPoetryBot:
    def __init__(self):
        # Initialize Instagram
        self.setup_instagram()
        
        # Initialize AI APIs for content generation
        self.setup_ai_apis()
        
        # Track hourly posts to avoid duplicates within the hour
        self.hourly_posts = {
            'authors': [],
            'sources': [],
            'poems_posted': [],
            'hour': datetime.now().hour
        }
        
    def setup_instagram(self):
        """Set up Instagram client"""
        username = os.getenv('INSTAGRAM_USERNAME')
        password = os.getenv('INSTAGRAM_PASSWORD')
        
        if not username or not password:
            raise ValueError("Instagram credentials not found in environment variables")
            
        try:
            self.instagram = Client()
            # Try to load session first to avoid repeated logins
            session_file = f"instagram_session_{username}.json"
            if os.path.exists(session_file):
                try:
                    self.instagram.load_settings(session_file)
                    self.instagram.login(username, password)
                    print("✅ Instagram session restored successfully")
                except:
                    # If session restore fails, do fresh login
                    self.instagram.login(username, password)
                    self.instagram.dump_settings(session_file)
                    print("✅ Instagram fresh login successful")
            else:
                self.instagram.login(username, password)
                self.instagram.dump_settings(session_file)
                print("✅ Instagram connected and session saved")
                
        except Exception as e:
            print(f"❌ Instagram connection failed: {e}")
            self.instagram = None
            
    def setup_ai_apis(self):
        """Set up AI API connections for backup content"""
        # Gemini (recommended - free tier)
        if os.getenv('GEMINI_API_KEY'):
            genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
            print("✅ Gemini API connected")
            
        # Claude
        if os.getenv('CLAUDE_API_KEY'):
            self.claude_client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
            print("✅ Claude API connected")
        else:
            self.claude_client = None
            
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            print("✅ OpenAI API connected")

    def get_hourly_theme(self):
        """Get theme based on current hour for variety"""
        hour = datetime.now().hour
        
        # Different themes for different times of day
        if 5 <= hour < 9:  # Early morning
            themes = ['dawn', 'morning', 'sunrise', 'awakening', 'fresh start']
        elif 9 <= hour < 12:  # Morning
            themes = ['hope', 'energy', 'growth', 'possibility', 'light']
        elif 12 <= hour < 17:  # Afternoon
            themes = ['strength', 'journey', 'discovery', 'adventure', 'clarity']
        elif 17 <= hour < 21:  # Evening
            themes = ['reflection', 'beauty', 'peace', 'gratitude', 'golden hour']
        else:  # Night
            themes = ['dreams', 'stars', 'mystery', 'solitude', 'moonlight']
            
        return random.choice(themes)

    def fetch_poem_for_instagram(self):
        """Fetch a poem optimized for Instagram format"""
        from config import get_weighted_journal_list
        
        # Get weighted list and shuffle for randomness
        weighted_journals = get_weighted_journal_list()
        random.shuffle(weighted_journals)
        
        # Try to get a poem from literary journals first
        for journal in weighted_journals[:10]:  # Try up to 10 sources
            try:
                print(f"🎲 Trying: {journal['name']}")
                poem = self.fetch_from_journal(journal)
                
                if poem and self.is_good_for_instagram(poem):
                    print(f"✅ Found Instagram-suitable poem from {journal['name']}")
                    return poem
                    
            except Exception as e:
                print(f"❌ {journal['name']} failed: {e}")
                continue
        
        # If no suitable poem found, generate with AI
        print("🎨 Generating AI poem for Instagram...")
        return self.generate_instagram_poem()

    def fetch_from_journal(self, journal):
        """Simplified journal fetching for Instagram"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; InstagramPoetryBot/1.0)'}
            response = requests.get(journal['url'], headers=headers, timeout=10)
            
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for poem links
            poem_links = soup.find_all('a', href=True)
            poem_urls = []
            
            for link in poem_links:
                href = link['href']
                if any(indicator in href.lower() for indicator in ['/poem', '/poetry', '/verse']):
                    if not href.startswith('http'):
                        from urllib.parse import urljoin
                        href = urljoin(journal['url'], href)
                    poem_urls.append(href)
            
            # Try a few random poems
            for _ in range(min(3, len(poem_urls))):
                poem_url = random.choice(poem_urls)
                poem = self.extract_poem_details(poem_url, journal['name'])
                if poem:
                    return poem
                    
        except Exception as e:
            print(f"Journal fetch failed: {e}")
            
        return None

    def extract_poem_details(self, url, source_name):
        """Extract poem details optimized for Instagram"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; InstagramPoetryBot/1.0)'}
            response = requests.get(url, headers=headers, timeout=8)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find('h2')
            title = title_elem.text.strip() if title_elem else "Untitled"
            
            # Extract author
            author_elem = soup.find('span', class_='author') or soup.find('p', class_='author')
            if not author_elem:
                import re
                text_content = soup.get_text()
                author_match = re.search(r'by\s+([^\n,]+)', text_content, re.IGNORECASE)
                author = author_match.group(1).strip() if author_match else "Unknown"
            else:
                author = author_elem.text.strip()
            
            # Extract poem text
            poem_content = (soup.find('div', class_='poem') or 
                           soup.find('div', class_='poetry') or
                           soup.find('main') or
                           soup.find('article'))
            
            if poem_content:
                text = poem_content.get_text(separator='\n').strip()
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                
                # Clean and limit for Instagram
                clean_lines = []
                for line in lines[:12]:  # Limit to 12 lines for Instagram
                    if (title.lower() not in line.lower() and 
                        author.lower() not in line.lower()):
                        clean_lines.append(line)
                
                text = '\n'.join(clean_lines)
                
                if len(text) > 30:
                    return {
                        'title': title[:60],  # Limit title length
                        'author': author[:40],  # Limit author length
                        'text': text,
                        'source': source_name,
                        'url': url
                    }
                    
        except Exception as e:
            print(f"Poem extraction failed: {e}")
            
        return None

    def is_good_for_instagram(self, poem):
        """Check if poem is suitable for Instagram format"""
        if not poem or not poem.get('text'):
            return False
            
        text = poem['text']
        lines = text.split('\n')
        
        # Instagram preferences
        if len(lines) > 15:  # Too long for image
            return False
        if len(text) < 20:  # Too short
            return False
        if any(len(line) > 80 for line in lines):  # Lines too long for image
            return False
            
        return True

    def generate_instagram_poem(self):
        """Generate AI poem optimized for Instagram"""
        theme = self.get_hourly_theme()
        hour = datetime.now().hour
        
        # Time-specific prompts
        if 5 <= hour < 12:
            time_context = "morning light and new beginnings"
        elif 12 <= hour < 17:
            time_context = "afternoon energy and clarity"
        elif 17 <= hour < 21:
            time_context = "evening reflection and golden light"
        else:
            time_context = "night's mystery and starlight"
            
        prompt = f"""Write a beautiful, evocative poem about {theme} with {time_context}. 
        Keep it under 8 lines and 200 characters total. 
        Focus on vivid imagery and emotional resonance.
        Make it perfect for Instagram - inspiring and shareable."""
        
        # Try Gemini first (free tier)
        if os.getenv('GEMINI_API_KEY'):
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                poem_text = response.text.strip()
                
                return {
                    'title': f"Inspired by {theme.title()}",
                    'author': 'AI Generated',
                    'text': poem_text,
                    'source': 'Gemini AI',
                    'theme': theme
                }
            except Exception as e:
                print(f"Gemini generation failed: {e}")
        
        # Fallback to Claude
        if self.claude_client:
            try:
                response = self.claude_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=150,
                    messages=[{"role": "user", "content": prompt}]
                )
                poem_text = response.content[0].text.strip()
                
                return {
                    'title': f"Inspired by {theme.title()}",
                    'author': 'AI Generated',
                    'text': poem_text,
                    'source': 'Claude AI',
                    'theme': theme
                }
            except Exception as e:
                print(f"Claude generation failed: {e}")
        
        # Final fallback - simple themed poem
        return {
            'title': f"Moment of {theme.title()}",
            'author': 'Poetry Bot',
            'text': f"In this hour of {theme},\nWords find their way\nTo hearts that listen.",
            'source': 'Generated',
            'theme': theme
        }

    def create_instagram_image(self, poem):
        """Create beautiful Instagram square image with poem"""
        width, height = 1080, 1080
        
        # Create gradient background based on time of day
        hour = datetime.now().hour
        if 5 <= hour < 12:  # Morning - warm colors
            colors = [(255, 223, 186), (255, 182, 193)]  # Peach to pink
        elif 12 <= hour < 17:  # Afternoon - bright colors
            colors = [(135, 206, 235), (255, 255, 255)]  # Sky blue to white
        elif 17 <= hour < 21:  # Evening - golden colors
            colors = [(255, 165, 0), (255, 69, 0)]  # Orange to red-orange
        else:  # Night - cool colors
            colors = [(25, 25, 112), (72, 61, 139)]  # Midnight blue to dark slate blue
        
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Create gradient
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Load fonts
        try:
            font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        except:
            try:
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_medium = ImageFont.truetype("arial.ttf", 36)
                font_small = ImageFont.truetype("arial.ttf", 28)
            except:
                font_large = ImageFont.load_default()
                font_medium = ImageFont.load_default()
                font_small = ImageFont.load_default()
        
        # Text color (contrasting with background)
        if hour < 17:
            text_color = (40, 40, 40)  # Dark text for light backgrounds
        else:
            text_color = (255, 255, 255)  # Light text for dark backgrounds
        
        # Position poem text in center
        y_pos = 300
        lines = poem['text'].split('\n')[:8]  # Limit to 8 lines
        
        for line in lines:
            if line.strip():
                # Wrap long lines
                wrapped_lines = textwrap.fill(line, width=25).split('\n')
                for wrapped_line in wrapped_lines:
                    bbox = draw.textbbox((0, 0), wrapped_line, font=font_large)
                    text_width = bbox[2] - bbox[0]
                    x_pos = (width - text_width) // 2
                    draw.text((x_pos, y_pos), wrapped_line, fill=text_color, font=font_large)
                    y_pos += 60
        
        # Add author attribution
        y_pos += 40
        author_text = f"— {poem['author']}"
        bbox = draw.textbbox((0, 0), author_text, font=font_medium)
        text_width = bbox[2] - bbox[0]
        x_pos = (width - text_width) // 2
        draw.text((x_pos, y_pos), author_text, fill=text_color, font=font_medium)
        
        # Add time/hour indicator
        time_text = f"Hour {datetime.now().hour:02d}"
        bbox = draw.textbbox((0, 0), time_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        draw.text((width - text_width - 40, height - 60), time_text, fill=text_color, font=font_small)
        
        # Save image
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        img_path = f"instagram_poem_{timestamp}.jpg"
        img.save(img_path, 'JPEG', quality=95)
        
        return img_path

    def create_instagram_caption(self, poem):
        """Create engaging Instagram caption"""
        hour = datetime.now().hour
        
        # Time-based greetings
        if 5 <= hour < 12:
            greeting = "Good morning, poetry lovers! ☀️"
        elif 12 <= hour < 17:
            greeting = "Afternoon inspiration! ✨"
        elif 17 <= hour < 21:
            greeting = "Evening reflections 🌅"
        else:
            greeting = "Under the stars tonight 🌙"
        
        # Build caption
        caption = f'{greeting}\n\n'
        
        if 'AI Generated' in poem['author']:
            caption += f'"{poem["title"]}" - a moment of {poem.get("theme", "beauty")}\n\n'
        else:
            caption += f'"{poem["title"]}" by {poem["author"]}\n\n'
        
        # Add engaging question
        questions = [
            "What line speaks to your heart? 💭",
            "Which words resonate with you today? 🤔",
            "What emotions does this evoke? ❤️",
            "Share your favorite line below! 👇",
            "How does this make you feel? ✨"
        ]
        caption += random.choice(questions) + '\n\n'
        
        # Add source if available
        if poem.get('url') and 'AI Generated' not in poem['author']:
            caption += f"Read more: {poem['url']}\n\n"
        
        # Hashtags
        hashtags = [
            "#poetry", "#dailypoetry", "#poetrycommunity", "#poetrylovers",
            "#instapoetry", "#poems", "#poetrygram", "#writersofinstagram",
            "#literature", "#poetryislife", "#wordsmith", "#verse",
            "#poetryquotes", "#inspiration", "#mindfulness"
        ]
        
        # Add time-specific hashtags
        if 5 <= hour < 12:
            hashtags.extend(["#morningpoetry", "#sunrise", "#newday"])
        elif 12 <= hour < 17:
            hashtags.extend(["#afternoonvibes", "#inspiration", "#clarity"])
        elif 17 <= hour < 21:
            hashtags.extend(["#eveningpoetry", "#reflection", "#goldenhour"])
        else:
            hashtags.extend(["#nightpoetry", "#stars", "#dreams"])
        
        # Limit hashtags to avoid spam
        selected_hashtags = hashtags[:20]
        caption += ' '.join(selected_hashtags)
        
        return caption

    def post_to_instagram(self, poem):
        """Post poem to Instagram with image and caption"""
        if not self.instagram:
            print("❌ Instagram not configured")
            return False
            
        try:
            # Create image
            print("🖼️  Creating Instagram image...")
            img_path = self.create_instagram_image(poem)
            
            # Create caption
            print("📝 Creating Instagram caption...")
            caption = self.create_instagram_caption(poem)
            
            print(f"📱 Posting to Instagram...")
            print(f"Caption preview: {caption[:100]}...")
            
            # Upload to Instagram
            media = self.instagram.photo_upload(img_path, caption)
            print(f"✅ Posted to Instagram successfully! Media ID: {media.pk}")
            
            # Clean up image file
            if os.path.exists(img_path):
                os.remove(img_path)
                
            return True
            
        except Exception as e:
            print(f"❌ Instagram posting failed: {e}")
            return False

    def run(self):
        """Main Instagram bot execution"""
        print("📱 Instagram Poetry Bot starting...")
        
        current_hour = datetime.now().hour
        print(f"🕐 Current hour: {current_hour:02d}")
        print(f"🎨 Theme for this hour: {self.get_hourly_theme()}")
        
        # Get poem for Instagram
        poem = self.fetch_poem_for_instagram()
        
        if not poem:
            print("❌ Failed to get any poem for Instagram")
            return False
            
        print(f"📝 Selected: '{poem['title']}' by {poem['author']}")
        print(f"📍 Source: {poem['source']}")
        
        # Post to Instagram
        success = self.post_to_instagram(poem)
        
        if success:
            print(f"🎉 Instagram poetry bot completed successfully!")
            print(f"✨ Posted '{poem['title']}' by {poem['author']}")
        else:
            print("❌ Instagram poetry bot encountered errors")
            
        return success

if __name__ == "__main__":
    try:
        bot = InstagramPoetryBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        exit(1) 