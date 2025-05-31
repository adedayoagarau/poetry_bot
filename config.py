# Configuration for Twitter Poetry Bot

# Bot Settings
BOT_SETTINGS = {
    'posts_per_day': 10,
    'max_ai_posts_per_day': 0,  # NEVER post AI-generated content
    'avoid_repeat_sources': False,  # Allow repeat sources for 10 posts/day
    'avoid_repeat_authors': False,  # Allow repeat authors for 10 posts/day
    'upload_media_v1_1': False,
    'post_times_utc': ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00']
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