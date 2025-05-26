#!/usr/bin/env python3
"""
Quick Twitter test - Generate and post AI poem right now
"""

from poetry_bot import PoetryBot

def test_twitter_post():
    print("🐦 Twitter Poetry Bot - Live Test")
    print("=" * 50)
    
    # Create bot
    bot = PoetryBot()
    
    # Force AI generation for demo
    print('🎨 Generating AI poem for Twitter demo...')
    poem = bot.generate_ai_poem()
    
    if poem:
        print(f'✅ Generated poem: "{poem["title"]}" by {poem["author"]}')
        print(f'📝 Text preview: {poem["text"][:100]}...')
        
        # Create tweet
        tweet_text = bot.format_tweet_text(poem)
        print(f'🐦 Tweet preview ({len(tweet_text)} chars):')
        print('-' * 50)
        print(tweet_text)
        print('-' * 50)
        
        # Post to Twitter
        print('🚀 Posting to Twitter...')
        success = bot.post_to_twitter(poem)
        if success:
            print('✅ Successfully posted to Twitter!')
            return True
        else:
            print('❌ Twitter posting failed')
            return False
    else:
        print('❌ AI poem generation failed')
        return False

if __name__ == "__main__":
    test_twitter_post() 