cat > .github/workflows/daily-poetry.yml << 'EOF'
name: Ultra-Frequent Poetry Bot - 16 Posts Daily

on:
  schedule:
    # 16 posts per day - every 1.5 hours around the clock
    - cron: '0 0 * * *'    # 12:00 AM UTC
    - cron: '30 1 * * *'   # 1:30 AM UTC
    - cron: '0 3 * * *'    # 3:00 AM UTC
    - cron: '30 4 * * *'   # 4:30 AM UTC
    - cron: '0 6 * * *'    # 6:00 AM UTC
    - cron: '30 7 * * *'   # 7:30 AM UTC
    - cron: '0 9 * * *'    # 9:00 AM UTC
    - cron: '30 10 * * *'  # 10:30 AM UTC
    - cron: '0 12 * * *'   # 12:00 PM UTC
    - cron: '30 13 * * *'  # 1:30 PM UTC
    - cron: '0 15 * * *'   # 3:00 PM UTC
    - cron: '30 16 * * *'  # 4:30 PM UTC
    - cron: '0 18 * * *'   # 6:00 PM UTC
    - cron: '30 19 * * *'  # 7:30 PM UTC
    - cron: '0 21 * * *'   # 9:00 PM UTC
    - cron: '30 22 * * *'  # 10:30 PM UTC
  workflow_dispatch:       # Manual trigger
  push:
    branches: [main]       # Test on push

jobs:
  post-poetry:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4 tweepy
        
    - name: Run Twitter Poetry Bot
      env:
        TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
        TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
        TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
        TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
      run: |
        echo "🐦 Running Twitter Poetry Bot - Ultra-frequent posting!"
        echo "📅 Current time: $(date -u)"
        echo "🎯 16 posts per day schedule"
        python twitter_bot.py
        
    - name: Log execution
      if: always()
      run: |
        echo "✅ Poetry post completed"
        echo "📊 Next post in ~1.5 hours"
        echo "📅 Execution time: $(date -u)"
EOF