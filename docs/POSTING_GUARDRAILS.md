# Posting Guardrails & Decision Framework

**Purpose**: Define exactly what to post, when to skip, and how to decide

## The Core Question

**"Should we post this poem?"**

This document provides the complete decision framework.

---

## Decision Tree

```
START: Bot found potential poem
    ↓
[1] Is URL accessible? (HTTP 200)
    NO → SKIP (log: URL inaccessible)
    YES ↓
[2] Does it have a title?
    NO → SKIP (log: Missing title)
    YES ↓
[3] Does it have an author?
    NO → SKIP (log: Missing author)
    YES ↓
[4] Is author real? (not "Unknown", "Anonymous")
    NO → SKIP (log: Invalid author)
    YES ↓
[5] Does title contain red flags?
    - "reviewed by"
    - "No. X" (issue number)
    - "Winter 2025" (date)
    - "1945-2025" (year range)
    YES → SKIP (log: Title red flag)
    NO ↓
[6] Does content match blocklist patterns?
    - Reviews, interviews
    - Obituaries, memorials
    - Table of contents
    - Submissions calls
    YES → SKIP (log: Blocklist match)
    NO ↓
[7] Is word count in range? (20-600)
    NO → SKIP (log: Word count out of range)
    YES ↓
[8] Is line count in range? (4-100)
    NO → SKIP (log: Line count out of range)
    YES ↓
[9] Is average line length reasonable? (<120 chars)
    NO → SKIP (log: Lines too long - prose)
    YES ↓
[10] Are there prose paragraphs? (>20% lines over 200 chars)
    YES → SKIP (log: Contains prose paragraphs)
    NO ↓
[11] Has this been posted before?
    YES → SKIP (log: Already posted)
    NO ↓
[12] Is preview mode enabled?
    YES → SHOW PREVIEW, mark as posted
    NO ↓
[13] POST TO TWITTER ✅
    ↓
Mark as posted, log success
END
```

---

## Guardrail Categories

### 1. Accessibility Guardrails

**What**: Can we access the content?

**Checks**:
- ✅ URL returns HTTP 200
- ✅ Content loads within 15 seconds
- ✅ No authentication required
- ✅ No CAPTCHA or bot detection

**Skip If**:
- ❌ HTTP 404, 403, 500
- ❌ Timeout after 15 seconds
- ❌ Paywall detected
- ❌ Requires login

**Logging**:
```
❌ Skipped: URL inaccessible (HTTP 404)
URL: https://example.com/poem
```

---

### 2. Structure Guardrails

**What**: Does it have required fields?

**Required Fields**:
1. Title (non-empty, not "Untitled")
2. Author (non-empty, not "Unknown")
3. Text (at least 20 characters)

**Skip If**:
- ❌ Missing title
- ❌ Missing author
- ❌ Missing or empty text
- ❌ Title is "Untitled", "Blog", "Home"
- ❌ Author is "Unknown", "Anonymous", "Poetry"

**Logging**:
```
❌ Skipped: Missing author
Title: "The Road Not Taken"
URL: https://example.com/poem
```

---

### 3. Content Type Guardrails

**What**: Is it actually a poem (not a review/interview/etc.)?

**Blocklist Patterns**:

#### Reviews & Criticism
- ❌ "reviewed by"
- ❌ "book review"
- ❌ "critique of"
- ❌ "analysis of"

#### Interviews & Features
- ❌ "interview with"
- ❌ "conversation with"
- ❌ "in conversation"
- ❌ "profile of"

#### Obituaries & Memorials
- ❌ "1945-2025" (birth-death years)
- ❌ "passed away"
- ❌ "in memoriam"
- ❌ "obituary"

#### Table of Contents / Issues
- ❌ "No. 44 Winter 2025"
- ❌ "Issue 12"
- ❌ "Table of Contents"
- ❌ "Contributors"

#### Submissions & Announcements
- ❌ "Call for submissions"
- ❌ "Submission guidelines"
- ❌ "Now accepting"
- ❌ "Deadline"

#### About Pages
- ❌ "About the author"
- ❌ "About the poet"
- ❌ "Biography"

**Action**: If content matches ANY pattern → SKIP

**Logging**:
```
❌ Skipped: Blocklist match (pattern: "reviewed by")
Title: "Last Day on Earth reviewed by Jane Zwart"
URL: https://example.com/review
```

---

### 4. Length Guardrails

**What**: Is the length appropriate for a poem?

**Word Count**:
- ✅ Minimum: 20 words
- ✅ Maximum: 600 words
- ❌ Below 20 → Too short (likely incomplete)
- ❌ Above 600 → Too long (likely essay or multiple poems)

**Line Count**:
- ✅ Minimum: 4 lines
- ✅ Maximum: 100 lines
- ❌ Below 4 → Not enough content
- ❌ Above 100 → Likely not a single poem

**Why These Limits**:
- 20-600 words captures 95% of poems
- Excludes haiku-only (too short for tweet)
- Excludes epic poems (too long to excerpt well)
- Excludes essays and prose

**Logging**:
```
❌ Skipped: Word count out of range (12 words)
Title: "Haiku Example"
URL: https://example.com/haiku

❌ Skipped: Word count out of range (1200 words)
Title: "Essay About Poetry"
URL: https://example.com/essay
```

---

### 5. Structure Analysis Guardrails

**What**: Does it look like poetry (not prose)?

**Average Line Length**:
- ✅ Poetry: Usually < 80 characters per line
- ⚠️ Borderline: 80-120 characters
- ❌ Prose: > 120 characters

**Very Long Lines**:
- ✅ Poetry: < 20% of lines over 200 chars
- ❌ Prose: > 20% of lines over 200 chars

**Why This Matters**:
- Prose has long, paragraph-like lines
- Poetry has intentional line breaks
- Catches essays that slipped through content filter

**Example - Prose** (reject):
```
This is a very long line that goes on and on with no intentional breaks at all, more like a paragraph than a poem, and this is characteristic of prose rather than poetry which typically has much shorter lines.
```

**Example - Poetry** (accept):
```
The trees are in their autumn beauty,
The woodland paths are dry,
Under the October twilight the water
Mirrors a still sky
```

**Logging**:
```
❌ Skipped: Average line too long (145 chars) - likely prose
Title: "Reflections on Poetry"
Word count: 450
URL: https://example.com/prose
```

---

### 6. Duplicate Prevention Guardrails

**What**: Have we posted this before?

**Check**:
- Compare URL against `data/posted_poems.json`
- Exact URL match

**Skip If**:
- ❌ URL already in posted_urls set

**Why URL-Based**:
- Same poem can have multiple URLs
- We don't want to post from same URL twice
- Even if it's updated/different poem later

**Logging**:
```
⏭️  Skipped: Already posted
Title: "The Wild Swans at Coole"
Author: W. B. Yeats
Posted on: 2026-01-03
URL: https://poems.com/poem/wild-swans
```

---

### 7. Posting Frequency Guardrails

**What**: Are we posting too often?

**Limits**:
- ✅ Maximum: 3 posts per day
- ✅ Minimum interval: 4 hours between posts
- ❌ Never post more than once per hour

**Why**:
- Twitter algorithm penalizes spam
- Audience can't engage with too many posts
- Quality over quantity

**Implementation**:
```python
# In future enhancement
last_post_time = tracker.get_last_post_time()
if datetime.now() - last_post_time < timedelta(hours=4):
    SKIP (log: Too soon since last post)
```

**Logging**:
```
⏸️  Skipped: Posted 2 hours ago (minimum 4 hours)
Next eligible post time: 2026-01-05 16:00:00 UTC
```

---

### 8. Source Diversity Guardrails

**What**: Are we posting from same source too often?

**Limits** (Future Enhancement):
- ✅ Maximum 2 posts from same source per day
- ✅ Try to rotate sources
- ❌ Never post same source consecutively if possible

**Why**:
- Show diverse curation
- If one source goes down, others available
- Better for audience engagement

**Implementation**:
```python
# In future enhancement
recent_sources = tracker.get_recent_sources(count=5)
if recent_sources.count(poem.source_name) >= 2:
    # Try another source first
    pass
```

---

## Special Cases

### Case 1: Classic Poems (Public Domain)

**Scenario**: Posting "The Road Not Taken" by Robert Frost

**Guardrails**:
- ✅ All normal guardrails apply
- ✅ Can post from any source that has it
- ✅ Check if posted before (even from different source)

**Note**: Classic poems may appear on multiple sources. Use URL-based duplicate detection to allow same poem from different sources.

---

### Case 2: Contemporary Poems (Copyright)

**Scenario**: Posting new poem from living poet

**Guardrails**:
- ✅ All normal guardrails apply
- ✅ Only post excerpt (4-6 lines) + link
- ✅ Always attribute source
- ✅ Always link to original

**Legal Safe Harbor**:
- We post excerpts (fair use)
- We link to original (drives traffic)
- We attribute author and source
- Educational/promotional purpose

---

### Case 3: Translation

**Scenario**: Poem translated from another language

**Guardrails**:
- ✅ All normal guardrails apply
- ✅ Credit both poet and translator if available
- ✅ Example: "Poem by Pablo Neruda, translated by Robert Bly"

**Handling**:
```python
# If translator info available in source
author = f"{poet_name}, translated by {translator_name}"
```

---

### Case 4: No Author Found

**Scenario**: Beautiful poem but no author attribution

**Guardrail**: SKIP

**Why**:
- Could be anonymous
- Could be extraction error
- Could be user-submitted (quality unknown)
- Better safe than sorry

**Logging**:
```
❌ Skipped: No author attribution found
Title: "Beautiful Sunset"
URL: https://example.com/poem
```

---

### Case 5: Anthology or Collection Page

**Scenario**: Source page lists multiple poems

**Guardrail**: Extract one poem only

**How**:
- Source extractor should identify individual poem
- If page has multiple poems, skip (or extract first only)
- Prefer sources with one-poem-per-page

**Example - BAD** (skip):
```html
<div class="anthology">
  <div class="poem">Poem 1...</div>
  <div class="poem">Poem 2...</div>
  <div class="poem">Poem 3...</div>
</div>
```

**Example - GOOD** (extract):
```html
<article class="single-poem">
  <h1>Title</h1>
  <div class="author">Author</div>
  <div class="content">Poem text...</div>
</article>
```

---

## Manual Override Cases

### When to Manually Review

**Triggers**:
1. Validation failures increasing
2. Low engagement on recent posts
3. Community feedback
4. Source HTML changed
5. New source being tested

**Process**:
1. Run in preview mode
2. Review output manually
3. Check tweet format
4. Verify poem quality
5. Only then enable live posting

**Review Checklist**:
- [ ] Is this actually a poem?
- [ ] Is the title correct?
- [ ] Is the author correct?
- [ ] Does the excerpt make sense?
- [ ] Is the URL correct?
- [ ] Does the tweet format look good?
- [ ] Would I want to read this?

---

## Logging & Monitoring

### What to Log

**Success**:
```
✅ Posted successfully
Title: "The Wild Swans at Coole"
Author: W. B. Yeats
Source: Poetry Daily
Lines: 24
Words: 156
Tweet length: 245 chars
URL: https://poems.com/poem/wild-swans
Tweet: https://twitter.com/user/status/123456
```

**Skipped - Validation Failure**:
```
❌ Skipped: Validation failed (blocklist match: "reviewed by")
Title: "Book Review: New Collection"
Source: Poetry Daily
URL: https://poems.com/review
```

**Skipped - Duplicate**:
```
⏭️  Skipped: Already posted
Title: "Stopping by Woods"
Author: Robert Frost
Posted: 2026-01-03
URL: https://poems.com/poem/woods
```

**Error - Extraction Failed**:
```
❌ Error: Failed to extract poem
Source: Poetry Daily
URL: https://poems.com/
Reason: Could not find title element
```

**Error - Source Down**:
```
❌ Error: Source unavailable
Source: Poetry Daily
URL: https://poems.com/
HTTP Status: 503
```

### What to Monitor

**Daily Metrics**:
- ✅ Successful posts
- ❌ Validation failures
- ⏭️  Duplicates skipped
- 🔧 Extraction errors

**Weekly Metrics**:
- 📊 Success rate by source
- 📈 Engagement per post
- 🎯 Validation pattern trends
- 🔄 Posting frequency

**Monthly Metrics**:
- 📚 Total poems posted
- 🌟 Top performing posts
- 📉 Declining sources (fix or remove)
- 💡 Opportunities for improvement

---

## Quality Assurance

### Daily QA (First Month)
- Review every post manually
- Check for false positives
- Verify engagement
- Adjust guardrails if needed

### Weekly QA (After First Month)
- Sample 7 recent posts
- Check quality
- Review skip logs
- Monitor metrics

### Monthly QA
- Full source audit
- Engagement analysis
- Guardrail effectiveness review
- Plan adjustments

---

## Guardrail Evolution

### When to Adjust Guardrails

**Tighten If**:
- False positives appearing
- Quality declining
- Community complaints
- Validation not catching bad content

**Loosen If**:
- Too many false negatives
- Missing good poems
- Sources changing format
- Community wants more content

**Examples**:

**Tightening**:
```python
# Before: 600 word max
# After seeing essays slip through
# After: 500 word max
max_word_count: 500
```

**Loosening**:
```python
# Before: 4 line minimum
# After missing good short poems
# After: 3 line minimum
min_line_count: 3
```

### Guardrail Versioning

Track changes:
```yaml
# guardrails_v1.yaml (Jan 2026)
word_count:
  min: 20
  max: 600

# guardrails_v2.yaml (Feb 2026)
word_count:
  min: 20
  max: 500  # Reduced after essay slip-through
```

---

## Emergency Procedures

### If Bot Posts Bad Content

**Immediate**:
1. Delete tweet
2. Add URL to blocklist
3. Stop bot
4. Review logs

**Within 24 Hours**:
1. Identify why validation failed
2. Update validation rules
3. Test thoroughly
4. Document incident
5. Resume posting

**Example**:
```
INCIDENT: Posted obituary instead of poem
Date: 2026-01-15
URL: https://example.com/memorial
Title: "In Memory of Poet X"

Root Cause: Blocklist pattern didn't catch "In Memory of"
Fix: Added to blocklist
Test: Verified catches similar patterns
Status: Resolved, bot resumed
```

### If Source Changes HTML

**Immediate**:
1. Stop extracting from that source
2. Log errors
3. Continue with other sources

**Within Week**:
1. Analyze new HTML structure
2. Update extractor
3. Test with 20+ examples
4. Resume using source

---

## Success Criteria

### Per-Post Success
- ✅ Is a real poem
- ✅ Has correct title
- ✅ Has correct author
- ✅ Excerpt is well-formatted
- ✅ URL works
- ✅ Tweet length < 280 chars

### Weekly Success
- ✅ 7/7 posts meet quality standard
- ✅ 0 community complaints
- ✅ Engagement > baseline
- ✅ 0 deleted tweets

### Monthly Success
- ✅ 30/30 posts meet quality standard
- ✅ Growing follower count
- ✅ Positive community feedback
- ✅ Sustainable maintenance effort

---

## Decision Framework Summary

**The Simple Version**:

1. **Can we access it?** (URL works)
2. **Is it complete?** (Has title, author, text)
3. **Is it actually a poem?** (Not review/interview/obituary)
4. **Is it the right length?** (20-600 words, 4-100 lines)
5. **Does it look like poetry?** (Not prose paragraphs)
6. **Have we posted it before?** (URL not in history)
7. **Are we posting too often?** (Respect frequency limits)

If ALL answers are YES → POST ✅

If ANY answer is NO → SKIP ❌

**When in doubt, skip.**

Quality over quantity. Every time.
