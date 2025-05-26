import os
from poetry_bot import PoetryBot

if __name__ == "__main__":
    print("🐦 Twitter Poetry Bot starting...")
    bot = PoetryBot()
    # Run Twitter posting logic
    bot.run()
    print("✅ Twitter Poetry Bot finished.") 