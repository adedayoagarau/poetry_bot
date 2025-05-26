#!/usr/bin/env python3
"""
Test tweet validation issue
"""

from poetry_bot import PoetryBot

def test_tweet_validation():
    """Test the tweet validation with the extracted poem"""
    
    # Sample poem data from the extraction
    poem_data = {
        'title': 'After the Operation (extract)',
        'author': 'Elizabeth T. Gray',
        'text': '''(After the operation,
intact
abandoned
its nouns, the idea
itself fell
apart and was
last seen somewhere
in an enamel
bowl in pieces
next to a bone saw)
We came upon her at dusk
in a dense forest
of monitors
draped cuffs, dangling
salines, tapes, drains
broad bandages, electrodes
We tried not to be terrified
and failed
We looked to her as we always had
We tried to tell her she looked fine
Because she could not see herself
she tried to put us at ease
We asked her how she felt, really
She was very calm (the meds)
"I was worried," she said
"but nothing has changed. Listen,
beyond the windows:
the creak of bullock carts
breaking waves, crows,
the call to prayer."''',
        'source': 'Poetry Daily',
        'url': 'https://poems.com/todays-poem/'
    }
    
    bot = PoetryBot()
    
    # Test the striking lines selection
    print("=== TESTING STRIKING LINES SELECTION ===")
    striking_lines = bot.select_striking_lines(poem_data['text'])
    print(f"Selected striking lines:\n{striking_lines}")
    
    # Test the tweet formatting
    print("\n=== TESTING TWEET FORMATTING ===")
    tweet_text = bot.format_tweet_text(poem_data)
    print(f"Formatted tweet ({len(tweet_text)} chars):")
    print("-" * 50)
    print(tweet_text)
    print("-" * 50)
    
    # Test the validation
    print("\n=== TESTING TWEET VALIDATION ===")
    is_valid, message = bot.validate_tweet_content(tweet_text, poem_data, poem_data['url'])
    print(f"Validation result: {is_valid}")
    print(f"Validation message: {message}")
    
    if not is_valid:
        print("\n=== DEBUGGING VALIDATION FAILURE ===")
        
        # Check what significant words are being looked for
        poem_text = poem_data['text'].lower()
        tweet_lower = tweet_text.lower()
        
        poem_words = [word.strip('.,!?;:"()[]') for word in poem_text.split() if len(word) > 3]
        significant_words = [word for word in poem_words if word not in ['the', 'and', 'but', 'for', 'with', 'from', 'that', 'this', 'they', 'have', 'been', 'were', 'said']]
        
        print(f"First 10 significant words from poem: {significant_words[:10]}")
        print(f"Tweet text (lowercase): {tweet_lower}")
        
        # Check which words are found
        found_words = [word for word in significant_words[:5] if word in tweet_lower]
        print(f"Significant words found in tweet: {found_words}")
        
        if not found_words:
            print("❌ No significant words from poem found in tweet!")
            print("This is why validation is failing.")

if __name__ == "__main__":
    test_tweet_validation() 