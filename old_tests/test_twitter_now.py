#!/usr/bin/env python3
"""
Quick Twitter test - Find and post real poem from literary sources
"""

from poetry_bot import PoetryBot

def test_twitter_post():
    print("🐦 Twitter Poetry Bot - Live Test")
    print("=" * 50)
    
    # Create bot
    bot = PoetryBot()
    
    # Get real poem from literary sources
    print('📚 Finding real poem from literary journals...')
    poem = bot.fetch_poem_from_journals()
    
    if poem:
        print(f'✅ Found poem: "{poem["title"]}" by {poem["author"]}')
        print(f'📍 Source: {poem["source"]}')
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
        print('❌ No real poems found from literary sources')
        print('🚫 AI generation is disabled - only real poems allowed')
        return False

if __name__ == "__main__":
    test_twitter_post() 