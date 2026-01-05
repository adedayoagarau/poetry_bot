# Quick Start - Poetry Bot Setup

## ✅ Step 1: Your Code is Ready!

Your branch has been merged to `main`. All code is production-ready.

---

## 🚀 Step 2: Choose Your Deployment Method

### Option A: GitHub Actions (Recommended) ⭐

**Best for**: Hands-off automation, no server needed

#### Setup (5 minutes):

1. **Go to your GitHub repo** → **Settings** → **Secrets and variables** → **Actions**

2. **Add these 5 secrets**:
   ```
   TWITTER_API_KEY = [get from developer.twitter.com]
   TWITTER_API_SECRET = [get from developer.twitter.com]
   TWITTER_ACCESS_TOKEN = [get from developer.twitter.com]
   TWITTER_ACCESS_TOKEN_SECRET = [get from developer.twitter.com]
   TWITTER_BEARER_TOKEN = [get from developer.twitter.com]
   ```

3. **Enable GitHub Actions**:
   - Go to **Actions** tab
   - Click "I understand, enable them"

4. **Test it manually**:
   - Actions → "Post Daily Poem" → "Run workflow"
   - Watch it run
   - Check Twitter

5. **Done!** It will auto-post daily at 9am EST.

---

### Option B: Server Cron Job

**Best for**: If you have a server running 24/7

#### Setup (10 minutes):

```bash
# 1. Clone repo on your server
git clone https://github.com/your-username/poetry_bot.git
cd poetry_bot

# 2. Set up Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Create .env file
nano .env
# Add your Twitter credentials (see .env.example)
# Save and exit

# 4. Test it
python bot.py          # Preview mode
python bot.py --live   # Live posting (test once)

# 5. Set up cron (runs daily at 9am)
crontab -e
# Add this line (replace /full/path/to with actual paths):
0 9 * * * cd /full/path/to/poetry_bot && /full/path/to/poetry_bot/venv/bin/python /full/path/to/poetry_bot/bot.py --live >> /full/path/to/poetry_bot/logs/cron.log 2>&1
```

---

## 📋 Step 3: Get Twitter API Credentials

1. Go to **https://developer.twitter.com/en/portal/dashboard**
2. Create a new app (or use existing)
3. Go to **Keys and Tokens**
4. Generate/copy all 5 credentials:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token
5. Your app needs **Read and Write** permissions

---

## 🧪 Step 4: Test Before Going Live

### First Test (Preview Only):
```bash
# Locally or on server
python bot.py
# Review output - does it look good?
```

### Second Test (One Live Post):
```bash
python bot.py --live
# Check Twitter - did it post correctly?
```

### Third Test (Automated Run):
- GitHub Actions: Click "Run workflow" manually
- Cron: Wait for scheduled time, check logs

---

## 📅 Step 5: Your Schedule

**Default**: Posts daily at 9am EST (14:00 UTC)

**To change the time**:

### GitHub Actions:
Edit `.github/workflows/daily-poem.yml`:
```yaml
schedule:
  - cron: '0 14 * * *'  # Change this
```

### Cron Job:
Edit crontab:
```bash
crontab -e
0 9 * * * [your command]  # Change first number (hour)
```

**Cron examples**:
- `0 9 * * *` = 9am daily
- `0 9,17 * * *` = 9am and 5pm daily
- `0 */4 * * *` = Every 4 hours

Use [Crontab Guru](https://crontab.guru/) to test schedules.

---

## 🔍 Step 6: Monitor

### GitHub Actions:
- Go to **Actions** tab
- See green ✅ or red ❌
- Click to view logs
- Get email on failures

### Cron Job:
```bash
# Check logs
tail -f logs/cron.log

# Check last post
cat data/posted_poems.json | tail -20
```

---

## 🛠️ Troubleshooting

### Bot didn't post?

**Check 1**: Are credentials correct?
```bash
# Test authentication
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Loaded' if os.getenv('TWITTER_API_KEY') else '❌ Missing')"
```

**Check 2**: Did extraction work?
```bash
# Test in preview mode
python bot.py
```

**Check 3**: Check logs
- GitHub Actions: Actions tab → Click run → View logs
- Cron: `tail -f logs/cron.log`

### Common Issues:

**"Missing Twitter API credentials"**
- Add secrets to GitHub repo OR
- Create .env file on server

**"No poem found"**
- Poetry Daily might be down
- Check source in preview mode
- Will retry next run automatically

**"Already posted"**
- Bot tracks posted poems
- Won't post duplicates
- This is normal behavior

---

## 📊 Recommended Timeline

**Week 1**: Preview mode only
- Run `python bot.py` daily
- Manually review each output
- No live posting yet

**Week 2**: Manual live posts
- Run `python bot.py --live` once
- Monitor Twitter engagement
- Verify quality

**Week 3**: Enable automation
- Set up GitHub Actions or cron
- Monitor daily
- Verify posts look good

**Week 4+**: Fully automated
- Check weekly
- Review engagement
- Adjust as needed

---

## 📈 Next Steps After Launch

### Month 2:
- Add Academy of American Poets source
- Increase to 2 posts/day

### Month 3:
- Add Poetry Foundation source
- Increase to 2-3 posts/day
- Track engagement metrics

### Month 6+:
- Consider 4th/5th source if needed
- Optimize posting times
- Build community

---

## 📚 Full Documentation

- **DEPLOYMENT_GUIDE.md** - Complete deployment instructions
- **README_NEW.md** - User guide
- **docs/SOURCE_MINING_ANALYSIS.md** - Source evaluation
- **docs/POSTING_GUARDRAILS.md** - What gets posted
- **docs/KEY_IMPROVEMENTS.md** - Future enhancements

---

## 🎯 Your First Goal

**Get 7 consecutive days of quality posts**

✅ Day 1: Post looks good
✅ Day 2: Post looks good
✅ Day 3: Post looks good
✅ Day 4: Post looks good
✅ Day 5: Post looks good
✅ Day 6: Post looks good
✅ Day 7: Post looks good

Once you achieve this, you're ready to scale up!

---

## 💡 Pro Tips

1. **Start conservative**: 1 post/day is plenty
2. **Monitor closely**: First month, check daily
3. **Quality over quantity**: Always
4. **Engage with followers**: Reply to comments
5. **Track what works**: Note which poets get engagement
6. **Be patient**: Building an audience takes time

---

## ✅ Checklist

Setup:
- [ ] Twitter API credentials obtained
- [ ] Secrets added to GitHub (or .env created)
- [ ] GitHub Actions enabled (or cron set up)
- [ ] Manual test completed successfully

Week 1:
- [ ] 7 days of preview mode testing
- [ ] All outputs look good
- [ ] Ready for live posting

Week 2:
- [ ] First live post successful
- [ ] Monitoring engagement
- [ ] Tweaking as needed

Week 3:
- [ ] Automation enabled
- [ ] Daily monitoring in place
- [ ] Quality maintained

---

## 🆘 Need Help?

1. Check **DEPLOYMENT_GUIDE.md** for detailed instructions
2. Review **docs/** folder for comprehensive documentation
3. Test in preview mode: `python bot.py`
4. Check logs for errors

---

## 🎉 You're Ready!

Your poetry bot is:
- ✅ Built with quality-first approach
- ✅ Thoroughly documented
- ✅ Ready to deploy
- ✅ Set up for long-term success

**Time to share beautiful poetry with the world!** 📖✨

---

**Last Updated**: January 5, 2026
**Bot Version**: 2.0 (Complete Rebuild)
