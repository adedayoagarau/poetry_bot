import os
import random
import requests
import tweepy
from datetime import datetime
import openai
import google.generativeai as genai
import anthropic
from PIL import Image, ImageDraw, ImageFont
import textwrap
from bs4 import BeautifulSoup
import json
from config import *

class PoetryBot:
    def __init__(self):
        # Initialize Twitter API
        self.setup_twitter()
        
        # Initialize AI APIs
        self.setup_ai_apis()
        
    def setup_twitter(self):
        """Set up Twitter API connection"""
        try:
            auth = tweepy.OAuthHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET')
            )
            auth.set_access_token(
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            self.twitter_api = tweepy.API(auth)
            print("✅ Twitter API connected successfully")
        except Exception as e:
            print(f"❌ Twitter API connection failed: {e}")
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

    def fetch_poem_from_poetry_foundation(self):
        """Fetch a random poem from Poetry Foundation"""
        try:
            # Poetry Foundation's poems of the day archive
            url = "https://www.poetryfoundation.org/poems/browse"
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
            
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find poem links
            poem_links = soup.find_all('a', href=True)
            poem_urls = [link['href'] for link in poem_links if '/poems/' in link['href']]
            
            if poem_urls:
                # Get a random poem
                poem_url = random.choice(poem_urls[:20])  # Take from first 20 to avoid too obscure ones
                if not poem_url.startswith('http'):
                    poem_url = 'https://www.poetryfoundation.org' + poem_url
                
                return self.extract_poem_details(poem_url)
                
        except Exception as e:
            print(f"Poetry Foundation fetch failed: {e}")
            
        return None

    def extract_poem_details(self, url):
        """Extract poem title, author, and text from URL"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find title and author
            title = soup.find('h1')
            title = title.text.strip() if title else "Untitled"
            
            author = soup.find('span', class_='author') or soup.find('a', href=lambda x: x and '/poets/' in x)
            author = author.text.strip() if author else "Unknown"
            
            # Try to find poem text
            poem_content = soup.find('div', class_='poem') or soup.find('div', class_='poetry')
            if not poem_content:
                # Try other common selectors
                poem_content = soup.find('div', {'data-view': 'poems'}) or soup.find('main')
            
            if poem_content:
                # Clean up the text
                text = poem_content.get_text(separator='\n').strip()
                # Remove extra whitespace and clean up
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                text = '\n'.join(lines[:20])  # Limit to first 20 lines
                
                return {
                    'title': title,
                    'author': author,
                    'text': text,
                    'source': 'Poetry Foundation'
                }
                
        except Exception as e:
            print(f"Poem extraction failed: {e}")
            
        return None

    def generate_ai_poem(self):
        """Generate a poem using AI APIs"""
        themes = POETRY_THEMES
        theme = random.choice(themes)
        
        prompt = f"Write a beautiful, short poem about {theme}. Keep it under 200 characters, suitable for social media. Make it inspiring and thoughtful."
        
        # Try different AI services
        poem = None
        
        # Try Gemini first (free tier available)
        if os.getenv('GEMINI_API_KEY') and not poem:
            try:
                model = genai.GenerativeModel('gemini-pro')
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
                    max_tokens=150,
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
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150
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
        """Format poem for Twitter with character limit"""
        # Start with title and author
        base_text = f'"{poem["title"]}" by {poem["author"]}\n\n'
        
        # Add poem text, respecting Twitter's 280 character limit
        available_chars = 280 - len(base_text) - len(' '.join(HASHTAGS)) - 10  # Buffer
        
        poem_text = poem['text']
        if len(poem_text) > available_chars:
            # Truncate and add ellipsis
            poem_text = poem_text[:available_chars-3] + "..."
        
        # Combine everything
        tweet_text = base_text + poem_text + '\n\n' + ' '.join(HASHTAGS[:5])  # Limit hashtags
        
        return tweet_text[:280]  # Final safety check

    def post_to_twitter(self, poem, image_path=None):
        """Post poem to Twitter"""
        if not self.twitter_api:
            print("❌ Twitter API not available")
            return False
            
        try:
            tweet_text = self.format_tweet_text(poem)
            
            if image_path and os.path.exists(image_path):
                # Post with image
                media = self.twitter_api.media_upload(image_path)
                tweet = self.twitter_api.update_status(status=tweet_text, media_ids=[media.media_id])
            else:
                # Post text only
                tweet = self.twitter_api.update_status(status=tweet_text)
            
            print(f"✅ Posted to Twitter: {tweet.id}")
            return True
            
        except Exception as e:
            print(f"❌ Twitter posting failed: {e}")
            return False

    def run(self):
        """Main bot execution"""
        print("🤖 Poetry Bot starting...")
        
        # Try to fetch a poem from Poetry Foundation first
        poem = self.fetch_poem_from_poetry_foundation()
        
        # If that fails, generate with AI
        if not poem:
            print("🎨 Generating AI poem...")
            poem = self.generate_ai_poem()
        
        if not poem:
            print("❌ Failed to get any poem")
            return
            
        print(f"📝 Got poem: '{poem['title']}' by {poem['author']}")
        
        # Create image
        image_path = self.create_poem_image(poem)
        if image_path:
            print(f"🖼️ Created image: {image_path}")
        
        # Post to Twitter
        success = self.post_to_twitter(poem, image_path)
        
        # Clean up image file
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
            
        if success:
            print("🎉 Poetry bot completed successfully!")
        else:
            print("❌ Poetry bot encountered errors")

if __name__ == "__main__":
    bot = PoetryBot()
    bot.run()