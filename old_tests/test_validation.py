#!/usr/bin/env python3
"""
Simple test script for poem validation
"""

from debug_poetry_extraction import debug_poem_extraction

def test_working_urls():
    """Test some working poem URLs"""
    test_urls = [
        "https://poems.com/poem/daughter/",
        "https://poems.com/poem/ahshinayo/",
        "https://poems.com/todays-poem/"
    ]
    
    for url in test_urls:
        print(f"\n{'='*80}")
        print(f"TESTING: {url}")
        print('='*80)
        
        poem = debug_poem_extraction(url, 'Poetry Daily')
        
        print(f"\n{'='*50}")
        print("FINAL RESULT:")
        print(f"Success: {poem is not None}")
        if poem:
            print(f"Title: {poem['title']}")
            print(f"Author: {poem['author']}")
            print(f"Text length: {len(poem['text'])} chars")
            print(f"First 200 chars: {poem['text'][:200]}...")
        print('='*50)

if __name__ == "__main__":
    test_working_urls() 