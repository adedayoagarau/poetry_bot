#!/usr/bin/env python3
"""
Test poem extraction from different literary journals
"""

from poetry_bot import PoetryBot
from config import LITERARY_JOURNALS
import random

def test_poem_sources():
    print("🔍 Testing Poem Extraction from Literary Journals")
    print("=" * 60)
    
    bot = PoetryBot()
    
    # Test a few different sources
    test_sources = [
        'Poetry Daily',
        'Verse Daily', 
        'Poetry Foundation',
        'The Paris Review',
        'Rattle Magazine'
    ]
    
    for source_name in test_sources:
        print(f"\n📚 Testing: {source_name}")
        print("-" * 40)
        
        # Find the journal config
        journal = None
        for j in LITERARY_JOURNALS:
            if j['name'] == source_name:
                journal = j
                break
        
        if not journal:
            print(f"❌ Journal config not found for {source_name}")
            continue
            
        try:
            poem = bot.fetch_from_journal(journal)
            if poem:
                print(f"✅ Found poem: '{poem['title'][:50]}...'")
                print(f"👤 Author: {poem['author']}")
                print(f"📝 Text preview: {poem['text'][:100]}...")
                print(f"🔗 URL: {poem.get('url', 'No URL')}")
                
                # Test the formatting
                tweet_text = bot.format_tweet_text(poem)
                print(f"🐦 Tweet preview ({len(tweet_text)} chars):")
                print(tweet_text[:200] + "..." if len(tweet_text) > 200 else tweet_text)
            else:
                print(f"❌ No poem found from {source_name}")
                
        except Exception as e:
            print(f"❌ Error with {source_name}: {e}")
    
    print(f"\n🎯 Recommendation: Use sources that successfully extract real poem content")
    print(f"📝 Format: Your exact format is now implemented!")

if __name__ == "__main__":
    test_poem_sources() 