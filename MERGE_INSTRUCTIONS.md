# How to Merge and Deploy

## ✅ All Code is Pushed!

Your branch `claude/poetry-bot-daily-publish-011CUiLEg8eyQGvfYPV9Bkuv` contains all the complete, production-ready code.

---

## Step 1: Create Main Branch (On GitHub)

Since pushes are restricted to `claude/*` branches, you'll need to create the main branch on GitHub:

### Option A: Using GitHub Web Interface (Easiest)

1. **Go to your repo on GitHub**: `https://github.com/adedayoagarau/poetry_bot`

2. **Go to Settings → Branches**

3. **Create branch protection rule** (optional but recommended):
   - Branch name pattern: `main`
   - Click "Create"

4. **Manually create main branch**:
   - Go to your repo homepage
   - Click the branch dropdown (currently shows your claude/* branch)
   - Type "main" in the search box
   - Click "Create branch: main from 'claude/poetry-bot-daily-publish-011CUiLEg8eyQGvfYPV9Bkuv'"

5. **Set main as default**:
   - Settings → Branches → Default branch
   - Change to "main"
   - Confirm

### Option B: Using GitHub CLI (if installed)

```bash
# If you have gh CLI installed
gh repo set-default adedayoagarau/poetry_bot

# Create main branch from current branch
gh api repos/adedayoagarau/poetry_bot/git/refs \
  -f ref='refs/heads/main' \
  -f sha="$(git rev-parse claude/poetry-bot-daily-publish-011CUiLEg8eyQGvfYPV9Bkuv)"

# Set as default
gh repo edit --default-branch main
```

---

## Step 2: Set Up Automated Posting

Once main branch is created, choose your deployment method:

### 🌟 GitHub Actions (Recommended)

**Already included in your code!** File: `.github/workflows/daily-poem.yml`

#### Setup:

1. **Add Twitter API secrets** to your GitHub repo:
   - Go to repo → **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Add each:
     - `TWITTER_API_KEY`
     - `TWITTER_API_SECRET`
     - `TWITTER_ACCESS_TOKEN`
     - `TWITTER_ACCESS_TOKEN_SECRET`
     - `TWITTER_BEARER_TOKEN`

2. **Enable GitHub Actions**:
   - Go to **Actions** tab
   - Click "I understand my workflows, go ahead and enable them"

3. **Test manually**:
   - Actions → "Post Daily Poem" → "Run workflow"
   - Watch it run
   - Check Twitter to verify

4. **Done!** Runs automatically at 9am EST daily

#### How it works:

```yaml
# Runs daily at 9am EST (14:00 UTC)
schedule:
  - cron: '0 14 * * *'

# Posts poem
run: python bot.py --live

# Commits updated posted_poems.json
git add data/posted_poems.json
git commit && git push
```

---

### 🖥️ Traditional Cron Job (Alternative)

If you prefer running on your own server:

```bash
# 1. Clone on your server
git clone https://github.com/adedayoagarau/poetry_bot.git
cd poetry_bot
git checkout main

# 2. Set up Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create .env with Twitter credentials
cp .env.example .env
nano .env  # Add your credentials

# 4. Test
python bot.py         # Preview
python bot.py --live  # Live (once)

# 5. Set up cron
crontab -e

# Add this line (adjust paths):
0 9 * * * cd /full/path/to/poetry_bot && /full/path/to/poetry_bot/venv/bin/python /full/path/to/poetry_bot/bot.py --live >> /full/path/to/poetry_bot/logs/cron.log 2>&1
```

---

## Step 3: Monitor

### GitHub Actions
- Check **Actions** tab for workflow runs
- Green ✅ = success
- Red ❌ = check logs
- Email notifications on failure

### Cron Job
```bash
# Check logs
tail -f logs/cron.log

# Check posted poems
cat data/posted_poems.json | tail -20
```

---

## Quick Reference

### Cron Schedule Examples

```bash
# Daily at 9am
0 9 * * * [command]

# Twice daily (9am, 5pm)
0 9,17 * * * [command]

# Every 4 hours
0 */4 * * * [command]

# Mon-Fri at 9am only
0 9 * * 1-5 [command]
```

**Test schedules**: https://crontab.guru/

---

## Your Files

All deployment files are ready:

```
poetry_bot/
├── .github/workflows/
│   └── daily-poem.yml          ✅ GitHub Actions workflow
│
├── DEPLOYMENT_GUIDE.md         ✅ Full deployment guide
├── QUICK_START.md              ✅ Quick setup instructions
├── MERGE_INSTRUCTIONS.md       ✅ This file
│
├── bot.py                      ✅ Main bot (ready to run)
├── .env.example                ✅ Credentials template
└── requirements.txt            ✅ Dependencies
```

---

## Checklist

Branch Setup:
- [ ] Create `main` branch on GitHub
- [ ] Set `main` as default branch
- [ ] Verify all code is there

Twitter API:
- [ ] Get credentials from developer.twitter.com
- [ ] Test credentials work
- [ ] Add to GitHub Secrets OR .env file

Deployment:
- [ ] Choose GitHub Actions OR cron job
- [ ] Follow setup for chosen method
- [ ] Test with manual run
- [ ] Verify post on Twitter

Monitoring:
- [ ] Check first automated post works
- [ ] Set up notification/monitoring
- [ ] Review posts for first week

---

## Testing Workflow

**Week 1**: Preview only
```bash
python bot.py  # Run manually, review output
```

**Week 2**: One test post
```bash
python bot.py --live  # Post once, check quality
```

**Week 3**: Enable automation
- Set up GitHub Actions or cron
- Monitor daily
- Verify quality maintained

**Week 4+**: Production
- Check weekly
- Track engagement
- Refine as needed

---

## Documentation

Everything you need is documented:

- **QUICK_START.md** - 5-minute setup guide
- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **README_NEW.md** - Full user guide
- **docs/SOURCE_MINING_ANALYSIS.md** - Source evaluation
- **docs/POSTING_GUARDRAILS.md** - What gets posted
- **docs/SOURCE_DISCOVERY_EXPLAINED.md** - How discovery works
- **docs/KEY_IMPROVEMENTS.md** - Future enhancements

---

## Next Steps

1. **Create main branch** on GitHub (see Option A above)
2. **Read QUICK_START.md** for 5-minute setup
3. **Add Twitter credentials** to GitHub Secrets
4. **Enable GitHub Actions** and test manually
5. **Monitor** first few posts closely
6. **Enjoy** sharing poetry daily! 📖✨

---

**Your bot is production-ready and waiting to be deployed!**

All 3,500+ lines of documentation, complete rebuild, refinements, and deployment setup are done. Time to go live! 🚀
