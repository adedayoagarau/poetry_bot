# Where Is The Bot Posting From?

**Understanding the Source Discovery Mechanism**

## The Simple Answer

**The bot posts from poetry website homepage URLs that are updated daily.**

It doesn't "mine" or "scrape" or "search" the web. It goes to specific, known locations where editors have already selected and published a poem.

---

## How It Actually Works

### Current Implementation (Poetry Daily)

```python
class PoetryDailySource(PoetrySource):
    def get_todays_poem_url(self) -> str:
        return "https://poems.com/"  # Just the homepage!

    def extract_poem(self, url: str) -> Poem:
        # Fetch homepage
        soup = fetch_html(url)

        # Extract poem from known selectors
        title = soup.select_one('title').get_text()
        author = soup.select_one('.daily_poem_author').get_text()
        poem = soup.select_one('.elementor-widget-theme-post-content').get_text()

        return Poem(title, author, poem, "Poetry Daily", url)
```

**That's it!**

No complex discovery. No searching. Just:
1. Go to homepage
2. Extract today's poem
3. Validate it
4. Post it

---

## The Three-Tier Discovery Model

### Tier 1: Known Daily URLs (Current)
**Method**: Direct URL

**How It Works**:
```
1. Bot knows: "Poetry Daily publishes at poems.com/"
2. Bot fetches: poems.com/
3. Bot extracts: Today's poem from homepage
4. Bot posts: Validated poem
```

**Sources Using This**:
- Poetry Daily (poems.com/)
- Academy of American Poets (poets.org/poem-a-day)
- Poetry Foundation (poetryfoundation.org/poems/poem-of-the-day)

**Pros**:
- ✅ Simple, reliable
- ✅ Always fresh content
- ✅ Editor-curated quality
- ✅ No searching needed

**Cons**:
- 🟡 Limited to sources with daily feature

---

### Tier 2: Archive Discovery (Future)
**Method**: Parse archive pages

**How It Would Work**:
```
1. Bot goes to: poems.com/archive/
2. Bot finds links: All recent poem URLs
3. Bot filters: Not yet posted
4. Bot extracts: From individual URLs
5. Bot posts: Validated poems
```

**Example**:
```python
def discover_recent_poems(self) -> List[str]:
    archive_url = "https://poems.com/archive/"
    soup = fetch_html(archive_url)

    # Find all poem links from last 30 days
    links = soup.select('a[href*="/poem/"]')
    urls = [urljoin(archive_url, link['href']) for link in links]

    # Filter to unposted
    unposted = [url for url in urls if url not in posted_tracker]

    return unposted[:10]  # Top 10
```

**Sources That Could Use This**:
- Poetry Foundation (huge archive)
- Academy archives
- Verse Daily archive

**Pros**:
- ✅ More variety
- ✅ Can post 2-3x/day from one source
- ✅ Fallback if daily poem fails

**Cons**:
- 🟡 More complex
- 🟡 Need to parse archive structure
- 🟡 Risk of older/duplicate content

**When To Use**:
- After perfecting daily poems
- If want 3+ posts/day
- As fallback mechanism

---

### Tier 3: Search/API (Not Recommended)
**Method**: Search APIs or site search

**How It Would Work**:
```
1. Bot searches: "contemporary poetry 2026"
2. Bot gets results: Mix of quality
3. Bot filters: Validation hell
4. Bot extracts: Often fails
5. Bot posts: Low quality
```

**Why We DON'T Do This**:
- ❌ Quality uncontrolled
- ❌ Validation nightmare
- ❌ Copyright concerns
- ❌ No editorial curation
- ❌ This was the OLD bot's mistake

---

## URL Structure by Source

### Poetry Daily
```
Homepage: https://poems.com/
Today's poem: https://poems.com/ (updated daily)
Archive: https://poems.com/archive/
Individual: https://poems.com/poem/[poem-slug]/

Discovery strategy: Homepage only
```

### Academy of American Poets
```
Homepage: https://poets.org/
Poem-a-Day: https://poets.org/poem-a-day (updated daily)
Archive: https://poets.org/poems
Individual: https://poets.org/poem/[poem-slug]

Discovery strategy: /poem-a-day page
```

### Poetry Foundation
```
Homepage: https://www.poetryfoundation.org/
Poem of Day: https://www.poetryfoundation.org/poems/poem-of-the-day
Archive: https://www.poetryfoundation.org/poems/browse
Individual: https://www.poetryfoundation.org/poems/[id]/[slug]

Discovery strategy: /poems/poem-of-the-day
```

---

## Where Exactly Does Content Come From?

### Poetry Daily (Current)

**Publishing Model**:
- Editors read 200+ literary magazines
- Select one outstanding poem per day
- Publish full poem on homepage
- Update at midnight EST

**What We Get**:
- Pre-curated quality
- Full poem text
- Author attribution
- Link to original source

**Our Discovery**:
```python
url = "https://poems.com/"  # That's it!
```

**Real Example**:
```
Date: January 5, 2026
Poem: "The Wild Swans at Coole" by W. B. Yeats
Source: Originally from The Wild Swans at Coole (1919)
Featured by: Poetry Daily editors

Our bot:
1. Fetches poems.com/
2. Extracts title, author, poem
3. Validates (passes all checks)
4. Posts to Twitter
```

---

### Academy of American Poets (To Implement)

**Publishing Model**:
- Commissioned Poem-a-Day program
- Diverse contemporary poets
- New poem every single day
- Free to public

**What We'll Get**:
- Original contemporary poems
- Diverse voices (curated for representation)
- Full poem + poet bio
- Copyright cleared for sharing

**Our Discovery**:
```python
url = "https://poets.org/poem-a-day"  # Updated daily
```

---

### Poetry Foundation (To Implement)

**Publishing Model**:
- Draws from archive of 75,000+ poems
- Mix of contemporary and classic
- Curated Poem of the Day
- Public domain + permissions

**What We'll Get**:
- Mix of eras and styles
- Vetted quality
- Full poems
- Comprehensive metadata

**Our Discovery**:
```python
url = "https://www.poetryfoundation.org/poems/poem-of-the-day"
```

---

## What We DON'T Do

### ❌ Web Crawling
We don't crawl the web looking for poems. We go to known, trusted sources.

### ❌ Search Engines
We don't use Google/Bing to find poems. We use editorial curation.

### ❌ Random Websites
We don't scrape random poetry blogs. We use established institutions.

### ❌ User Submissions
We don't accept user-submitted poems. We use published work only.

### ❌ Social Media
We don't pull from Instagram/Twitter poetry. We use literary sources.

### ❌ AI Generation
We NEVER use AI-generated poems. Real poets only.

---

## Discovery Process Flowchart

```
┌─────────────────────────────────────┐
│ Bot Wakes Up (Daily @ 9am EST)     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Check Source 1: Poetry Daily        │
│ URL: poems.com/                     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Fetch HTML from homepage            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Extract poem using known selectors  │
│ - Title from <title> tag            │
│ - Author from .daily_poem_author    │
│ - Poem from .elementor-widget-...   │
└──────────────┬──────────────────────┘
               │
               ▼
       ┌───────┴───────┐
       │ Validate      │
       └───────┬───────┘
               │
        ┌──────┴──────┐
        │             │
     PASS           FAIL
        │             │
        ▼             ▼
   ┌────────┐   ┌──────────┐
   │ POST ✅│   │ SKIP ❌  │
   └────────┘   └────┬─────┘
                     │
                     ▼
            ┌────────────────┐
            │ Try Source 2:  │
            │ Academy        │
            └────────────────┘
```

---

## Source Reliability

### Why Our Sources Are Reliable

**Poetry Daily**:
- ✅ Same HTML structure since 2015
- ✅ Published daily for 27 years
- ✅ Non-profit, stable funding
- ✅ Professional editorial team
- ✅ Predictable update schedule

**Academy of American Poets**:
- ✅ Established 1934
- ✅ Well-funded non-profit
- ✅ Committed to Poem-a-Day program
- ✅ Consistent web presence
- ✅ Actively maintained site

**Poetry Foundation**:
- ✅ $200M endowment (very stable)
- ✅ Professional organization
- ✅ Massive digital archive
- ✅ Long-term commitment
- ✅ Technical excellence

### Why Random Sites Are Unreliable

**Problems**:
- ❌ HTML changes frequently
- ❌ Sites go offline
- ❌ Inconsistent quality
- ❌ No editorial standards
- ❌ Copyright unclear
- ❌ Maintenance burden

---

## Content Provenance

### Where Poems Originally Come From

**Poetry Daily** curates from:
- The New Yorker
- The Paris Review
- Granta
- Atlantic
- 200+ literary magazines

**Academy** publishes:
- Commissioned original work
- Contemporary American poets
- Diverse voices program

**Poetry Foundation** hosts:
- Poetry Magazine archive
- Classic public domain works
- Licensed contemporary poems

**Our Role**:
- We don't curate (they do)
- We don't search (they publish)
- We extract and share
- We attribute and link

---

## Discovery vs Curation

### What's The Difference?

**Discovery** (what bot does):
- Go to known URL
- Extract structured data
- Validate technical requirements
- Post if valid

**Curation** (what sources do):
- Read hundreds of submissions
- Select best poems
- Edit for quality
- Publish with context

**We inherit curation from trusted sources.**

This is why 3-5 sources > 75 random sources.

---

## The URLs We Actually Use

### Current (Live)
```python
ACTIVE_SOURCES = {
    'Poetry Daily': 'https://poems.com/'
}
```

### Next (To Implement)
```python
PLANNED_SOURCES = {
    'Academy of American Poets': 'https://poets.org/poem-a-day',
    'Poetry Foundation': 'https://www.poetryfoundation.org/poems/poem-of-the-day'
}
```

### Maybe Later (If Needed)
```python
OPTIONAL_SOURCES = {
    'Verse Daily': 'https://www.versedaily.org/',
    'Rattle': 'https://rattle.com/poetry-of-the-day/'
}
```

### Never
```python
AVOID = {
    'The New Yorker': 'https://newyorker.com',  # Paywall
    'Random blogs': '*',  # Quality unknown
    'Social media': '*',  # Not our purpose
}
```

---

## Technical Implementation

### How Extraction Works

**Step 1: Fetch**
```python
response = requests.get('https://poems.com/')
soup = BeautifulSoup(response.content, 'html.parser')
```

**Step 2: Extract**
```python
title_elem = soup.find('title')
title = title_elem.get_text().replace(' – Poetry Daily', '')

author_elem = soup.select_one('.daily_poem_author')
author = author_elem.get_text().strip()

poem_elem = soup.select_one('.elementor-widget-theme-post-content')
poem_text = poem_elem.get_text(separator='\n')
```

**Step 3: Clean**
```python
# Remove navigation, metadata, etc.
lines = [line.strip() for line in poem_text.split('\n') if line.strip()]
clean_lines = [line for line in lines if not is_metadata(line)]
poem_text = '\n'.join(clean_lines)
```

**Step 4: Validate**
```python
validator = ContentValidator()
is_valid, reason = validator.validate(poem)
```

**Step 5: Post (if valid)**
```python
if is_valid:
    tweet = formatter.format_tweet(poem)
    twitter.post(tweet)
    tracker.mark_posted(poem)
```

---

## Why This Approach Works

### Simplicity
- ✅ 3 URLs to monitor
- ✅ Known structure
- ✅ Predictable updates
- ✅ Easy to debug

### Reliability
- ✅ Sources stable for decades
- ✅ Professional maintenance
- ✅ Consistent publishing
- ✅ Clear attribution

### Quality
- ✅ Pre-curated content
- ✅ Editorial standards
- ✅ Diverse voices
- ✅ Copyright cleared

### Sustainability
- ✅ Low maintenance
- ✅ Easy to monitor
- ✅ Clear failure modes
- ✅ Room to grow

---

## Future Discovery Enhancements

### Enhancement 1: Archive Fallback

If today's poem fails validation:
```python
def get_daily_poem(self):
    # Try today's poem first
    poem = get_todays_poem()
    if poem and validate(poem):
        return poem

    # Fallback: Get from recent archive
    archive_poems = get_recent_archive_poems(days=7)
    for poem in archive_poems:
        if validate(poem) and not is_posted(poem):
            return poem

    return None
```

### Enhancement 2: Multi-Source Selection

Pick best poem from multiple sources:
```python
def get_best_daily_poem(self):
    candidates = []

    # Get from all sources
    for source in sources:
        poem = source.get_daily_poem()
        if poem and validate(poem):
            candidates.append(poem)

    # Score by engagement potential
    best = max(candidates, key=score_engagement_potential)
    return best
```

### Enhancement 3: Time-Based Rotation

Post different sources at different times:
```python
POSTING_SCHEDULE = {
    '09:00': PoetryDailySource(),      # Morning: Contemporary
    '14:00': PoetryFoundationSource(),  # Afternoon: Classic
    '19:00': AcademySource(),          # Evening: Diverse voices
}
```

---

## Monitoring Discovery Health

### Daily Checks
- ✅ Did each source return a poem?
- ✅ Did extraction succeed?
- ✅ Did validation pass?
- ✅ Are URLs still valid?

### Weekly Checks
- 📊 Success rate per source
- 📈 Validation failure patterns
- 🔧 Extraction errors
- 🌐 Source uptime

### Monthly Checks
- 🏥 Source health audit
- 🔄 HTML structure changes?
- 📉 Declining quality?
- 💡 New sources to consider?

---

## Summary

**Where does content come from?**
→ Three known, trusted URLs that update daily

**How does discovery work?**
→ Fetch homepage, extract poem, validate, post

**Why not search/crawl?**
→ Quality > quantity, curation > automation

**Why so simple?**
→ Simple = reliable, maintainable, sustainable

**Why 3-5 sources?**
→ Sufficient variety, manageable maintenance, quality focus

**The philosophy:**
Trust expert curators, inherit their quality, share reliably with attribution.
