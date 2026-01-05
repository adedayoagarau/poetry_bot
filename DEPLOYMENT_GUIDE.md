# Deployment Guide - Poetry Bot

## Step 1: Merge Your Branch

Since there's no main branch yet, let's create one from your current work:

```bash
# Create and push main branch from current work
git checkout -b main
git push -u origin main

# Or if you want to merge into an existing default branch:
# git checkout main  # or master
# git merge claude/poetry-bot-daily-publish-011CUiLEg8eyQGvfYPV9Bkuv
# git push origin main
```

After this, set `main` as your default branch on GitHub:
1. Go to your repo on GitHub
2. Settings → Branches
3. Set "main" as default branch

---

## Step 2: Set Up Automated Posting

You have two options: **GitHub Actions** (recommended) or **Traditional Cron Job** (server-based).

---

## Option A: GitHub Actions (Recommended) ⭐

**Why GitHub Actions?**
- ✅ Free (2,000 minutes/month on public repos)
- ✅ No server needed
- ✅ Automatic updates when you push code
- ✅ Easy to monitor and debug
- ✅ Built-in secret management

### Setup Instructions

#### 1. Create GitHub Actions Workflow

Create this file in your repo:

**.github/workflows/daily-poem.yml**

```yaml
name: Post Daily Poem

on:
  # Run daily at 9am EST (14:00 UTC)
  schedule:
    - cron: '0 14 * * *'

  # Allow manual trigger for testing
  workflow_dispatch:

jobs:
  post-poem:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Post daily poem
        env:
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          TWITTER_API_SECRET: ${{ secrets.TWITTER_API_SECRET }}
          TWITTER_ACCESS_TOKEN: ${{ secrets.TWITTER_ACCESS_TOKEN }}
          TWITTER_ACCESS_TOKEN_SECRET: ${{ secrets.TWITTER_ACCESS_TOKEN_SECRET }}
          TWITTER_BEARER_TOKEN: ${{ secrets.TWITTER_BEARER_TOKEN }}
        run: |
          python bot.py --live

      - name: Commit updated posted_poems.json
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add data/posted_poems.json
          git diff --quiet && git diff --staged --quiet || git commit -m "Update posted poems [skip ci]"
          git push
```

#### 2. Add Secrets to GitHub

1. Go to your repo on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each of these secrets:

```
Name: TWITTER_API_KEY
Value: [your API key from Twitter Developer Portal]

Name: TWITTER_API_SECRET
Value: [your API secret]

Name: TWITTER_ACCESS_TOKEN
Value: [your access token]

Name: TWITTER_ACCESS_TOKEN_SECRET
Value: [your access token secret]

Name: TWITTER_BEARER_TOKEN
Value: [your bearer token]
```

#### 3. Enable GitHub Actions

1. Go to **Actions** tab in your repo
2. Click "I understand my workflows, go ahead and enable them"

#### 4. Test Manually

1. Go to **Actions** tab
2. Click "Post Daily Poem" workflow
3. Click "Run workflow" → "Run workflow"
4. Watch it run in real-time
5. Check Twitter to verify post

#### 5. Monitor

- Workflow runs automatically at 9am EST daily
- Check **Actions** tab to see history
- Email notifications if workflow fails
- View logs for debugging

### Schedule Customization

```yaml
# Change the cron schedule:
schedule:
  # 9am EST (14:00 UTC)
  - cron: '0 14 * * *'

  # Multiple times per day:
  - cron: '0 14 * * *'  # 9am EST
  - cron: '0 18 * * *'  # 1pm EST
  - cron: '0 22 * * *'  # 5pm EST
```

**Cron Format**: `minute hour day month day-of-week`
- `0 14 * * *` = 14:00 UTC daily = 9am EST
- Use [Crontab Guru](https://crontab.guru/) to test schedules

---

## Option B: Traditional Cron Job (Server-Based)

**When to use this:**
- You have a server running 24/7
- You want more control
- You have private repo (GitHub Actions limits)

### Setup Instructions

#### 1. Clone Repo on Server

```bash
# SSH into your server
ssh your-server

# Clone repo
git clone https://github.com/your-username/poetry_bot.git
cd poetry_bot

# Checkout main branch
git checkout main
```

#### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

#### 3. Set Up Environment Variables

```bash
# Create .env file
nano .env

# Add your credentials:
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Save and exit (Ctrl+O, Enter, Ctrl+X)

# Protect the file
chmod 600 .env
```

#### 4. Test Manually

```bash
# Test in preview mode first
python bot.py

# If looks good, test live posting
python bot.py --live

# Check Twitter to verify
```

#### 5. Set Up Cron Job

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9am server time):
0 9 * * * cd /path/to/poetry_bot && /path/to/poetry_bot/venv/bin/python /path/to/poetry_bot/bot.py --live >> /path/to/poetry_bot/logs/cron.log 2>&1

# Example with actual paths:
0 9 * * * cd /home/user/poetry_bot && /home/user/poetry_bot/venv/bin/python /home/user/poetry_bot/bot.py --live >> /home/user/poetry_bot/logs/cron.log 2>&1
```

**Important Notes:**
- Use **absolute paths** (not ~/), cron doesn't expand ~
- Redirect output to log file for debugging
- Ensure script has execute permissions

#### 6. Verify Cron Job

```bash
# List cron jobs
crontab -l

# Check if cron service is running
sudo systemctl status cron

# Monitor logs
tail -f logs/cron.log
```

#### 7. Common Cron Schedules

```bash
# Daily at 9am
0 9 * * * [command]

# Three times a day (9am, 1pm, 5pm)
0 9,13,17 * * * [command]

# Every 4 hours
0 */4 * * * [command]

# Monday-Friday at 9am
0 9 * * 1-5 [command]
```

---

## Option C: Hybrid Approach

Use GitHub Actions for posting + manual server for development:

**GitHub Actions**: Automated daily posting
**Your Server**: Development, testing, manual runs

This gives you:
- ✅ Reliable automated posting (GitHub)
- ✅ Local testing environment
- ✅ Manual override when needed

---

## Monitoring & Maintenance

### GitHub Actions Monitoring

1. **Check Workflow Runs**:
   - Go to Actions tab
   - See green ✅ or red ❌
   - Click to view logs

2. **Email Notifications**:
   - Settings → Notifications → Actions
   - Get email on failure

3. **View Logs**:
   ```
   Actions → Select run → Click job → View logs
   ```

### Cron Job Monitoring

1. **Check Logs**:
   ```bash
   tail -f logs/cron.log
   ```

2. **Check Posted Poems**:
   ```bash
   cat data/posted_poems.json | jq '.poems[-5:]'
   ```

3. **Check Last Run**:
   ```bash
   ls -lh data/posted_poems.json  # See last modified time
   ```

---

## Troubleshooting

### GitHub Actions Issues

**Workflow not running?**
- Check Actions tab is enabled
- Verify cron syntax with Crontab Guru
- Check repo permissions

**Authentication failed?**
- Verify secrets are set correctly
- Check Twitter API credentials
- Ensure Twitter app has write permissions

**Import errors?**
- Check requirements.txt is up to date
- Verify Python version (3.11)

### Cron Job Issues

**Job not running?**
- Check cron service: `sudo systemctl status cron`
- Verify crontab: `crontab -l`
- Check logs: `tail -f logs/cron.log`

**Path errors?**
- Use absolute paths (not ~/)
- Check working directory exists
- Verify virtual environment path

**Permission errors?**
- Check file permissions: `ls -la`
- Ensure .env is readable
- Check data/ directory exists

---

## Updating the Bot

### GitHub Actions (Automatic)

```bash
# Make changes locally
git add .
git commit -m "Update bot"
git push origin main

# GitHub Actions automatically uses latest code
# Next scheduled run will use new version
```

### Cron Job (Manual)

```bash
# SSH to server
ssh your-server
cd poetry_bot

# Pull latest changes
git pull origin main

# Update dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# Cron will use new version on next run
```

---

## Testing Before Going Live

### Test Schedule

**Week 1**: Preview mode only
```bash
# Manually run and review output
python bot.py
```

**Week 2**: One live post manually
```bash
# Post once, monitor engagement
python bot.py --live
```

**Week 3**: Enable automation
- Set up GitHub Actions OR cron
- Monitor daily for 1 week
- Verify quality

**Week 4+**: Fully automated
- Check weekly for issues
- Review engagement metrics
- Adjust schedule if needed

---

## Recommended Schedule

**Starting Out** (Week 1-4):
```yaml
# Once daily at 9am EST
- cron: '0 14 * * *'
```

**After Success** (Month 2+):
```yaml
# Twice daily
- cron: '0 14 * * *'  # 9am EST
- cron: '0 22 * * *'  # 5pm EST
```

**Mature Bot** (Month 3+):
```yaml
# Three times daily
- cron: '0 14 * * *'  # 9am EST
- cron: '0 18 * * *'  # 1pm EST
- cron: '0 22 * * *'  # 5pm EST
```

---

## Quick Start Checklist

### GitHub Actions Setup
- [ ] Create `.github/workflows/daily-poem.yml`
- [ ] Add secrets to GitHub repo
- [ ] Enable GitHub Actions
- [ ] Test manual run
- [ ] Monitor first automatic run
- [ ] Check posted poems on Twitter

### Cron Job Setup
- [ ] Clone repo to server
- [ ] Install dependencies
- [ ] Create .env file
- [ ] Test bot manually
- [ ] Set up crontab
- [ ] Monitor logs
- [ ] Verify first automatic post

---

## Support

**Issues?**
- Check logs first
- Review troubleshooting section
- Test manually to isolate issue
- Check Twitter API status

**Questions?**
- Review documentation in docs/
- Check bot.py comments
- Test in preview mode first

---

## Next Steps

1. **Choose your approach** (GitHub Actions recommended)
2. **Follow setup instructions** above
3. **Test in preview mode** for 1 week
4. **Enable live posting** when confident
5. **Monitor daily** for first month
6. **Refine as needed** based on engagement

**Your bot is ready to share beautiful poetry with the world!** 📖✨
