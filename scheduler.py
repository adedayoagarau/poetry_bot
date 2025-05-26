#!/usr/bin/env python3
"""
Twitter Poetry Bot Scheduler
Runs the bot 10 times per day at specified times
"""

import schedule
import time
import subprocess
import os
from datetime import datetime
from config import BOT_SETTINGS

def run_twitter_bot():
    """Run the Twitter poetry bot"""
    try:
        print(f"🤖 Starting Twitter Poetry Bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run the Twitter bot
        result = subprocess.run(['python3', 'twitter_bot.py'], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Twitter bot completed successfully")
            print(result.stdout)
        else:
            print("❌ Twitter bot failed")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error running Twitter bot: {e}")

def setup_schedule():
    """Set up the posting schedule"""
    post_times = BOT_SETTINGS.get('post_times_utc', ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00'])
    
    print(f"📅 Setting up schedule for {len(post_times)} posts per day")
    print(f"🕐 Post times (UTC): {', '.join(post_times)}")
    
    # Schedule each post time
    for post_time in post_times:
        schedule.every().day.at(post_time).do(run_twitter_bot)
        print(f"   ⏰ Scheduled post at {post_time} UTC")
    
    print("✅ Schedule setup complete!")

def main():
    """Main scheduler loop"""
    print("🚀 Twitter Poetry Bot Scheduler Starting...")
    print("=" * 50)
    
    # Set up the schedule
    setup_schedule()
    
    print("\n🔄 Scheduler running... Press Ctrl+C to stop")
    print("📊 Next scheduled runs:")
    
    # Show next few scheduled runs
    for job in schedule.jobs[:5]:
        print(f"   📅 {job.next_run}")
    
    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
            
    except KeyboardInterrupt:
        print("\n🛑 Scheduler stopped by user")
    except Exception as e:
        print(f"\n❌ Scheduler error: {e}")

if __name__ == "__main__":
    main() 