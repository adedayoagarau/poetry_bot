def validate_poem_content(self, poem_data, url=None):
    """Enhanced validation that poem content is real and complete"""
    if not poem_data:
        return False, "No poem data provided"
    
    # Check required fields
    required_fields = ['title', 'author', 'text', 'source']
    for field in required_fields:
        if not poem_data.get(field):
            return False, f"Missing required field: {field}"
    
    text = poem_data['text'].strip()
    title = poem_data['title'].strip()
    
    # ENHANCED: URL accessibility check
    if url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0)'}
            response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
            if response.status_code >= 400:
                return False, f"URL not accessible: HTTP {response.status_code}"
        except Exception as e:
            return False, f"URL validation failed: {e}"
    
    # Basic length checks
    if len(text) < 30:
        return False, "Poem text too short (likely incomplete)"
    
    if len(text) > 3000:
        return False, "Content too long (likely essay, not poem)"
    
    # ENHANCED: Structure analysis for poetry vs prose
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if len(lines) < 2:
        return False, "Insufficient poem content (needs multiple lines)"
    
    # Check average line length (prose has much longer lines)
    avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
    long_lines = sum(1 for line in lines if len(line) > 120)
    very_long_lines = sum(1 for line in lines if len(line) > 200)
    
    # If most lines are very long, it's likely prose
    if avg_line_length > 100 and long_lines > len(lines) * 0.6:
        return False, "Content appears to be prose, not poetry (very long lines)"
    
    if very_long_lines > len(lines) * 0.3:
        return False, "Content contains prose paragraphs, not poetry lines"
    
    # ENHANCED: Essay/review detection (much more comprehensive)
    text_lower = text.lower()
    title_lower = title.lower()
    
    # Strong essay indicators
    essay_patterns = [
        'in this essay', 'the author argues', 'according to', 'furthermore',
        'in conclusion', 'to summarize', 'for example', 'such as',
        'the collection', 'the poet writes', 'as mentioned earlier',
        'drawing on', 'in fiction', 'in poetry', 'the speaker',
        'voice is', 'equally accessible', 'compelling', 'transformation needs',
        'slow build-up', 'can be transformative', 'leaves us with',
        'american poetry landscape', 'increasingly dominated',
        'instagramable verse', 'present-day politics',
        'refreshing return', 'lyric poetry', 'opening poem',
        'intersection of myth', 'human body', 'covers a range of themes',
        'most compelling when writing', 'drawing from the wells',
        'storytelling and science', 'guided me while writing',
        'full-length poetry collection', 'chronicle of drifting'
    ]
    
    essay_count = sum(1 for pattern in essay_patterns if pattern in text_lower)
    if essay_count >= 2:  # Lowered threshold for stricter validation
        return False, f"Content appears to be essay/review about poetry ({essay_count} essay patterns found)"
    
    # ENHANCED: Title analysis for non-poetry content
    problematic_titles = [
        'review of', 'essay', 'interview', 'conversation with', 'profile',
        'announcement', 'winner', 'prize', 'award', 'selected poems',
        'new and selected', 'biography', 'memoir', 'critical essay',
        'marie howe', 'ruth lilly', 'building the perfect',
        'poetry and lightness', 'lightness', 'six memos',
        'calvino', 'italo calvino', 'craft essay', 'poetics'
    ]
    
    for indicator in problematic_titles:
        if indicator in title_lower:
            return False, f"Title indicates non-poem content: '{indicator}' in '{title}'"
    
    # ENHANCED: Navigation/metadata detection
    nav_patterns = [
        'table of contents', 'contents', 'browse', 'archive', 'search results',
        'subscription', 'newsletter', 'featured', 'latest', 'recent',
        'shortlist', 'issue', 'volume', 'submissions', 'contest',
        'author index', 'title index', 'editorial board',
        'macarthur', 'national book award', 'poet laureate', 'pulitzer prize'
    ]
    
    nav_count = sum(1 for pattern in nav_patterns if pattern in text_lower)
    if nav_count >= 2:
        return False, "Content appears to be navigation/metadata, not actual poetry"
    
    # ENHANCED: Biographical content detection
    bio_patterns = [
        'first book', 'second book', 'latest book', 'published in', 'appears in',
        'winner of', 'recipient of', 'teaches at', 'professor at', 'lives in',
        'born in', 'graduated from', 'mfa', 'phd', 'university', 'college',
        'press', 'publisher', 'publication', 'four way books', 'copper canyon'
    ]
    
    bio_count = sum(1 for pattern in bio_patterns if pattern in text_lower)
    if bio_count >= 3:
        return False, f"Content appears to be biographical information ({bio_count} bio indicators)"
    
    # ENHANCED: Check for error pages
    error_patterns = [
        'page not found', '404', 'error', 'access denied',
        'subscription required', 'login required', 'not available',
        'coming soon', 'under construction', 'temporarily unavailable'
    ]
    
    for pattern in error_patterns:
        if pattern in text_lower:
            return False, f"Content contains error pattern: {pattern}"
    
    # ENHANCED: Publication/book description detection
    publication_phrases = [
        'first book', 'latest collection', 'new book', 'forthcoming',
        'new and selected', 'building the perfect', 'four way books',
        'copper canyon press', 'sixth book of poetry', 'chronicle of drifting'
    ]
    
    for phrase in publication_phrases:
        if phrase in text_lower:
            return False, f"Content appears to be publication description: '{phrase}'"
    
    # ENHANCED: Check for reasonable title and author
    if len(title) > 100:
        return False, "Title too long (likely extracted wrong content)"
    
    author = poem_data['author'].strip()
    if author.lower() in ['unknown', 'anonymous', ''] and 'ai generated' not in poem_data['source'].lower():
        return False, "Missing author information"
    
    # ENHANCED: Word count validation (more specific ranges)
    word_count = len(text.split())
    if word_count < 20:
        return False, f"Too short ({word_count} words) - likely incomplete"
    elif word_count > 800:
        return False, f"Too long ({word_count} words) - likely essay or multiple poems"
    
    return True, "Poem content validated successfully"
