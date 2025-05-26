# Poetry Bot Configuration

# All themes have equal opportunity - no preferences
POETRY_THEMES = [
    "nature and seasons",
    "love and relationships", 
    "hope and dreams",
    "memories and nostalgia",
    "strength and resilience", 
    "beauty in simple moments",
    "the ocean and waves",
    "mountains and valleys",
    "stars and moonlight",
    "morning coffee",
    "rainy days",
    "sunset and dawn",
    "friendship",
    "gratitude",
    "courage",
    "peace and solitude",
    "change and growth",
    "home and comfort",
    "time and patience",
    "kindness and compassion",
    "urban landscapes",
    "modern connections",
    "digital age reflections",
    "changing times",
    "new beginnings",
    "quiet moments",
    "celebration",
    "loss and healing",
    "wonder and discovery",
    "freedom and expression"
]

# Image styling options
IMAGE_COLORS = {
    'backgrounds': [
        '#2C3E50',  # Dark blue-gray
        '#34495E',  # Dark gray
        '#8E44AD',  # Purple  
        '#2980B9',  # Blue
        '#16A085',  # Teal
        '#27AE60',  # Green
        '#E67E22',  # Orange
        '#E74C3C',  # Red
        '#F39C12',  # Yellow
        '#9B59B6'   # Light purple
    ],
    'text': [
        '#FFFFFF',  # White
        '#ECF0F1',  # Light gray
        '#BDC3C7',  # Gray
        '#F8C471',  # Light orange
        '#AED6F1',  # Light blue
        '#A9DFBF',  # Light green
    ]
}

# Social media hashtags
HASHTAGS = [
    '#WritingCommunity',
    '#PoetryCommunity'
]

# Literary journals and sources - Flattened for random selection with slight preference for major sources
LITERARY_JOURNALS = [
    # Major poetry sources (included multiple times for higher probability)
    {
        'name': 'Poetry Daily',
        'url': 'https://poems.com/',
        'selector': 'div.poem-text, .poem-body, main',
        'has_online_poems': True,
        'preferred': True
    },
    {
        'name': 'Poetry Foundation',
        'url': 'https://www.poetryfoundation.org/poems/browse',
        'selector': 'div.poem, div[data-view="poems"]',
        'has_online_poems': True,
        'preferred': True
    },
    {
        'name': 'Poetry Magazine',
        'url': 'https://www.poetrymagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True,
        'preferred': True
    },
    {
        'name': 'Verse Daily', 
        'url': 'https://www.versedaily.org/',
        'selector': 'div.poem, .poem-content, main',
        'has_online_poems': True,
        'preferred': True
    },
    
    # All other quality sources (equal opportunity)
    {
        'name': 'American Poetry Review',
        'url': 'https://aprweb.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Rattle Magazine',
        'url': 'https://rattle.com/poetry/',
        'selector': 'div.poem-text, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'AGNI',
        'url': 'https://agnionline.bu.edu/',
        'selector': 'div.poem, .entry-content, main',
        'has_online_poems': True
    },
    {
        'name': 'The Paris Review',
        'url': 'https://www.theparisreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Kenyon Review',
        'url': 'https://www.kenyonreview.org/',
        'selector': 'div.poem, .post-content, article',
        'has_online_poems': True
    },
    {
        'name': 'Ploughshares',
        'url': 'https://www.pshares.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Missouri Review',
        'url': 'https://www.missourireview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'New England Review',
        'url': 'http://www.nereview.com/',
        'selector': 'div.poem, .post-content',
        'has_online_poems': True
    },
    {
        'name': 'Prairie Schooner',
        'url': 'https://prairieschooner.unl.edu/',
        'selector': 'div.poem, .entry-content, article',
        'has_online_poems': True
    },
    {
        'name': 'The Georgia Review',
        'url': 'https://www.thegeorgiareview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Iowa Review',
        'url': 'https://iowareview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Colorado Review',
        'url': 'https://coloradoreview.colostate.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Southern Review',
        'url': 'https://thesouthernreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Boulevard Magazine',
        'url': 'https://boulevardmagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Black Warrior Review',
        'url': 'https://bwr.ua.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Conjunctions',
        'url': 'https://www.conjunctions.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Sewanee Review',
        'url': 'https://thesewaneereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Adroit Journal',
        'url': 'https://theadroitjournal.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Atticus Review',
        'url': 'https://atticusreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Barren Magazine',
        'url': 'https://barrenmagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Entropy Magazine',
        'url': 'https://entropymag.org/',
        'selector': 'div.poem, .entry-content, article',
        'has_online_poems': True
    },
    {
        'name': 'Narrative Magazine',
        'url': 'https://www.narrativemagazine.com/',
        'selector': 'div.poem, .story-text',
        'has_online_poems': True
    },
    {
        'name': 'Salamander Magazine',
        'url': 'https://salamandermag.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Tin House',
        'url': 'https://tinhouse.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Ghost City Review',
        'url': 'https://ghostcitypress.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Frontier Poetry',
        'url': 'https://www.frontierpoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Palette Poetry',
        'url': 'https://www.palettepoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'SWWIM Every Day',
        'url': 'https://www.swwim.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Poetry Northwest',
        'url': 'https://www.poetrynw.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Yes Poetry',
        'url': 'https://www.yespoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Diode Poetry Journal',
        'url': 'http://diodepoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Rumpus',
        'url': 'https://therumpus.net/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    }
]

# Create weighted list for random selection (preferred sources appear more often)
def get_weighted_journal_list():
    """Create a weighted list giving preferred sources higher probability"""
    weighted_list = []
    for journal in LITERARY_JOURNALS:
        if journal.get('preferred', False):
            # Preferred sources appear 5 times (5x probability) - they work better
            weighted_list.extend([journal] * 5)
        else:
            # Regular sources appear once
            weighted_list.append(journal)
    return weighted_list

# Bot behavior settings - Simplified and egalitarian
BOT_SETTINGS = {
    'posts_per_day': 10,                    # 10 posts per day for Twitter
    'post_times_utc': ['00:00', '02:24', '04:48', '07:12', '09:36', '12:00', '14:24', '16:48', '19:12', '21:36'],  # Every ~2.4 hours
    'max_poem_length': 500,                 # Allow longer poems (we'll extract best lines)
    'backup_to_ai': False,                  # NO AI - ONLY REAL POEMS
    'create_images': False,                 # Focus on text-only posts with links
    'include_source': True,                 # Always include source attribution
    'random_selection': True,               # Random selection, no tiers
    'avoid_repeat_authors': False,          # Allow repeat authors (we need 10 posts/day)
    'avoid_repeat_sources': False,          # Allow repeat sources (we need 10 posts/day)
    'max_ai_posts_per_day': 0,              # NO AI CONTENT ALLOWED
    'post_format': 'excerpt',               # Post up to 4 lines only
    'include_poem_links': True,             # Always include link to full poem
    'equal_opportunity': True,              # All poets get equal chance
    'require_real_poems_only': True,        # ONLY real poems from journals
}

# Content filters (poems containing these words will be skipped)
CONTENT_FILTERS = [
    # Add words here that you want to avoid
    'explicit',
    'inappropriate', 
    # You can add more filters as needed
]

# Custom prompts for AI generation
AI_PROMPTS = {
    'standard': "Write a beautiful, short poem about {theme}. Keep it under 200 characters, suitable for social media. Make it inspiring and thoughtful.",
    'haiku': "Write a traditional haiku about {theme}. Follow the 5-7-5 syllable pattern exactly.",
    'inspirational': "Write an uplifting and inspiring short poem about {theme}. Focus on hope, strength, and beauty.",
    'nature': "Write a vivid, nature-focused poem about {theme}. Use rich imagery and sensory details.",
}

# Seasonal themes (bot will prefer these during relevant months)
SEASONAL_THEMES = {
    'spring': ['renewal', 'growth', 'flowers blooming', 'fresh beginnings'],
    'summer': ['sunshine', 'warm days', 'long evenings', 'freedom'],  
    'autumn': ['falling leaves', 'harvest', 'change', 'golden colors'],
    'winter': ['snow', 'quiet moments', 'warmth inside', 'reflection']
}