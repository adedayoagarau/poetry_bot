# Configuration for Twitter Poetry Bot

# Bot Settings
BOT_SETTINGS = {
    'posts_per_day': 2,
    'max_ai_posts_per_day': 1,
    'avoid_repeat_sources': True,
    'avoid_repeat_authors': True,
    'upload_media_v1_1': False,
    'post_times_utc': ['09:00', '21:00']
}

# Weighted journal list for poem selection
def get_weighted_journal_list():
    """Return a weighted list of literary journals for poem selection"""
    journals = [
        {'name': 'Poetry Daily', 'url': 'https://poems.com'},
        {'name': 'The Adroit Journal', 'url': 'https://theadroitjournal.org'},
        {'name': 'Poetry Foundation', 'url': 'https://poetryfoundation.org'},
        {'name': 'Academy of American Poets', 'url': 'https://poets.org'},
        {'name': 'Poetry Magazine', 'url': 'https://poetrymagazine.org'},
        {'name': 'The Paris Review', 'url': 'https://theparisreview.org'},
        {'name': 'Poetry Northwest', 'url': 'https://poetrynw.org'},
        {'name': 'Barren Magazine', 'url': 'https://barrenmagazine.com'},
        {'name': 'Greensboro Review', 'url': 'https://greensbororeview.org'},
    ]
    
    # Create weighted list (some journals appear multiple times for higher probability)
    weighted_list = []
    for journal in journals:
        # Add each journal once (equal weight for now)
        weighted_list.append(journal)
    
    return weighted_list 