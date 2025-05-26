# Twitter Poetry Bot - Quick Start Guide

## Current Status ✅
- **Real Poem Extraction**: ✅ Working (Poetry Foundation, Poetry Daily, etc.)
- **AI Poem Generation**: ✅ Working (OpenAI, Gemini, Claude)
- **Twitter Posting**: ✅ Working
- **Posting Frequency**: 🚀 **10 posts per day** (every 2.4 hours)

## Quick Test
```bash
python3 twitter_bot.py
```

## Posting Schedule (UTC)
- 06:00, 08:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00, 00:00
- **10 posts per day** with real poems from literary sources
- Up to 2 AI-generated poems per day when real poems unavailable

## Running Options

### 1. Single Post (Manual)
```bash
python3 twitter_bot.py
```

### 2. Run 10 Posts Immediately (Testing)
```bash
python3 run_10_posts.py
```
⚠️ This will post 10 times with 30-second delays

### 3. Automated Scheduler (Production)
```bash
python3 scheduler.py
```
🔄 Runs continuously, posting 10 times per day at scheduled times

## Dependencies Installed:
- tweepy (Twitter API)
- openai==1.82.0
- google-generativeai==0.8.5
- anthropic==0.52.0
- schedule==1.2.0 (for automated scheduling)
- All other dependencies up to date 