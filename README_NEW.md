# Poetry Bot 2.0 - Complete Rebuild

**Clean, Reliable, Quality-Focused Poetry Posting**

## What Changed

### Before (Old Bot)
- ❌ 75+ sources (most broken)
- ❌ 10 posts/day of variable quality
- ❌ Complex validation that didn't work
- ❌ Generic extractors that caught reviews, obituaries, TOC pages
- ❌ Posted non-poems consistently

### After (New Bot)
- ✅ 1-3 reliable sources
- ✅ 1-3 posts/day of high quality
- ✅ Simple, strict validation
- ✅ Source-specific extractors
- ✅ Zero tolerance for non-poems

## Architecture

```
poetry_bot/
├── sources/              # Source-specific extractors
│   ├── base.py          # Base classes (Poem, PoetrySource)
│   ├── poetry_daily.py  # Poetry Daily extractor
│   └── __init__.py
│
├── validators/          # Content validation
│   ├── content.py       # Strict validation rules
│   └── __init__.py
│
├── formatters/          # Tweet formatting
│   ├── twitter.py       # Twitter formatter
│   └── __init__.py
│
├── storage/             # State tracking
│   ├── posted.py        # Posted poems tracker
│   └── __init__.py
│
├── bot.py               # Main orchestrator
├── test_bot.py          # Test suite
├── new_config.yaml      # Configuration
└── README_NEW.md        # This file
```

## Clean Separation of Concerns

### Sources (`sources/`)
- **Responsibility**: Extract poems from specific websites
- **Each source has custom logic** - no generic "works everywhere" code
- **Returns structured `Poem` objects**

Example:
```python
from sources import PoetryDailySource

source = PoetryDailySource()
poem = source.get_daily_poem()
# Returns: Poem(title, author, text, source_name, source_url)
```

### Validators (`validators/`)
- **Responsibility**: Ensure content is actually a poem
- **Strict blocklist** - reviews, obituaries, interviews, TOC pages
- **Structure checks** - line length, word count, prose detection

Example:
```python
from validators import ContentValidator

validator = ContentValidator()
is_valid, reason = validator.validate(poem)
# Returns: (True, "Poem validated successfully") or (False, "reason")
```

### Formatters (`formatters/`)
- **Responsibility**: Format poems for Twitter
- **Clean, consistent format**
- **Handles truncation gracefully**

Example:
```python
from formatters import TwitterFormatter

formatter = TwitterFormatter()
tweet = formatter.format_tweet(poem)
# Returns formatted tweet text (max 280 chars)
```

### Storage (`storage/`)
- **Responsibility**: Track which poems have been posted
- **Prevents duplicates**
- **Maintains history**

Example:
```python
from storage import PostedTracker

tracker = PostedTracker()
if not tracker.has_posted(poem):
    # Post poem...
    tracker.mark_posted(poem, tweet_url)
```

## Usage

### Preview Mode (Default)
```bash
# Preview what would be posted (doesn't actually post)
python bot.py
```

Output:
```
🤖 Poetry Bot initialized
📍 Mode: PREVIEW
📚 Sources: ['Poetry Daily']
💾 Posted poems: 0

🔍 Checking Poetry Daily...
✅ Valid poem found!
   Title: The Wild Swans at Coole
   Author: W. B. Yeats
   Lines: 24
   Words: 156

============================================================
📱 TWEET PREVIEW
============================================================
The Wild Swans at Coole
by W. B. Yeats

The trees are in their autumn beauty,
The woodland paths are dry,
Under the October twilight the water
Mirrors a still sky;
...

https://poems.com/poem/wild-swans-coole/

#Poetry
============================================================
📊 Length: 245/280 chars
📝 Lines: 4/24
✂️  Truncated: Yes (full poem at link)
============================================================

👁️  Preview mode - not posting to Twitter
💡 Run with preview_mode=False to post
```

### Live Posting
```bash
# Actually post to Twitter (requires API credentials)
python bot.py --live
```

### Test Suite
```bash
# Run tests
python test_bot.py
```

## Configuration

Edit `new_config.yaml`:

```yaml
bot:
  preview_mode: true   # false for live posting
  posts_per_day: 1     # Conservative start

sources:
  - name: "Poetry Daily"
    enabled: true
    weight: 1.0

validation:
  min_word_count: 20
  max_word_count: 600
  min_line_count: 4
  max_line_count: 100

twitter:
  default_lines_in_excerpt: 4
  hashtags:
    - "Poetry"
```

## Twitter Setup

Set environment variables:
```bash
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
export TWITTER_BEARER_TOKEN="your_bearer_token"
```

Or create `.env` file:
```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

## Validation Rules

The new bot has **zero tolerance** for false positives:

### Blocklist Patterns
- ❌ Reviews: "reviewed by", "book review", "critique"
- ❌ Interviews: "interview with", "conversation with"
- ❌ Obituaries: "1945-2025", "passed away", "in memoriam"
- ❌ TOC: "No. 44 Winter 2025", "issue", "table of contents"
- ❌ Submissions: "call for submissions", "deadline"
- ❌ About pages: "about the author", "biography"

### Structure Checks
- ✅ 20-600 words (poems, not essays)
- ✅ 4-100 lines
- ✅ Average line length < 120 chars (poetry, not prose)
- ✅ < 20% lines over 200 chars (no prose paragraphs)

### Title Checks
- ❌ "reviewed by"
- ❌ "No. X" (issue numbers)
- ❌ Year ranges (1945-2025)
- ❌ "Issue", "Winter 2025", etc.

## Tweet Format

```
[Poem Title]
by [Author Name]

[First 4 lines]
...

[URL to full poem]

#Poetry
```

**Example**:
```
The Wild Swans at Coole
by W. B. Yeats

The trees are in their autumn beauty,
The woodland paths are dry,
Under the October twilight the water
Mirrors a still sky;
...

https://poems.com/poem/wild-swans-coole/

#Poetry
```

## Adding New Sources

Create a new file in `sources/`:

```python
# sources/poetry_foundation.py

from typing import Optional
from .base import PoetrySource, Poem


class PoetryFoundationSource(PoetrySource):
    """Extract poems from Poetry Foundation"""

    @property
    def name(self) -> str:
        return "Poetry Foundation"

    @property
    def base_url(self) -> str:
        return "https://www.poetryfoundation.org"

    def get_todays_poem_url(self) -> Optional[str]:
        """Get URL for today's poem"""
        # Implementation specific to Poetry Foundation
        ...

    def extract_poem(self, url: str) -> Optional[Poem]:
        """Extract poem from URL"""
        # Implementation specific to Poetry Foundation
        ...
```

Update `sources/__init__.py`:
```python
from .poetry_foundation import PoetryFoundationSource

__all__ = [..., 'PoetryFoundationSource']
```

Update `bot.py`:
```python
from sources import PoetryDailySource, PoetryFoundationSource

self.sources = [
    PoetryDailySource(),
    PoetryFoundationSource(),  # Add new source
]
```

## Deployment

### Local Cron Job
```bash
# Edit crontab
crontab -e

# Add job to run once a day at 9am EST (14:00 UTC)
0 14 * * * cd /path/to/poetry_bot && python bot.py --live >> logs/bot.log 2>&1
```

### GitHub Actions (Coming Soon)
```yaml
name: Post Daily Poem
on:
  schedule:
    - cron: '0 14 * * *'  # 9am EST daily
jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Post poem
        env:
          TWITTER_API_KEY: ${{ secrets.TWITTER_API_KEY }}
          # ... other secrets
        run: python bot.py --live
```

## Quality Metrics

Track these metrics to ensure quality:

1. **Extraction Success Rate**: Did we get a poem?
2. **Validation Pass Rate**: Did it pass validation?
3. **False Positive Rate**: Did we post a non-poem? (should be 0%)
4. **Engagement Rate**: Twitter impressions, likes, retweets

## Monitoring

Check logs for:
- ❌ Failed extractions
- ❌ Validation failures
- ✅ Successful posts
- 📊 Engagement metrics

## Maintenance

### Weekly
- Review last 7 posts for quality
- Check validation failure reasons
- Adjust extractors if source HTML changed

### Monthly
- Review engagement metrics
- Consider adding new source
- Update validation rules if needed

## Migration from Old Bot

The old code has been archived:
- `archive/` - Main bot files
- `old_tests/` - Test scripts

Keep the old `posted_poems.json` to avoid reposting:
```bash
# Copy old posted history to new location
mkdir -p data
cp posted_poems.json data/posted_poems.json
```

## Philosophy

**Quality over Quantity**
- 1 perfect poem/day > 10 questionable posts/day
- Build reputation for quality
- Drive traffic to poetry sources
- Respect copyright with excerpts + links

**Reliability over Features**
- Simple, tested code
- Source-specific logic
- Strict validation
- Manual review until confident

**Gradual Expansion**
- Start with 1 source (Poetry Daily)
- Verify quality for 2 weeks
- Add sources one at a time
- Never sacrifice quality for volume

## FAQ

**Q: Why only one source to start?**
A: Perfect one source before adding more. Quality over quantity.

**Q: Why 1 post/day instead of 10?**
A: Build reputation for quality. Engage audience, don't spam.

**Q: What if Poetry Daily changes their HTML?**
A: The extractor will fail gracefully. Fix the selectors in `sources/poetry_daily.py`.

**Q: Can I add my own sources?**
A: Yes! Follow the pattern in `sources/poetry_daily.py`. Test thoroughly.

**Q: How do I know it's working?**
A: Run in preview mode first. Manually review output. Only go live when confident.

## License

MIT

## Contributing

1. Test thoroughly with preview mode
2. Ensure 100% validation success rate
3. Manually review 20+ outputs
4. Submit PR with test results

## Support

Issues: https://github.com/your-username/poetry_bot/issues

---

**Built with care for the poetry community 📖✨**
