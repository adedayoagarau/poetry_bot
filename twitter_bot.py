import os
from poetry_bot import TwitterPoetryBot

if __name__ == "__main__":
    print("🐦 Twitter Poetry Bot starting...")
    bot = TwitterPoetryBot()  # ← This was the issue!
    # Run Twitter posting logic
    bot.run()
    print("✅ Twitter Poetry Bot finished.")