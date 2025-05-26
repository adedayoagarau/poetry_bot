#!/usr/bin/env python3
"""
Run 10 Twitter Posts Immediately
For testing the increased posting frequency
"""

import time
import subprocess
import os
from datetime import datetime

def run_single_post(post_number):
    """Run a single Twitter post"""
    try:
        print(f"🤖 Running post {post_number}/10 at {datetime.now().strftime('%H:%M:%S')}")
        
        # Run the Twitter bot
        result = subprocess.run(['python3', 'twitter_bot.py'], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print(f"✅ Post {post_number} completed successfully")
            if result.stdout:
                # Show only the last few lines to avoid spam
                lines = result.stdout.strip().split('\n')
                for line in lines[-3:]:
                    if line.strip():
                        print(f"   {line}")
        else:
            print(f"❌ Post {post_number} failed")
            print(f"   Error: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Error running post {post_number}: {e}")

def main():
    """Run 10 posts with delays"""
    print("🚀 Running 10 Twitter Posts")
    print("=" * 40)
    print("⚠️  This will post 10 times to Twitter!")
    print("⏱️  Each post will have a 30-second delay")
    print()
    
    # Confirm before running
    response = input("Continue? (y/N): ").lower().strip()
    if response != 'y':
        print("❌ Cancelled by user")
        return
    
    print("\n🔄 Starting posts...")
    
    for i in range(1, 11):
        run_single_post(i)
        
        # Add delay between posts (except after the last one)
        if i < 10:
            print(f"⏳ Waiting 30 seconds before next post...\n")
            time.sleep(30)
    
    print("\n🎉 All 10 posts completed!")
    print("📊 Check your Twitter account to verify posts")

if __name__ == "__main__":
    main() 