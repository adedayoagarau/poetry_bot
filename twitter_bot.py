import os
from poetry_bot import PoetryBot

if __name__ == "__main__":
    print("🐦 Twitter Poetry Bot starting...")
    bot = PoetryBot()
    # Remove Instagram client if present
    if hasattr(bot, 'instagram'):
        delattr(bot, 'instagram')
    # Only run Twitter posting logic
    # (This will skip Instagram posting due to the guard in poetry_bot.py)
    bot.run()
    print("✅ Twitter Poetry Bot finished.") 