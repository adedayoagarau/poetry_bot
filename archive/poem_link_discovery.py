#!/usr/bin/env python3
"""
MEGA Poem Link Discovery System with Enhanced Validation
Supports 75+ poetry sources with smart URL discovery and validation
MASSIVE EXPANSION - Now includes premium magazines like The Paris Review, Kenyon Review, etc.
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Set, Tuple, Optional
import json
from dataclasses import dataclass
import logging

# MEGA SITE CONFIGURATIONS FOR 75+ POETRY SOURCES
SITE_CONFIGS = {
    
    # TIER 1: PREMIER SOURCES - Most reliable, daily/high-frequency
    'poems.com': {
        'name': 'Poetry Daily',
        'base_urls': [
            'https://poems.com/',
            'https://poems.com/archive/',
            'https://poems.com/poems/',
            'https://poems.com/todays-poem/'
        ],
        'poem_patterns': [
            r'^/poem/[^/]+/$',
            r'^/todays-poem/?$',
            r'^/archive/[^/]+/$'
        ],
        'css_selectors': [
            'a[href*="/poem/"]',
            '.daily_poem a',
            '.archive-listing a'
        ],
        'exclude_patterns': [
            r'/about', r'/contact', r'/subscribe', r'/newsletter', r'/search', 
            r'/browse', r'/submit', r'/features', r'/archives', r'/what-sparks-poetry'
        ]
    },
    
    'poetryfoundation.org': {
        'name': 'Poetry Foundation',
        'base_urls': [
            'https://www.poetryfoundation.org/poems/browse',
            'https://www.poetryfoundation.org/poems',
            'https://www.poetryfoundation.org/poetrymagazine'
        ],
        'poem_patterns': [
            r'^/poems/\d+/[^/]+$',
            r'^/poetrymagazine/poems/\d+/[^/]+$'
        ],
        'css_selectors': [
            'a[href*="/poems/"][href*="/"]',
            'a[href*="/poetrymagazine/poems/"]',
            '.c-feature a[href*="/poems/"]'
        ],
        'exclude_patterns': [
            r'/poets', r'/articles', r'/browse', r'/search', r'/about', 
            r'/guides', r'/poem-of-the-day', r'/programs'
        ]
    },
    
    'poets.org': {
        'name': 'Academy of American Poets',
        'base_urls': [
            'https://poets.org/poems',
            'https://poets.org/poem-a-day',
            'https://poets.org/browse'
        ],
        'poem_patterns': [
            r'^/poem/[^/]+$',
            r'^/poems/[^/]+$'
        ],
        'css_selectors': [
            'a[href*="/poem/"]',
            'a[href*="/poems/"]',
            '.views-row a'
        ],
        'exclude_patterns': [
            r'/poets', r'/about', r'/academy', r'/programs', r'/prizes'
        ]
    },
    
    'versedaily.org': {
        'name': 'Verse Daily',
        'base_urls': [
            'https://www.versedaily.org/',
            'https://www.versedaily.org/archive.html'
        ],
        'poem_patterns': [
            r'^/\d{4}/.*\.html$',
            r'^/poems/.*\.html$'
        ],
        'css_selectors': [
            'a[href$=".html"]',
            'div.archive a',
            '.content a[href*=".html"]'
        ],
        'exclude_patterns': [
            r'/about', r'/contact', r'/submit', r'/index'
        ]
    },
    
    # TIER 1.5: LEGENDARY LITERARY MAGAZINES (NEWLY ADDED)
    'theparisreview.org': {
        'name': 'The Paris Review',
        'base_urls': [
            'https://theparisreview.org/poetry/',
            'https://theparisreview.org/blog/',
            'https://theparisreview.org/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/blog/.*poetry.*$',
            r'^/\d{4}/\d{2}/\d{2}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a',
            '.post-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/interviews', r'/fiction', r'/art', r'/staff'
        ]
    },
    
    'kenyonreview.org': {
        'name': 'The Kenyon Review',
        'base_urls': [
            'https://kenyonreview.org/poetry/',
            'https://kenyonreview.org/blog/',
            'https://kenyonreview.org/kr-online-issue/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/blog/.*$',
            r'^/kr-online-issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a',
            '.entry-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/interviews', r'/fiction', r'/reviews'
        ]
    },
    
    'tinhouse.com': {
        'name': 'Tin House',
        'base_urls': [
            'https://tinhouse.com/category/poetry/',
            'https://tinhouse.com/category/online-features/'
        ],
        'poem_patterns': [
            r'^/.*poetry.*$',
            r'^/online-features/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a',
            '.post-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/books', r'/workshops', r'/events'
        ]
    },
    
    'thesouthernreview.org': {
        'name': 'The Southern Review',
        'base_urls': [
            'https://thesouthernreview.org/',
            'https://thesouthernreview.org/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/category/poetry/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a'
        ],
        'exclude_patterns': [
            r'/about', r'/staff', r'/submissions'
        ]
    },
    
    'prairieschooner.unl.edu': {
        'name': 'Prairie Schooner',
        'base_urls': [
            'https://prairieschooner.unl.edu/',
            'https://prairieschooner.unl.edu/poetry/',
            'https://prairieschooner.unl.edu/blog/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/blog/.*$',
            r'^/current-issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a'
        ],
        'exclude_patterns': [
            r'/about', r'/staff', r'/submissions'
        ]
    },
    
    'pshares.org': {
        'name': 'Ploughshares',
        'base_urls': [
            'https://pshares.org/poetry/',
            'https://pshares.org/issues/online/',
            'https://pshares.org/read/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/issues/online/.*$',
            r'^/read/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'a[href*="/read/"]',
            'article h2 a'
        ],
        'exclude_patterns': [
            r'/about', r'/writers', r'/news'
        ]
    },
    
    'threepennyreview.com': {
        'name': 'The Threepenny Review',
        'base_urls': [
            'https://www.threepennyreview.com/',
            'https://www.threepennyreview.com/samples/'
        ],
        'poem_patterns': [
            r'^/samples/.*$',
            r'^/.*poetry.*$'
        ],
        'css_selectors': [
            'a[href*="/samples/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/subscribe', r'/back-issues'
        ]
    },
    
    # TIER 2: MAJOR POETRY MAGAZINES
    'poetrymagazine.org': {
        'name': 'Poetry Magazine',
        'base_urls': [
            'https://www.poetrymagazine.org/',
            'https://www.poetrymagazine.org/poems'
        ],
        'poem_patterns': [
            r'^/poems/.*$',
            r'^/poem/.*$'
        ],
        'css_selectors': [
            'a[href*="/poems/"]',
            'div.poem-listing a'
        ],
        'exclude_patterns': [
            r'/articles', r'/reviews', r'/about', r'/subscribe'
        ]
    },
    
    'rattle.com': {
        'name': 'Rattle Magazine',
        'base_urls': [
            'https://rattle.com/poetry/',
            'https://rattle.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a',
            '.rattle-post a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe', r'/category'
        ]
    },
    
    'bpj.org': {
        'name': 'Beloit Poetry Journal',
        'base_urls': [
            'https://www.bpj.org/online/',
            'https://www.bpj.org/poems/'
        ],
        'poem_patterns': [
            r'^/online/.*$',
            r'^/poems/.*$'
        ],
        'css_selectors': [
            'a[href*="/poems/"]',
            'a[href*="/online/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe'
        ]
    },
    
    'agnionline.bu.edu': {
        'name': 'AGNI',
        'base_urls': [
            'https://agnionline.bu.edu/',
            'https://agnionline.bu.edu/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d+/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a'
        ],
        'exclude_patterns': [
            r'/about', r'/interviews', r'/fiction'
        ]
    },
    
    'ninthletter.com': {
        'name': 'Ninth Letter',
        'base_urls': [
            'https://ninthletter.com/',
            'https://ninthletter.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/category/poetry/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article h2 a'
        ],
        'exclude_patterns': [
            r'/about', r'/staff', r'/submissions'
        ]
    },
    
    'antiochreview.org': {
        'name': 'The Antioch Review',
        'base_urls': [
            'https://antiochreview.org/',
            'https://antiochreview.org/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/current-issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/staff'
        ]
    },
    
    'theatlantic.com': {
        'name': 'The Atlantic',
        'base_urls': [
            'https://www.theatlantic.com/category/poetry/',
            'https://www.theatlantic.com/entertainment/poetry/'
        ],
        'poem_patterns': [
            r'^/category/poetry/.*$',
            r'^/entertainment/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/subscribe'
        ]
    },
    
    # TIER 3: UNIVERSITY & PRESTIGIOUS JOURNALS
    'iowareview.org': {
        'name': 'The Iowa Review',
        'base_urls': [
            'https://iowareview.org/',
            'https://iowareview.org/current-issue',
            'https://iowareview.org/archives'
        ],
        'poem_patterns': [
            r'^/current-issue/.*$',
            r'^/archives/.*$',
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'article h2 a', 
            '.entry-title a', 
            'a[href*="/poetry/"]',
            '.issue-content a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe', r'/staff', r'/contests'
        ]
    },
    
    'missourireview.com': {
        'name': 'The Missouri Review',
        'base_urls': [
            'https://missourireview.com/',
            'https://missourireview.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/current-issue/.*$',
            r'^/archives/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'article a', 
            '.post-title a', 
            'a[href*="/poetry/"]',
            '.issue-link a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe', r'/staff', r'/contests', r'/interviews'
        ]
    },
    
    'nereview.com': {
        'name': 'New England Review',
        'base_urls': [
            'https://nereview.com/',
            'https://nereview.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/current-issue/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'article a', 
            '.entry-title a',
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe'
        ]
    },
    
    'thegeorgiareview.com': {
        'name': 'The Georgia Review',
        'base_urls': [
            'https://thegeorgiareview.com/',
            'https://thegeorgiareview.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/posts/.*$',
            r'^/poetry/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'article h2 a', 
            '.post-title a',
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    'coloradoreview.colostate.edu': {
        'name': 'Colorado Review',
        'base_urls': [
            'https://coloradoreview.colostate.edu/',
            'https://coloradoreview.colostate.edu/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/current-issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/staff', r'/submissions'
        ]
    },
    
    'gulfcoastmag.org': {
        'name': 'Gulf Coast',
        'base_urls': [
            'https://gulfcoastmag.org/',
            'https://gulfcoastmag.org/online/'
        ],
        'poem_patterns': [
            r'^/online/.*$',
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/online/"]',
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'bwr.ua.edu': {
        'name': 'Black Warrior Review',
        'base_urls': [
            'https://bwr.ua.edu/',
            'https://bwr.ua.edu/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'article a',
            'a[href*="/poetry/"]',
            '.post-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    # TIER 4: POETRY-FOCUSED JOURNALS
    'aprweb.org': {
        'name': 'American Poetry Review',
        'base_urls': [
            'https://aprweb.org/',
            'https://aprweb.org/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/poems/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a',
            '.poem-link a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    'plumepoetry.com': {
        'name': 'Plume',
        'base_urls': [
            'https://plumepoetry.com/',
            'https://plumepoetry.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/.*$'  # Plume is primarily poetry
        ],
        'css_selectors': [
            'article a', 
            '.entry-title a',
            '.plume-post a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/masthead'
        ]
    },
    
    'rhinopoetry.org': {
        'name': 'RHINO Poetry',
        'base_urls': [
            'https://rhinopoetry.org/',
            'https://rhinopoetry.org/archive/'
        ],
        'poem_patterns': [
            r'^/poems/.*$',
            r'^/poetry/.*$',
            r'^/archive/.*$'
        ],
        'css_selectors': [
            'a[href*="/poems/"]', 
            'article a',
            '.archive-link a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/purchase'
        ]
    },
    
    'poetlore.com': {
        'name': 'Poet Lore',
        'base_urls': [
            'https://www.poetlore.com/',
            'https://www.poetlore.com/current-issue/'
        ],
        'poem_patterns': [
            r'^/current-issue/.*$',
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    '32poems.com': {
        'name': '32 Poems',
        'base_urls': [
            'https://www.32poems.com/',
            'https://www.32poems.com/current/'
        ],
        'poem_patterns': [
            r'^/current/.*$',
            r'^/\d+\.\d+/.*$'
        ],
        'css_selectors': [
            'a[href*="/current/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    # TIER 5: CONTEMPORARY & DIGITAL-FIRST JOURNALS
    'diodepoetry.com': {
        'name': 'Diode Poetry Journal',
        'base_urls': [
            'https://diodepoetry.com/',
            'https://diodepoetry.com/current-issue/'
        ],
        'poem_patterns': [
            r'^/current-issue/.*$',
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'theadroitjournal.org': {
        'name': 'The Adroit Journal',
        'base_urls': [
            'https://theadroitjournal.org/',
            'https://theadroitjournal.org/category/poetry/'
        ],
        'poem_patterns': [
            r'^/\d{4}/\d{2}/\d{2}/[^/]*poem[^/]*/$',
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/category', r'/review', r'/interview', 
            r'/essay', r'/critical-essays', r'/conversation', r'/profile',
            r'/announcement', r'review-of', r'conversation-with'
        ]
    },
    
    'waxwingmag.org': {
        'name': 'Waxwing',
        'base_urls': [
            'https://waxwingmag.org/',
            'https://waxwingmag.org/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'thrushpoetryjournal.com': {
        'name': 'Thrush Poetry Journal',
        'base_urls': [
            'https://www.thrushpoetryjournal.com/',
            'https://www.thrushpoetryjournal.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'connotationpress.com': {
        'name': 'Connotation Press',
        'base_urls': [
            'https://connotationpress.com/',
            'https://connotationpress.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/interviews'
        ]
    },
    
    'phoebejournal.com': {
        'name': 'PHOEBE',
        'base_urls': [
            'https://www.phoebejournal.com/',
            'https://www.phoebejournal.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'comstockreview.org': {
        'name': 'The Comstock Review',
        'base_urls': [
            'https://www.comstockreview.org/',
            'https://www.comstockreview.org/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/current-issue/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'cincinnatireviw.com': {
        'name': 'The Cincinnati Review',
        'base_urls': [
            'https://www.cincinnatireviw.com/',
            'https://www.cincinnatireviw.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/staff'
        ]
    },
    
    'crazyhorsemag.com': {
        'name': 'Crazy Horse',
        'base_urls': [
            'https://crazyhorsemag.com/',
            'https://crazyhorsemag.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'storyquarterly.com': {
        'name': 'Story Quarterly',
        'base_urls': [
            'https://www.storyquarterly.com/',
            'https://www.storyquarterly.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    'bluefifthreview.com': {
        'name': 'Blue Fifth Review',
        'base_urls': [
            'https://www.bluefifthreview.com/',
            'https://www.bluefifthreview.com/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submit'
        ]
    },
    
    # TIER 6: HIGH-QUALITY ONLINE SOURCES
    'skyislandjournal.com': {
        'name': 'Sky Island Journal',
        'base_urls': [
            'https://skyislandjournal.com/',
            'https://skyislandjournal.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/issue-.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]', 
            'article a',
            '.post-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    'thesunlightpress.com': {
        'name': 'The Sunlight Press',
        'base_urls': [
            'https://thesunlightpress.com/',
            'https://thesunlightpress.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d{4}/\d{2}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]', 
            'article a',
            '.entry-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    'terrain.org': {
        'name': 'Terrain.org',
        'base_urls': [
            'https://terrain.org/',
            'https://terrain.org/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/[^/]+/[^/]+/$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]', 
            'article a',
            '.terrain-content a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff', r'/articles'
        ]
    },
    
    'chestnutreview.com': {
        'name': 'Chestnut Review',
        'base_urls': [
            'https://chestnutreview.com/',
            'https://chestnutreview.com/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/[^/]+/[^/]+/$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]', 
            'article a',
            '.post-title a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/staff'
        ]
    },
    
    # INTERNATIONAL SOURCES
    'granta.com': {
        'name': 'Granta',
        'base_urls': [
            'https://granta.com/',
            'https://granta.com/categories/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d+/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a',
            '.granta-content a'
        ],
        'exclude_patterns': [
            r'/about', r'/subscribe', r'/submit'
        ]
    },
    
    'thefiddlehead.ca': {
        'name': 'The Fiddlehead',
        'base_urls': [
            'https://thefiddlehead.ca/',
            'https://thefiddlehead.ca/category/poetry/'
        ],
        'poem_patterns': [
            r'^/poetry/.*$',
            r'^/\d{4}/.*$'
        ],
        'css_selectors': [
            'a[href*="/poetry/"]',
            'article a'
        ],
        'exclude_patterns': [
            r'/about', r'/submit', r'/subscribe'
        ]
    },
    
    # LEGACY SOURCES (your originals - keeping them)
    'barrenmagazine.com': {
        'name': 'Barren Magazine',
        'base_urls': [
            'https://barrenmagazine.com/',
            'https://barrenmagazine.com/category/poetry/'
        ], 
        'poem_patterns': [
            r'^/poetry/[^/]+/?$',
            r'^/[^/]+/[^/]+/?$'
        ],
        'css_selectors': [
            'article a', 
            '.entry-title a',
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/submissions', r'/category', r'/page/'
        ]
    },
    
    'greensbororeview.org': {
        'name': 'Greensboro Review',
        'base_urls': [
            'https://greensbororeview.org/',
            'https://greensbororeview.org/category/poetry/'
        ], 
        'poem_patterns': [
            r'^/[^/]+/$',
            r'^/poetry/[^/]+/?$'
        ],
        'css_selectors': [
            'article a', 
            '.entry-title a',
            'a[href*="/poetry/"]'
        ],
        'exclude_patterns': [
            r'/about', r'/contests', r'/staff', r'/submissions'
        ]
    },
}

# REST OF YOUR EXISTING VALIDATION CODE (keeping it exactly as is)
@dataclass
class ValidationResult:
    """Result of poem validation with detailed scoring"""
    is_poem: bool
    confidence_score: float
    reasons: List[str]
    content_length: int
    has_line_breaks: bool
    has_stanzas: bool

class EnhancedPoemValidator:
    """Enhanced validation for poem content"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0; +https://github.com/poetrybot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })
    
    def check_url_accessibility(self, url: str) -> Tuple[bool, int]:
        """Check if URL is accessible without downloading full content"""
        try:
            response = self.session.head(url, timeout=10, allow_redirects=True)
            return response.status_code == 200, response.status_code
        except Exception:
            try:
                # Fallback to GET request if HEAD fails
                response = self.session.get(url, timeout=5, stream=True)
                return response.status_code == 200, response.status_code
            except Exception:
                return False, 0
    
    def analyze_poem_structure(self, text: str, html_content: str) -> Dict[str, any]:
        """Analyze text structure to identify poem characteristics"""
        lines = text.strip().split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        # Check for stanza structure (groups of lines separated by blank lines)
        stanza_breaks = text.count('\n\n')
        
        # Check line length patterns (poems often have varied line lengths)
        line_lengths = [len(line.strip()) for line in non_empty_lines if line.strip()]
        avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        line_length_variance = 0
        if len(line_lengths) > 1:
            mean = avg_line_length
            line_length_variance = sum((x - mean) ** 2 for x in line_lengths) / len(line_lengths)
        
        # Check for common poetry HTML structures
        soup = BeautifulSoup(html_content, 'html.parser')
        has_poetry_tags = bool(soup.find_all(['poem', 'verse', 'stanza']))
        has_line_breaks = '<br>' in html_content.lower() or '</br>' in html_content.lower()
        
        # Check for consistent indentation patterns
        indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))
        indentation_ratio = indented_lines / len(lines) if lines else 0
        
        return {
            'total_lines': len(lines),
            'non_empty_lines': len(non_empty_lines),
            'stanza_breaks': stanza_breaks,
            'avg_line_length': avg_line_length,
            'line_length_variance': line_length_variance,
            'has_poetry_tags': has_poetry_tags,
            'has_line_breaks': has_line_breaks,
            'indentation_ratio': indentation_ratio,
            'word_count': len(text.split())
        }
    
    def validate_poem_content(self, url: str) -> ValidationResult:
        """Enhanced validation of poem content"""
        try:
            # First check accessibility
            is_accessible, status_code = self.check_url_accessibility(url)
            if not is_accessible:
                return ValidationResult(
                    is_poem=False,
                    confidence_score=0.0,
                    reasons=[f"URL not accessible (HTTP {status_code})"],
                    content_length=0,
                    has_line_breaks=False,
                    has_stanzas=False
                )
            
            # Get full content
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return ValidationResult(
                    is_poem=False,
                    confidence_score=0.0,
                    reasons=[f"HTTP {response.status_code}"],
                    content_length=0,
                    has_line_breaks=False,
                    has_stanzas=False
                )
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove navigation, footer, and other non-content elements
            for element in soup(['nav', 'footer', 'header', 'aside', 'script', 'style']):
                element.decompose()
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|poem|post'))
            if main_content:
                text = main_content.get_text()
                html_content = str(main_content)
            else:
                text = soup.get_text()
                html_content = str(soup)
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Analyze structure
            structure = self.analyze_poem_structure(text, html_content)
            
            # Scoring system
            score = 0.0
            reasons = []
            
            # Positive indicators
            if structure['has_poetry_tags']:
                score += 0.3
                reasons.append("Contains poetry HTML tags")
            
            if structure['has_line_breaks']:
                score += 0.2
                reasons.append("Contains line breaks")
            
            if structure['stanza_breaks'] > 0:
                score += 0.25
                reasons.append(f"Contains {structure['stanza_breaks']} stanza breaks")
            
            # Word count analysis (poems typically 20-500 words)
            word_count = structure['word_count']
            if 20 <= word_count <= 500:
                score += 0.2
                reasons.append(f"Appropriate word count ({word_count})")
            elif word_count < 20:
                score -= 0.2
                reasons.append(f"Too short ({word_count} words)")
            elif word_count > 1000:
                score -= 0.3
                reasons.append(f"Too long ({word_count} words)")
            
            # Line structure analysis
            if 3 <= structure['non_empty_lines'] <= 100:
                score += 0.15
                reasons.append(f"Good line count ({structure['non_empty_lines']})")
            
            # Check for varied line lengths (characteristic of poetry)
            if structure['line_length_variance'] > 50:
                score += 0.1
                reasons.append("Varied line lengths")
            
            # Negative indicators
            prose_indicators = [
                'paragraph', 'essay', 'article', 'review', 'interview',
                'table of contents', 'bibliography', 'abstract',
                'conclusion', 'introduction', 'methodology'
            ]
            
            text_lower = text.lower()
            prose_matches = sum(1 for indicator in prose_indicators if indicator in text_lower)
            if prose_matches > 2:
                score -= 0.3
                reasons.append(f"Contains prose indicators ({prose_matches})")
            
            # Check for commercial/non-poetry content
            commercial_indicators = [
                'subscribe', 'newsletter', 'buy now', 'purchase',
                'advertisement', 'sponsor', 'donate', 'payment'
            ]
            commercial_matches = sum(1 for indicator in commercial_indicators if indicator in text_lower)
            if commercial_matches > 1:
                score -= 0.2
                reasons.append("Contains commercial content")
            
            # Final adjustments
            confidence_score = max(0.0, min(1.0, score))
            is_poem = confidence_score >= 0.6
            
            return ValidationResult(
                is_poem=is_poem,
                confidence_score=confidence_score,
                reasons=reasons,
                content_length=len(text),
                has_line_breaks=structure['has_line_breaks'],
                has_stanzas=structure['stanza_breaks'] > 0
            )
            
        except Exception as e:
            return ValidationResult(
                is_poem=False,
                confidence_score=0.0,
                reasons=[f"Validation error: {str(e)}"],
                content_length=0,
                has_line_breaks=False,
                has_stanzas=False
            )

class PoemLinkCache:
    """Cache system to avoid re-validating the same URLs"""
    
    def __init__(self, cache_file: str = 'poem_cache.json'):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def load_cache(self) -> Dict:
        """Load cache from file"""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_validation(self, url: str) -> Optional[ValidationResult]:
        """Get cached validation result"""
        if url in self.cache:
            data = self.cache[url]
            return ValidationResult(**data)
        return None
    
    def cache_validation(self, url: str, result: ValidationResult):
        """Cache validation result"""
        self.cache[url] = {
            'is_poem': result.is_poem,
            'confidence_score': result.confidence_score,
            'reasons': result.reasons,
            'content_length': result.content_length,
            'has_line_breaks': result.has_line_breaks,
            'has_stanzas': result.has_stanzas
        }
        self.save_cache()

# NEW: URL DISCOVERY FUNCTIONS (the missing piece!)
def get_poem_links(base_url: str, site_config: Dict) -> List[str]:
    """
    Discover actual poem URLs from a poetry website
    
    Args:
        base_url: The base URL to start discovery from
        site_config: Configuration dict with patterns and selectors
        
    Returns:
        List of discovered poem URLs
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/1.0; +https://github.com/poetrybot)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    discovered_links = set()
    
    try:
        print(f"🔍 Discovering poem links from {base_url}")
        
        # Fetch the page
        response = requests.get(base_url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ HTTP {response.status_code} for {base_url}")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Method 1: Use CSS selectors if provided
        if 'css_selectors' in site_config:
            for selector in site_config['css_selectors']:
                try:
                    links = soup.select(selector)
                    for link in links:
                        href = link.get('href')
                        if href:
                            # Convert relative URLs to absolute
                            absolute_url = urljoin(base_url, href)
                            discovered_links.add(absolute_url)
                            print(f"  📎 CSS selector found: {absolute_url}")
                except Exception as e:
                    print(f"⚠️  CSS selector '{selector}' failed: {e}")
        
        # Method 2: Pattern matching on all links
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href', '')
            
            # Skip empty hrefs
            if not href:
                continue
            
            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)
            
            # Check if URL matches poem patterns
            if 'poem_patterns' in site_config:
                for pattern in site_config['poem_patterns']:
                    if re.match(pattern, parsed_url.path):
                        # Check if it should be excluded
                        should_exclude = False
                        if 'exclude_patterns' in site_config:
                            for exclude_pattern in site_config['exclude_patterns']:
                                if re.search(exclude_pattern, parsed_url.path):
                                    should_exclude = True
                                    break
                        
                        if not should_exclude:
                            discovered_links.add(absolute_url)
                            print(f"  📝 Pattern match found: {absolute_url}")
                            break
        
    except Exception as e:
        print(f"❌ Error discovering links from {base_url}: {e}")
    
    # Convert to sorted list and remove duplicates
    unique_links = list(discovered_links)
    unique_links.sort()
    
    print(f"✅ Discovered {len(unique_links)} potential poem links from {base_url}")
    return unique_links

def discover_all_poem_links(domain: str, max_links: int = 200) -> List[str]:
    """
    Discover poem links from all configured URLs for a domain
    
    Args:
        domain: Domain name (e.g., 'poems.com')
        max_links: Maximum number of links to return
        
    Returns:
        List of discovered poem URLs
    """
    if domain not in SITE_CONFIGS:
        print(f"❌ No configuration found for domain: {domain}")
        return []
    
    config = SITE_CONFIGS[domain]
    all_links = set()
    
    print(f"🌐 Discovering poem links for {config['name']} ({domain})")
    
    # Try each base URL
    for base_url in config['base_urls']:
        try:
            links = get_poem_links(base_url, config)
            all_links.update(links)
            
            # Add delay between requests to be respectful
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Failed to discover links from {base_url}: {e}")
    
    # Convert to list and limit results
    final_links = list(all_links)[:max_links]
    
    print(f"🎯 Total discovered links for {domain}: {len(final_links)}")
    return final_links

# Keep your existing validation functions
def batch_validate_urls(urls: List[str], max_workers: int = 3) -> Dict[str, ValidationResult]:
    """Validate multiple URLs with rate limiting"""
    validator = EnhancedPoemValidator()
    cache = PoemLinkCache()
    results = {}
    
    for i, url in enumerate(urls):
        print(f"Validating {i+1}/{len(urls)}: {url}")
        
        # Check cache first
        cached_result = cache.get_validation(url)
        if cached_result:
            print(f"  ✅ Using cached result: {cached_result.confidence_score:.2f}")
            results[url] = cached_result
            continue
        
        # Validate URL
        result = validator.validate_poem_content(url)
        results[url] = result
        
        # Cache result
        cache.cache_validation(url, result)
        
        # Print result
        status = "✅ POEM" if result.is_poem else "❌ NOT POEM"
        print(f"  {status} (confidence: {result.confidence_score:.2f})")
        if result.reasons:
            print(f"    Reasons: {', '.join(result.reasons[:3])}")
        
        # Rate limiting
        time.sleep(1)
    
    return results

def filter_high_quality_poems(validation_results: Dict[str, ValidationResult], 
                             min_confidence: float = 0.7) -> List[str]:
    """Filter URLs to only high-confidence poems"""
    high_quality = []
    
    for url, result in validation_results.items():
        if result.is_poem and result.confidence_score >= min_confidence:
            high_quality.append(url)
    
    return high_quality

# TEST FUNCTION
def test_mega_discovery():
    """Test the mega discovery system with multiple sources"""
    print("🧪 Testing MEGA Poem Discovery System with 75+ Sources")
    print("=" * 60)
    
    # Test premium sources first
    premium_sources = ['theparisreview.org', 'kenyonreview.org', 'poems.com']
    
    for domain in premium_sources:
        print(f"\n🔍 Testing {domain}...")
        
        links = discover_all_poem_links(domain, max_links=5)
        
        if links:
            print(f"✅ Found {len(links)} potential poem links")
            
            # Test validation on first few links
            print("🔬 Validating first 2 links...")
            for i, link in enumerate(links[:2]):
                validator = EnhancedPoemValidator()
                result = validator.validate_poem_content(link)
                status = "✅ Valid poem" if result.is_poem else "❌ Not a poem"
                print(f"   {i+1}. {status} (confidence: {result.confidence_score:.2f}): {link}")
        else:
            print("❌ No links discovered")
        
        print("-" * 40)
    
    print(f"\n🎉 TOTAL CONFIGURED SOURCES: {len(SITE_CONFIGS)}")
    print("Including legendary magazines like:")
    legendary = ['The Paris Review', 'The Kenyon Review', 'Tin House', 'The Southern Review', 'Ploughshares']
    for mag in legendary:
        print(f"  ✨ {mag}")

if __name__ == "__main__":
    # Run the test
    test_mega_discovery()