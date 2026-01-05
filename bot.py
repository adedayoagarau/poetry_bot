#!/usr/bin/env python3
"""
Main Poetry Bot - Clean, reliable, quality-focused.
"""

import os
from typing import Optional
from pathlib import Path
from sources import PoetryDailySource, Poem
from validators import ContentValidator
from formatters import TwitterFormatter
from storage import PostedTracker


def ensure_directories():
    """Create necessary directories if they don't exist"""
    Path('data').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    Path('docs').mkdir(exist_ok=True)


class PoetryBot:
    """Main bot orchestrator"""

    def __init__(self, preview_mode: bool = True):
        """
        Initialize bot.

        Args:
            preview_mode: If True, don't post to Twitter (just preview)
        """
        # Ensure directories exist
        ensure_directories()

        self.preview_mode = preview_mode
        self.validator = ContentValidator()
        self.formatter = TwitterFormatter()
        self.tracker = PostedTracker()

        # Initialize sources
        self.sources = [
            PoetryDailySource(),
        ]

        print(f"🤖 Poetry Bot initialized")
        print(f"📍 Mode: {'PREVIEW' if preview_mode else 'LIVE POSTING'}")
        print(f"📚 Sources: {[s.name for s in self.sources]}")
        print(f"💾 Posted poems: {len(self.tracker.posted_urls)}")

    def get_poem(self) -> Optional[Poem]:
        """
        Get a valid, unposted poem from sources.

        Returns:
            Poem object or None if unable to find valid poem
        """
        for source in self.sources:
            print(f"\n🔍 Checking {source.name}...")

            try:
                poem = source.get_daily_poem()

                if not poem:
                    print(f"❌ No poem from {source.name}")
                    continue

                # Check if already posted
                if self.tracker.has_posted(poem):
                    print(f"⏭️  Already posted: '{poem.title}'")
                    continue

                # Validate content
                is_valid, reason = self.validator.validate(poem)

                if not is_valid:
                    print(f"❌ Validation failed: {reason}")
                    print(f"   Title: {poem.title}")
                    print(f"   Author: {poem.author}")
                    print(f"   URL: {poem.source_url}")
                    continue

                # Success!
                print(f"✅ Valid poem found!")
                print(f"   Title: {poem.title}")
                print(f"   Author: {poem.author}")
                print(f"   Lines: {poem.line_count()}")
                print(f"   Words: {poem.word_count()}")

                return poem

            except Exception as e:
                print(f"❌ Error with {source.name}: {e}")
                continue

        print("\n❌ No valid poems found from any source")
        return None

    def preview_poem(self, poem: Poem):
        """Preview how poem would be posted"""
        preview = self.formatter.preview_tweet(poem)

        print("\n" + "=" * 60)
        print("📱 TWEET PREVIEW")
        print("=" * 60)
        print(preview['tweet'])
        print("=" * 60)
        print(f"📊 Length: {preview['length']}/{self.formatter.MAX_TWEET_LENGTH} chars")
        print(f"📝 Lines: {preview['lines_used']}/{preview['total_lines']}")
        if preview['is_truncated']:
            print(f"✂️  Truncated: Yes (full poem at link)")
        print("=" * 60)

    def post_poem(self, poem: Poem) -> bool:
        """
        Post poem to Twitter.

        Returns:
            True if posted successfully, False otherwise
        """
        try:
            import tweepy

            # Load environment variables from .env if present
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass  # python-dotenv not installed, use system env vars

            # Get credentials
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

            if not all([api_key, api_secret, access_token, access_token_secret]):
                print("❌ Missing Twitter API credentials")
                print("   Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET")
                return False

            # Create client
            client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )

            # Verify authentication
            me = client.get_me()
            print(f"✅ Authenticated as @{me.data.username}")

            # Format tweet
            tweet_text = self.formatter.format_tweet(poem)

            # Post
            response = client.create_tweet(text=tweet_text)
            tweet_id = response.data['id']
            tweet_url = f"https://twitter.com/{me.data.username}/status/{tweet_id}"

            print(f"🎉 Posted successfully!")
            print(f"🔗 {tweet_url}")

            # Mark as posted
            self.tracker.mark_posted(poem, tweet_url)

            return True

        except ImportError:
            print("❌ tweepy not installed. Run: pip install tweepy")
            return False

        except Exception as e:
            print(f"❌ Error posting to Twitter: {e}")
            return False

    def run(self) -> bool:
        """
        Main bot execution.

        Returns:
            True if successful, False otherwise
        """
        print("\n" + "🚀 " * 20)
        print("Poetry Bot Starting...")
        print("🚀 " * 20)

        # Get poem
        poem = self.get_poem()

        if not poem:
            print("\n❌ Failed to get valid poem")
            return False

        # Preview
        self.preview_poem(poem)

        # Post (if not in preview mode)
        if not self.preview_mode:
            print("\n📤 Posting to Twitter...")
            success = self.post_poem(poem)
            return success
        else:
            print("\n👁️  Preview mode - not posting to Twitter")
            print("💡 Run with preview_mode=False to post")

            # Still mark as posted in preview mode to avoid re-previewing
            self.tracker.mark_posted(poem)

            return True


def main():
    """CLI entry point"""
    import sys

    # Check if --live flag is provided
    preview_mode = '--live' not in sys.argv

    if preview_mode:
        print("👁️  Running in PREVIEW mode (use --live to post)")
    else:
        print("⚠️  Running in LIVE mode - will post to Twitter!")

    bot = PoetryBot(preview_mode=preview_mode)
    success = bot.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
