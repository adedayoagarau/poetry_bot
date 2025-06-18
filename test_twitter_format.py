#!/usr/bin/env python3
"""
Test different Twitter formatting options for poems
"""

def test_twitter_formats(poem):
    """Test different tweet formatting styles"""
    
    print("🐦 TWITTER FORMATTING OPTIONS")
    print("=" * 60)
    
    # Current format (from your TwitterPoetryBot)
    print("\n📱 CURRENT FORMAT:")
    print("-" * 30)
    tweet_text = f'"{poem["title"]}" by {poem["author"]}\n\n'
    max_poem_length = 280 - len(tweet_text) - 20
    if len(poem['text']) > max_poem_length:
        tweet_text += poem['text'][:max_poem_length] + "..."
    else:
        tweet_text += poem['text']
    print(tweet_text)
    print(f"Length: {len(tweet_text)} characters")
    
    # Compact format
    print("\n📱 COMPACT FORMAT:")
    print("-" * 30)
    compact = f'"{poem["title"]}" - {poem["author"]}\n\n{poem["text"][:200]}...'
    print(compact)
    print(f"Length: {len(compact)} characters")
    
    # Thread format (if poem is long)
    print("\n📱 THREAD FORMAT (if needed):")
    print("-" * 30)
    thread_start = f'🧵 THREAD: "{poem["title"]}" by {poem["author"]}\n\n{poem["text"][:180]}... (1/2)'
    print("Tweet 1:")
    print(thread_start)
    print(f"Length: {len(thread_start)} characters")
    
    remaining_text = poem["text"][180:]
    thread_end = f'...{remaining_text[:200]}\n\n#{poem["source"].replace(" ", "").replace(".", "")} #Poetry'
    print("\nTweet 2:")
    print(thread_end)
    print(f"Length: {len(thread_end)} characters")
    
    # Elegant format with hashtags
    print("\n📱 ELEGANT FORMAT WITH HASHTAGS:")
    print("-" * 30)
    elegant = f'"{poem["title"]}" by {poem["author"]}\n\n{poem["text"][:160]}...\n\n#Poetry #{poem["source"].replace(" ", "").replace(".", "")}'
    print(elegant)
    print(f"Length: {len(elegant)} characters")
    
    # Quote style
    print("\n📱 QUOTE STYLE:")
    print("-" * 30)
    quote = f'📜 "{poem["text"][:150]}..."\n\n— {poem["author"]}\nfrom "{poem["title"]}"\n\n#DailyPoetry #Literature'
    print(quote)
    print(f"Length: {len(quote)} characters")

# Test with the poem your bot just found
if __name__ == "__main__":
    # Use the Fernando Pessoa poem from your recent run
    test_poem = {
        "title": "Salute to Walt Whitman (excerpt)",
        "author": "Fernando Pessoa",
        "text": """Wherever I am not the first, I would prefer to be nothing, just not to be there at all,
Wherever I cannot be the first to take action, I prefer to watch others act.
Wherever I cannot be in command, I would prefer not even to obey.
I am so excessive in my desire for everything, so excessive that I never falter,
And I never do falter, because I never even try.
"All or Nothing" has a special meaning for me.
But I cannot be universal because I am individual.
I cannot be everyone because I am One, only one, only me.
I cannot be the first in anything, because there is no first.
I therefore prefer the nothing of being only that being nothing.""",
        "source": "Poetry Daily"
    }
    
    test_twitter_formats(test_poem)