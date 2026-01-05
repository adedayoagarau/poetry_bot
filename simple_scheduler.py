#!/usr/bin/env python3
"""
Simple scheduler for the new poetry bot.
Runs once per day at specified time.
"""

import schedule
import time
import subprocess
from datetime import datetime


def run_bot():
    """Run the poetry bot"""
    print(f"\n{'='*60}")
    print(f"🕐 Running Poetry Bot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    try:
        # Run bot in live mode
        result = subprocess.run(
            ['python', 'bot.py', '--live'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ Bot completed successfully")
            print(result.stdout)
        else:
            print("❌ Bot failed")
            print(result.stderr)

    except Exception as e:
        print(f"❌ Error running bot: {e}")


def main():
    """Main scheduler loop"""
    # Post time (9am EST = 14:00 UTC)
    post_time = "14:00"

    print("🤖 Poetry Bot Scheduler Starting...")
    print(f"⏰ Will post daily at {post_time} UTC (9am EST)")
    print("🔄 Press Ctrl+C to stop\n")

    # Schedule the job
    schedule.every().day.at(post_time).do(run_bot)

    # Show next run
    next_run = schedule.jobs[0].next_run
    print(f"📅 Next post scheduled for: {next_run}\n")

    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler stopped by user")


if __name__ == "__main__":
    main()
