# Configuration for Twitter Poetry Bot - Enhanced Version
# Bot Settings
BOT_SETTINGS = {
    'posts_per_day': 10,
    'max_ai_posts_per_day': 0,  # NEVER post AI-generated content
    'avoid_repeat_sources': False,  # Allow repeat sources for 10 posts/day
    'avoid_repeat_authors': False,  # Allow repeat authors for 10 posts/day
    'upload_media_v1_1': False,
    'post_times_utc': ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00'],
    
    # NEW: Enhanced settings for better performance
    'max_urls_per_source': 15,  # Try more URLs per source
    'validation_cache_hours': 8,  # Cache validation results
    'failed_url_retry_hours': 48,  # Retry failed URLs after 48 hours
    'min_confidence_score': 0.6,  # Minimum confidence for posting
    'max_validation_attempts_per_run': 100,  # Prevent infinite loops
    
    # NEW: Quality controls
    'max_same_author_per_day': 3,  # Allow up to 3 poems from same author
    'max_same_source_per_day': 4,  # Allow up to 4 poems from same source
    'min_hours_between_same_author': 2,  # Space out same author posts
}

# Expanded journal list with 30 high-quality sources
def get_weighted_journal_list():
    """Return a weighted list of literary journals for poem selection"""
    
    # TIER 1: Best sources (appear 3 times in rotation)
    tier1_journals = [
        {'name': 'Poetry Daily', 'url': 'https://poems.com', 'weight': 3},
        {'name': 'Poetry Foundation', 'url': 'https://poetryfoundation.org', 'weight': 3},
        {'name': 'Academy of American Poets', 'url': 'https://poets.org', 'weight': 3},
        {'name': 'Verse Daily', 'url': 'https://versedaily.org', 'weight': 3},
    ]
    
    # TIER 2: University journals (appear 2 times)
    tier2_journals = [
        {'name': 'The Iowa Review', 'url': 'https://iowareview.org', 'weight': 2},
        {'name': 'The Missouri Review', 'url': 'https://missourireview.com', 'weight': 2},
        {'name': 'New England Review', 'url': 'https://nereview.com', 'weight': 2},
        {'name': 'The Georgia Review', 'url': 'https://thegeorgiareview.com', 'weight': 2},
        {'name': 'Colorado Review', 'url': 'https://coloradoreview.colostate.edu', 'weight': 2},
        {'name': 'Black Warrior Review', 'url': 'https://bwr.ua.edu', 'weight': 2},
    ]
    
    # TIER 3: Poetry-focused journals (appear once)
    tier3_journals = [
        {'name': 'Plume', 'url': 'https://plumepoetry.com', 'weight': 2},
        {'name': 'American Poetry Review', 'url': 'https://aprweb.org', 'weight': 2},
        {'name': 'Rattle', 'url': 'https://rattle.com', 'weight': 2},
        {'name': 'Poetry Northwest', 'url': 'https://poetrynw.org', 'weight': 1},
        {'name': 'The Adroit Journal', 'url': 'https://theadroitjournal.org', 'weight': 1},
        {'name': 'Poetry Magazine', 'url': 'https://poetrymagazine.org', 'weight': 2},
    ]
    
    # TIER 4: Online sources (appear once)
    tier4_journals = [
        {'name': 'Sky Island Journal', 'url': 'https://skyislandjournal.com', 'weight': 1},
        {'name': 'The Sunlight Press', 'url': 'https://thesunlightpress.com', 'weight': 1},
        {'name': 'Terrain.org', 'url': 'https://terrain.org', 'weight': 1},
        {'name': 'Chestnut Review', 'url': 'https://chestnutreview.com', 'weight': 1},
        {'name': 'The Common', 'url': 'https://thecommonmagazine.org', 'weight': 1},
        {'name': 'Narrative', 'url': 'https://narrativemagazine.com', 'weight': 1},
    ]
    
    # TIER 5: Your original sources (keeping them)
    tier5_journals = [
        {'name': 'The Paris Review', 'url': 'https://theparisreview.org', 'weight': 1},
        {'name': 'Barren Magazine', 'url': 'https://barrenmagazine.com', 'weight': 1},
        {'name': 'Greensboro Review', 'url': 'https://greensbororeview.org', 'weight': 1},
    ]
    
    # Combine all tiers
    all_journals = tier1_journals + tier2_journals + tier3_journals + tier4_journals + tier5_journals
    
    # Create weighted list based on weights
    weighted_list = []
    for journal in all_journals:
        weight = journal.get('weight', 1)
        for _ in range(weight):
            weighted_list.append({
                'name': journal['name'], 
                'url': journal['url']
            })
    
    print(f"✅ Loaded {len(all_journals)} unique sources, {len(weighted_list)} weighted entries")
    return weighted_list
