#!/usr/bin/env python3
"""
Test Instagram Poetry Bot
Tests Instagram posting functionality without actually posting
"""

import os
from dotenv import load_dotenv
from instagram_bot import InstagramPoetryBot

# Load environment variables
load_dotenv()

def test_instagram_bot():
    """Test Instagram bot functionality"""
    print("🧪 Testing Instagram Poetry Bot...")
    print("=" * 50)
    
    try:
        # Test Instagram credentials
        username = os.getenv('INSTAGRAM_USERNAME')
        password = os.getenv('INSTAGRAM_PASSWORD')
        
        print(f"📱 Instagram Username: {'✅ Found' if username else '❌ Missing'}")
        print(f"🔐 Instagram Password: {'✅ Found' if password else '❌ Missing'}")
        
        if not username or not password:
            print("⚠️  Instagram credentials missing - cannot test posting")
            return False
        
        # Initialize bot (but don't actually connect to Instagram in test mode)
        print("\n🤖 Initializing Instagram bot...")
        
        # Create a mock bot for testing
        class MockInstagramBot(InstagramPoetryBot):
            def setup_instagram(self):
                """Mock Instagram setup for testing"""
                print("🧪 Mock Instagram setup (test mode)")
                self.instagram = "mock_client"  # Mock client
                
            def post_to_instagram(self, poem):
                """Mock Instagram posting for testing"""
                print("🧪 Mock Instagram posting (test mode)")
                
                # Test image creation
                try:
                    img_path = self.create_instagram_image(poem)
                    print(f"✅ Image created successfully: {img_path}")
                    
                    # Test caption creation
                    caption = self.create_instagram_caption(poem)
                    print(f"✅ Caption created ({len(caption)} chars)")
                    print(f"📝 Caption preview: {caption[:150]}...")
                    
                    # Clean up test image
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        print("🧹 Test image cleaned up")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ Mock posting failed: {e}")
                    return False
        
        # Test the bot
        bot = MockInstagramBot()
        
        # Test theme generation
        theme = bot.get_hourly_theme()
        print(f"🎨 Current hour theme: {theme}")
        
        # Test poem fetching
        print("\n📚 Testing poem fetching...")
        poem = bot.fetch_poem_for_instagram()
        
        if poem:
            print(f"✅ Poem found: '{poem['title']}' by {poem['author']}")
            print(f"📍 Source: {poem['source']}")
            print(f"📝 Text preview: {poem['text'][:100]}...")
            
            # Test Instagram suitability
            is_suitable = bot.is_good_for_instagram(poem)
            print(f"📱 Instagram suitable: {'✅ Yes' if is_suitable else '❌ No'}")
            
            # Test posting (mock)
            print("\n📱 Testing Instagram posting (mock)...")
            success = bot.post_to_instagram(poem)
            
            if success:
                print("✅ Instagram test completed successfully!")
                return True
            else:
                print("❌ Instagram test failed")
                return False
        else:
            print("❌ No poem found for testing")
            return False
            
    except Exception as e:
        print(f"❌ Instagram test failed with error: {e}")
        return False

def test_ai_generation():
    """Test AI poem generation for Instagram"""
    print("\n🎨 Testing AI poem generation...")
    
    try:
        from instagram_bot import InstagramPoetryBot
        
        class MockAIBot(InstagramPoetryBot):
            def setup_instagram(self):
                self.instagram = "mock"
                
        bot = MockAIBot()
        
        # Test AI generation
        ai_poem = bot.generate_instagram_poem()
        
        if ai_poem:
            print(f"✅ AI poem generated: '{ai_poem['title']}'")
            print(f"🤖 Source: {ai_poem['source']}")
            print(f"📝 Text: {ai_poem['text']}")
            
            # Test if it's suitable for Instagram
            is_suitable = bot.is_good_for_instagram(ai_poem)
            print(f"📱 Instagram suitable: {'✅ Yes' if is_suitable else '❌ No'}")
            
            return True
        else:
            print("❌ AI poem generation failed")
            return False
            
    except Exception as e:
        print(f"❌ AI generation test failed: {e}")
        return False

def main():
    """Run all Instagram tests"""
    print("🧪 Instagram Poetry Bot Test Suite")
    print("=" * 60)
    
    # Test basic functionality
    basic_test = test_instagram_bot()
    
    # Test AI generation
    ai_test = test_ai_generation()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Basic Instagram functionality: {'✅ PASS' if basic_test else '❌ FAIL'}")
    print(f"   AI poem generation: {'✅ PASS' if ai_test else '❌ FAIL'}")
    
    if basic_test and ai_test:
        print("\n🎉 All Instagram tests passed!")
        print("📱 Your Instagram Poetry Bot is ready for hourly posting!")
        print("\n📋 Next steps:")
        print("   1. Add Instagram credentials to GitHub Secrets:")
        print("      - INSTAGRAM_USERNAME")
        print("      - INSTAGRAM_PASSWORD")
        print("   2. Enable the hourly-instagram.yml workflow")
        print("   3. Monitor the first few posts to ensure everything works")
        print("   4. Enjoy 24 beautiful poetry posts per day! 🎨")
        return True
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main() 