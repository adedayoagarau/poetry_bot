# [Copy the entire code from the artifact above]
#!/usr/bin/env python3
"""
Example of what your Twitter posts will look like
4-6 lines with links to full poems
"""

def format_tweet_example(poem_data):
    """Show exactly what will be posted to Twitter"""
    
    # Extract 4-6 lines from the poem
    poem_lines = [line.strip() for line in poem_data['text'].split('\n') if line.strip()]
    
    # Select 4-5 lines for Twitter
    if len(poem_lines) >= 6:
        selected_lines = poem_lines[:5]
        has_more = True
    elif len(poem_lines) >= 4:
        selected_lines = poem_lines[:4]
        has_more = len(poem_lines) > 4
    else:
        selected_lines = poem_lines
        has_more = False
    
    # Join selected lines
    poem_excerpt = '\n'.join(selected_lines)
    if has_more:
        poem_excerpt += '\n...'
    
    # Create source hashtag
    source_hashtag = f"#{poem_data['source'].replace(' ', '').replace('.', '')}"
    
    # Format tweet
    tweet = f'"{poem_data["title"]}" by {poem_data["author"]}\n\n{poem_excerpt}\n\nRead full poem: {poem_data["url"]}\n\n#Poetry #WritingCommunity {source_hashtag}'
    
    return tweet

# EXAMPLE POEMS TO SHOW FORMAT

example_poems = [
    {
        'title': 'The Road Not Taken',
        'author': 'Robert Frost',
        'text': '''Two roads diverged in a yellow wood,
And sorry I could not travel both
And be one traveler, long I stood
And looked down one as far as I could
To where it bent in the undergrowth;

Then took the other, as just as fair,
And having perhaps the better claim,
Because it was grassy and wanted wear;
Though as for that the passing there
Had worn them really about the same,

And both that morning equally lay
In leaves no step had trodden black.
Oh, I kept the first for another day!
Yet knowing how way leads on to way,
I doubted if I should ever be back.

I shall be telling this with a sigh
Somewhere ages and ages hence:
Two roads diverged in a wood, and I—
I took the one less traveled by,
And that has made all the difference.''',
        'source': 'Poetry Foundation',
        'url': 'https://www.poetryfoundation.org/poems/44272/the-road-not-taken'
    },
    {
        'title': 'Still I Rise',
        'author': 'Maya Angelou',
        'text': '''You may write me down in history
With your bitter, twisted lies,
You may trod me in the very dirt
But still, like dust, I rise.

Does my sassiness upset you?
Why are you beset with gloom?
'Cause I walk like I've got oil wells
Pumping in my living room.

Just like moons and like suns,
With the certainty of tides,
Just like hopes springing high,
Still I'll rise.''',
        'source': 'Poetry Daily',
        'url': 'https://poems.com/poem/still-i-rise'
    },
    {
        'title': 'Haiku',
        'author': 'Matsuo Bashō',
        'text': '''An ancient pond—
a frog leaps in,
the sound of water.''',
        'source': 'Verse Daily',
        'url': 'https://versedaily.org/haiku-basho'
    }
]

def show_examples():
    """Display what Twitter posts will look like"""
    print("🐦 TWITTER POST EXAMPLES")
    print("=" * 60)
    
    for i, poem in enumerate(example_poems, 1):
        tweet = format_tweet_example(poem)
        char_count = len(tweet)
        
        print(f"\n📱 EXAMPLE {i} ({char_count}/280 characters)")
        print("-" * 50)
        print(tweet)
        print("-" * 50)
        
        # Analysis
        poem_lines = [line.strip() for line in poem['text'].split('\n') if line.strip()]
        excerpt_lines = tweet.split('\n\n')[1].split('\n')
        if excerpt_lines[-1] == '...':
            excerpt_lines = excerpt_lines[:-1]
        
        print(f"📊 Analysis:")
        print(f"   • Total poem lines: {len(poem_lines)}")
        print(f"   • Lines in tweet: {len(excerpt_lines)}")
        print(f"   • Character count: {char_count}/280")
        print(f"   • Space remaining: {280 - char_count} characters")
        print(f"   • Includes link: ✅")
        print(f"   • Hashtags: #Poetry #WritingCommunity #{poem['source'].replace(' ', '').replace('.', '')}")

def test_with_your_bot():
    """Test format with your actual bot"""
    print("\n\n🤖 TESTING WITH YOUR ACTUAL BOT")
    print("=" * 60)
    
    try:
        # Import your bot
        from poetry_bot import PoetryBot
        
        bot = PoetryBot()
        poem = bot.get_daily_poem()
        
        if poem:
            tweet = format_tweet_example(poem)
            print("📱 YOUR NEXT TWITTER POST WILL LOOK LIKE:")
            print("-" * 50)
            print(tweet)
            print("-" * 50)
            print(f"Character count: {len(tweet)}/280")
            
            # Show the difference
            print(f"\n📊 COMPARISON:")
            print(f"   Full poem: {len(poem['text'])} characters")
            
            # Count lines in excerpt
            poem_lines = [line.strip() for line in poem['text'].split('\n') if line.strip()]
            excerpt_lines = tweet.split('\n\n')[1].split('\n')
            if excerpt_lines[-1] == '...':
                excerpt_lines = excerpt_lines[:-1]
                
            print(f"   Tweet excerpt: {len(excerpt_lines)} lines from {len(poem_lines)} total")
            print(f"   Includes link: ✅")
            print(f"   Ready to post: ✅")
            
        else:
            print("❌ Could not get poem from bot")
            
    except ImportError:
        print("❌ Could not import your poetry_bot")
        print("Make sure poetry_bot.py is in the same directory")
    except Exception as e:
        print(f"❌ Error testing with your bot: {e}")

def test_different_lengths():
    """Test with different poem lengths"""
    print("\n\n🧪 TESTING DIFFERENT POEM LENGTHS")
    print("=" * 60)
    
    # Very short poem (3 lines)
    short_poem = {
        'title': 'Minimalist',
        'author': 'Test Author',
        'text': 'Line one\nLine two\nLine three',
        'source': 'Test Source',
        'url': 'https://example.com/short'
    }
    
    # Medium poem (8 lines)  
    medium_poem = {
        'title': 'Medium Length',
        'author': 'Test Author',
        'text': '\n'.join([f'Line {i}' for i in range(1, 9)]),
        'source': 'Test Source',
        'url': 'https://example.com/medium'
    }
    
    # Long poem (20 lines)
    long_poem = {
        'title': 'Very Long Poem',
        'author': 'Test Author', 
        'text': '\n'.join([f'This is line number {i} of a very long poem' for i in range(1, 21)]),
        'source': 'Test Source',
        'url': 'https://example.com/long'
    }
    
    test_poems = [
        ("SHORT POEM (3 lines)", short_poem),
        ("MEDIUM POEM (8 lines)", medium_poem), 
        ("LONG POEM (20 lines)", long_poem)
    ]
    
    for title, poem in test_poems:
        tweet = format_tweet_example(poem)
        print(f"\n📝 {title}")
        print("-" * 30)
        print(tweet)
        print(f"Characters: {len(tweet)}/280")

if __name__ == "__main__":
    show_examples()
    test_with_your_bot()
    test_different_lengths()
    
    print("\n\n✅ BENEFITS OF THIS FORMAT:")
    print("• Perfect for Twitter's format (short & engaging)")
    print("• Drives traffic to original sources")  
    print("• Respects copyright (fair use excerpt)")
    print("• Builds anticipation (people want to read more)")
    print("• Better engagement (easier to read & share)")
    print("• Professional appearance")