# Poetry Bot - Comprehensive Project Review

**Review Date**: January 5, 2026
**Reviewer**: Claude
**Current Status**: Needs Major Rework

---

## Executive Summary

This poetry bot was ambitious in scope but has fundamental issues that prevent it from reliably posting quality poetry content. The posted history shows it's extracting and posting **non-poem content** (obituaries, reviews, table of contents, submission calls) despite extensive validation logic.

**Key Finding**: The bot is ahead of its time in architecture but behind in execution quality.

---

## Current Architecture

### Core Components

1. **poem_link_discovery.py** (1,455 lines)
   - Configures 75+ poetry sources
   - Discovers poem URLs via CSS selectors and regex patterns
   - Validates content structure
   - Caches results

2. **poetry_bot.py** (597 lines)
   - Main bot logic with EnhancedPoetryBot class
   - Extracts poems from discovered URLs
   - Validates poem content
   - Tracks posted poems to avoid duplicates

3. **twitter_bot.py** (488 lines)
   - PunchyTwitterPoetryBot class
   - Finds "punchiest" 4 consecutive lines
   - Posts to Twitter with link
   - Additional validation layer

4. **scheduler.py** (74 lines)
   - Runs bot 10 times/day at configured UTC times
   - Simple schedule-based execution

5. **config.py** (190 lines)
   - Bot settings (10 posts/day)
   - 120+ weighted journal list
   - Diversity controls

---

## Critical Problems

### 1. Validation is Completely Broken

**Evidence from posted_poems.json**:

```json
{
  "title": "\"Victorious\" by Alice Notley, 1945–2025",
  "author": "Unknown",
  "source": "The Iowa Review"
}
```
→ **This is an obituary, not a poem**

```json
{
  "title": "Contemporary writing from Canada and the world",
  "author": "Poetry",
  "source": "PRISM International"
}
```
→ **This is a submissions call page**

```json
{
  "title": "Last Day on Earth... reviewed by Jane Zwart",
  "author": "Zwart Jane",
  "source": "Plume"
}
```
→ **This is a book review, not a poem**

```json
{
  "title": "No. 44 Winter 2025",
  "author": "Unknown",
  "source": "32 Poems"
}
```
→ **This is a table of contents page**

**Root Causes**:
- CSS selectors are too generic (`article a`, `h2 a`) and catch ALL links
- Regex patterns match non-poem URLs (`/poetry/` could be /poetry/reviews/)
- Validation logic checks for poetry indicators but doesn't verify actual poem content
- Multiple validation layers but they're all failing

### 2. Source Configuration Issues

**Problems**:
- 75+ sources configured, but many don't publish full poems online
- Literary journals often paywall content or only show excerpts
- URL patterns too broad, catching reviews/interviews/announcements
- No verification that sources actually work

**Example Bad Patterns**:
```python
'poem_patterns': [
    r'^/poetry/.*$',  # Too broad! Catches /poetry/reviews/, /poetry/news/
    r'^/.*$'          # Catches EVERYTHING
]
```

### 3. Over-Complexity

**Unnecessary Complexity**:
- Three separate validation systems that all fail
- "Punchy line" scoring algorithm (interesting but premature optimization)
- 75+ sources when 5-10 reliable ones would be better
- Weighted journal system that doesn't improve quality

**What's Missing**:
- Simple, reliable extraction for known-good sources
- Manual verification workflow
- Quality metrics and monitoring
- Fallback to reliable sources

### 4. Extraction Quality

**Current Issues**:
- Title extraction pulls page titles, not poem titles
- Author extraction gets reviewers, not poets
- Text extraction includes navigation, metadata, dates
- "Clean lines" logic removes actual poem content

**Example**:
```python
# Removes lines with years in them
if re.search(r'\d{4}', line):
    continue
```
→ This removes valid poem lines like "In 1984 my father left"

### 5. Twitter Integration

**Current State**:
- Posts 4 "punchy" lines + link
- Good: Uses Twitter's link support
- Bad: Content quality is terrible due to extraction issues

**Missed Opportunities**:
- Not leveraging Poetry Foundation's structured data
- Not using Open Graph meta tags
- Not verifying links are accessible before posting

---

## What Works Well

### Positive Aspects

1. **Link Support**: Now that Twitter supports links, the strategy of excerpt + link is solid

2. **State Tracking**: posted_poems.json prevents duplicates (when it has valid poems)

3. **Rate Limiting**: Respectful delays between requests

4. **Modern Stack**: BeautifulSoup, requests, tweepy - all good choices

5. **Ambitious Scope**: The vision of a diverse, high-volume poetry bot is admirable

---

## Recommended Path Forward

### Option A: Complete Rebuild (Recommended)

**Focus on Quality Over Quantity**

1. **Start with 3-5 Tier-1 Sources**
   - Poetry Daily (poems.com)
   - Poetry Foundation (poetryfoundation.org)
   - Academy of American Poets (poets.org)

2. **Custom Extractor per Source**
   - Write specific extraction logic for each source
   - Manually verify selectors
   - Test with 20+ examples per source

3. **Strict Validation**
   - Verify URL accessibility
   - Check for actual poem HTML structure
   - Minimum line count (4-20 lines)
   - Maximum length (prevent essays)
   - Block known bad patterns (review, interview, etc.)

4. **Manual Review Queue**
   - Generate preview of 10 poems
   - Human reviews before posting
   - Build confidence in the system

5. **Gradual Expansion**
   - Add one new source at a time
   - Verify quality for 2 weeks
   - Only then add another source

6. **Daily Publishing, Not 10x/day**
   - 1-3 high-quality poems per day
   - Post at optimal times (morning, lunch, evening)
   - Build a reputation for quality

### Option B: Minimal Viable Product

**Focus on One Perfect Source**

1. **Poetry Daily Only**
   - They publish one poem per day
   - High editorial standards
   - Consistent HTML structure
   - Always includes full poem

2. **Simple Workflow**
   - Scrape today's poem
   - Extract cleanly (known structure)
   - Post to Twitter at 9am EST
   - One perfect poem per day

3. **Expand Later**
   - Once this works flawlessly for a month
   - Add Poetry Foundation
   - Then Academy of American Poets
   - Maximum 3 sources, 3 poems/day

---

## Specific Technical Improvements Needed

### 1. Extraction Rewrite

**Current**:
```python
# Generic selectors that catch everything
poem_selectors = [
    '.elementor-widget-theme-post-content',
    '.c-feature-bd',
    '.poem', '.poetry', '.poem-text'
]
```

**Needed**:
```python
# Source-specific extraction
def extract_poetry_daily(url, soup):
    """Extract poem from Poetry Daily with known structure"""
    title = soup.select_one('h2.title')  # Exact selector
    author = soup.select_one('.daily_poem_author')
    poem_div = soup.select_one('.elementor-widget-theme-post-content')

    # Verify structure
    if not all([title, author, poem_div]):
        raise ExtractionError("Missing required elements")

    # Clean extraction with known patterns
    # ...
```

### 2. Validation Rewrite

**Current**:
```python
# Complex scoring system that doesn't work
essay_patterns = [100+ patterns]
essay_count = sum(1 for pattern in essay_patterns if pattern in text_lower)
if essay_count >= 2:
    return False
```

**Needed**:
```python
# Simple, strict checks
def validate_poem(poem_data):
    # 1. URL must be accessible
    # 2. Must have title and author
    # 3. Text must be 20-500 words
    # 4. Must have 4-50 lines
    # 5. Must NOT contain: "review", "interview", "about the author"
    # 6. Title must NOT contain: "reviewed by", "No. X", dates
    # 7. Lines must average < 80 chars (poetry, not prose)
```

### 3. Source Configuration Rewrite

**Current**:
```python
SITE_CONFIGS = {
    'domain.com': {
        'poem_patterns': [r'^/poetry/.*$'],  # Too broad
        'css_selectors': ['article a']  # Too generic
    }
}
```

**Needed**:
```python
RELIABLE_SOURCES = {
    'poems.com': {
        'name': 'Poetry Daily',
        'daily_poem_url': 'https://poems.com/',
        'title_selector': 'h2.title',
        'author_selector': '.daily_poem_author',
        'poem_selector': '.elementor-widget-theme-post-content',
        'verified': True,  # Manually verified
        'last_test': '2026-01-05',
        'success_rate': 0.95
    }
}
```

### 4. Twitter Format

**Current**: Complex "punchy lines" algorithm

**Proposed**:
```
[Poem Title]
by [Author Name]

[First 4 lines of poem]
...

Read more: [link]

#Poetry #PoetryDaily
```

Simple, clean, consistent.

---

## Implementation Recommendations

### Phase 1: Foundation (Week 1-2)

1. Create `sources/` directory with one file per source
2. Implement Poetry Daily extractor with 100% success rate
3. Build validation that catches ALL non-poems
4. Create preview mode (no posting)
5. Test with 100 historical poems from Poetry Daily

### Phase 2: Verification (Week 3-4)

1. Run in preview mode for 2 weeks
2. Manual review of all generated tweets
3. Fix any extraction issues
4. Build confidence metrics

### Phase 3: Launch (Week 5)

1. Enable posting (1 poem/day)
2. Monitor for 1 week
3. Review all posts
4. Adjust as needed

### Phase 4: Expansion (Week 6+)

1. Add Poetry Foundation (same process)
2. Add Academy of American Poets
3. Increase to 2-3 poems/day
4. Continue monitoring

---

## Architecture Proposal

### New Structure

```
poetry_bot/
├── sources/
│   ├── base.py              # Base source class
│   ├── poetry_daily.py      # Poetry Daily extractor
│   ├── poetry_foundation.py # Poetry Foundation extractor
│   └── poets_org.py         # Academy of American Poets
├── validators/
│   ├── content.py           # Content validation
│   ├── structure.py         # HTML structure validation
│   └── accessibility.py     # URL accessibility
├── formatters/
│   ├── twitter.py           # Twitter formatting
│   └── preview.py           # Preview formatting
├── storage/
│   ├── posted.py            # Posted poems tracker
│   └── queue.py             # Review queue
├── bot.py                   # Main orchestration
├── config.yaml              # Configuration
└── test_sources.py          # Source testing
```

### Clean Separation

- **Sources**: Know how to extract from specific sites
- **Validators**: Know what makes valid content
- **Formatters**: Know how to format for platforms
- **Storage**: Know how to track state
- **Bot**: Orchestrates everything

---

## Metrics to Track

### Quality Metrics

1. **Extraction Success Rate**: % of attempts that extract valid poems
2. **False Positive Rate**: % of "poems" that are actually reviews/TOC/etc.
3. **Author Accuracy**: % of correct author attributions
4. **Title Accuracy**: % of correct titles

### Operational Metrics

1. **Daily Success Rate**: Did we post today?
2. **Source Availability**: Are sources accessible?
3. **Error Types**: What's failing and why?

### Engagement Metrics (Twitter)

1. Impressions per post
2. Engagement rate
3. Link clicks (traffic to poetry sources)
4. Best performing poets/styles

---

## Questions to Answer

### Strategic Decisions Needed

1. **Volume vs Quality**: 1 perfect poem/day or 10 variable quality?
   - **Recommendation**: Quality. Build reputation first.

2. **Source Diversity**: 75+ sources or 3-5 reliable?
   - **Recommendation**: Start with 3-5, expand slowly.

3. **Content Strategy**: Excerpts or full poems?
   - **Recommendation**: Excerpts + link (respect copyright, drive traffic).

4. **Posting Frequency**: 10x/day or 1-3x/day?
   - **Recommendation**: 1-3x/day at optimal times.

5. **Automation Level**: Fully automatic or manual review?
   - **Recommendation**: Manual review until 99%+ accuracy.

---

## Immediate Next Steps

### If Rebuilding (Recommended)

1. **Archive current code**: `git checkout -b archive/old-approach`
2. **Start fresh**: New main branch with clean architecture
3. **Build Poetry Daily extractor**: One source, perfect quality
4. **Test extensively**: 100+ test cases
5. **Deploy in preview mode**: No posting yet
6. **Manual review**: 2 weeks of verification
7. **Launch**: 1 poem/day when confident
8. **Iterate**: Add sources one at a time

### If Fixing Current Code

1. **Fix validation first**: Make it catch ALL non-poems
2. **Reduce sources**: Disable all but Poetry Daily, Poetry Foundation, Poets.org
3. **Rewrite extractors**: Custom logic for each source
4. **Test extensively**: Run in preview mode for 2 weeks
5. **Manual verification**: Review every generated post
6. **Gradual rollout**: 1 poem/day, then increase

---

## Conclusion

This project has **good bones** but needs **major surgery**:

✅ Good: Link-based approach, state tracking, respectful scraping
❌ Bad: Validation broken, extraction poor, over-complexity
🎯 Fix: Rebuild with focus on quality over quantity

**Core Philosophy Shift Needed**:
- From "75+ sources, 10 posts/day" → "3-5 sources, 1-3 posts/day"
- From "automated everything" → "automated with verification"
- From "complex validation" → "simple, strict validation"
- From "generic extraction" → "source-specific extraction"

The vision is right: daily poetry on Twitter with links to sources. The execution needs to match the vision's quality.

---

## Resources Needed

1. **Time**: 2-4 weeks for proper rebuild
2. **Testing**: Access to historical posts for validation
3. **Monitoring**: Logging and metrics infrastructure
4. **Review**: Human review workflow for first month

**Estimated Effort**:
- Option A (Rebuild): 40-60 hours
- Option B (MVP): 20-30 hours
- Option C (Fix Current): 30-50 hours (high risk of failure)

**Recommendation**: Option A (Rebuild) or Option B (MVP)

The current approach is fundamentally flawed. Better to start fresh with clear principles than try to fix broken foundations.
