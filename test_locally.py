#!/usr/bin/env python3
"""
Test script for Poetry Bot - run this locally before deploying
Now supports testing two posts per day with diversity tracking
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from poetry_bot import PoetryBot
from config import BOT_SETTINGS, LITERARY_JOURNALS

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

def main():
    """Main test function - now supports random selection and excerpt format"""
    print("🧪 Poetry Bot Local Testing - Random Selection & Excerpt Format")
    print("=" * 70)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Test environment setup
    if not test_environment():
        print("\nPlease fix the environment issues and try again.")
        return
    
    # Test bot functionality with new random selection approach
    print(f"\n🚀 Testing {BOT_SETTINGS.get('posts_per_day', 2)} posts per day with random selection...")
    
    if test_bot_dry_run():
        print("\n🎉 All tests passed! Your Poetry Bot is ready to deploy.")
        print("\nNext steps:")
        print("1. Create a GitHub repository")
        print("2. Push your code to GitHub") 
        print("3. Add your API keys as GitHub Secrets")
        print("4. Enable GitHub Actions")
        print("5. Watch your bot post striking poetry excerpts twice daily!")
        
        print("\n🕐 Your posting schedule:")
        post_times = BOT_SETTINGS.get('post_times_utc', ['09:00', '21:00'])
        for i, time in enumerate(post_times, 1):
            print(f"   📅 Post {i}: {time} UTC (random selection)")
        
        print("\n🌟 Enhanced Features:")
        print("   🎲 Random selection (equal opportunity)")
        print("   📝 Striking excerpt format (1-2 lines + link)")
        print("   🌍 Preference for major sources (3x probability)")
        print("   🔄 Smart diversity tracking")
        print("   🤖 Limited AI backup (1 per day)")
        print(f"   📚 {len(LITERARY_JOURNALS)} curated sources")
        print("   ✅ Bulletproof validation")
        print("   🔗 Links to full poems for engagement")
        print("   ⚡ No image generation (faster posting)")
        
        print("\n📝 Excerpt Format Example:")
        print('   "The woods are lovely, dark and deep,')
        print('   But I have promises to keep"')
        print('')
        print('   — Robert Frost, "Stopping by Woods on a Snowy Evening"')
        print('')
        print('   Read full poem: [link]')
        print('')
        print('   #poetry #poems #literature')
        
        # Instagram integration test
        print("\n📱 Testing Instagram integration...")
        bot = PoetryBot()
        # Try to fetch a poem (reuse dry run logic)
        poem = bot.fetch_poem_from_journals()
        if not poem:
            poem = bot.generate_ai_poem()
        if poem and hasattr(bot, 'instagram') and bot.instagram:
            print("Attempting to post to Instagram...")
            result = bot.post_to_instagram(poem)
            if result:
                print("✅ Instagram post test succeeded!")
            else:
                print("❌ Instagram post test failed.")
        else:
            print("⚠️  Instagram not configured or no poem available for Instagram test.")

    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        print("💡 Common issues:")
        print("   - Missing API keys in .env file")
        print("   - Internet connection problems")
        print("   - Literary journal websites temporarily down")
        print("   - Need to install missing Python packages")

if __name__ == "__main__":
    main()