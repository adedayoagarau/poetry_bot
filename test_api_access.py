#!/usr/bin/env python3
"""
Test Twitter API v2 access and permissions
"""

import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def test_twitter_access():
    print("🔍 Testing Twitter API v2 Access")
    print("=" * 50)
    
    try:
        # Test v2 client
        client = tweepy.Client(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            wait_on_rate_limit=True
        )
        
        print("✅ Twitter API v2 client created successfully")
        
        # Test reading (should work with free tier)
        try:
            me = client.get_me()
            if me.data:
                print(f"✅ Read access confirmed - User: @{me.data.username}")
            else:
                print("❌ Read access failed - no user data")
        except Exception as e:
            print(f"❌ Read access failed: {e}")
        
        # Test write access (this is what we need to fix)
        print("\n🔍 Testing write permissions...")
        try:
            # Try to create a test tweet (we'll delete it immediately)
            test_tweet = "🤖 Testing Poetry Bot API access - will delete shortly"
            response = client.create_tweet(text=test_tweet)
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✅ Write access confirmed - Test tweet created: {tweet_id}")
                
                # Delete the test tweet
                try:
                    client.delete_tweet(tweet_id)
                    print("✅ Test tweet deleted successfully")
                except:
                    print("⚠️  Test tweet created but couldn't delete - please delete manually")
                
                return True
            else:
                print("❌ Write access failed - no response data")
                return False
                
        except Exception as e:
            print(f"❌ Write access failed: {e}")
            print("\n💡 This usually means:")
            print("   1. App permissions are set to 'Read' only")
            print("   2. Access tokens need to be regenerated after permission change")
            print("   3. App may need elevated access for posting")
            return False
            
    except Exception as e:
        print(f"❌ Twitter API connection failed: {e}")
        return False

# Load credentials from environment variables
consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Authenticate with Twitter API v1.1 (for posting tweets)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

try:
    tweet_text = "Test tweet from poetry bot (manual API test). #PoetryBotTest"
    tweet = api.update_status(tweet_text)
    print(f"✅ Successfully posted test tweet! Tweet ID: {tweet.id}")
    print(f"Tweet URL: https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}")
except Exception as e:
    print(f"❌ Failed to post tweet: {e}")

if __name__ == "__main__":
    test_twitter_access() 