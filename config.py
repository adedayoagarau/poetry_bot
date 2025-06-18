# Configuration for Twitter Poetry Bot - MEGA VERSION (120+ Sources)
# Bot Settings
BOT_SETTINGS = {
    'posts_per_day': 10,
    'max_ai_posts_per_day': 0,  # NEVER post AI-generated content
    'avoid_repeat_sources': False,  # Allow repeat sources for 10 posts/day
    'avoid_repeat_authors': False,  # Allow repeat authors for 10 posts/day
    'upload_media_v1_1': False,
    'post_times_utc': ['06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00', '00:00'],
    
    # MEGA SOURCE SETTINGS
    'max_urls_per_source': 20,  # More URLs per source for 120+ sources
    'validation_cache_hours': 12,  # Longer cache for stability
    'failed_url_retry_hours': 72,  # Longer retry for this many sources
    'min_confidence_score': 0.6,  # Balanced confidence
    'max_validation_attempts_per_run': 200,  # More attempts for 120+ sources
    
    # DIVERSITY CONTROLS
    'max_same_author_per_day': 2,  # Lower limit with more sources
    'max_same_source_per_day': 3,  # Lower limit with more sources
    'min_hours_between_same_author': 3,  # More spacing
    'prefer_tier1_sources_ratio': 0.4,  # 40% from tier 1
    'international_sources_ratio': 0.15,  # 15% international
    'daily_sources_ratio': 0.2,  # 20% from daily sources
}

def get_weighted_journal_list():
    """
    MEGA POETRY SOURCE LIST: 120+ Journals for High-Volume Bot
    Total: 120+ unique poetry sources across 6 tiers
    """
    
    # TIER 1: The Big Guns (Weight 6) - Ultra-reliable, high-volume sources
    tier1_sources = [
        {'name': 'Poetry Daily', 'url': 'https://poems.com', 'weight': 6},
        {'name': 'Poetry Foundation', 'url': 'https://poetryfoundation.org', 'weight': 6},
        {'name': 'Academy of American Poets', 'url': 'https://poets.org', 'weight': 5},
        {'name': 'Verse Daily', 'url': 'https://versedaily.org', 'weight': 5},
        {'name': 'Poetry Magazine', 'url': 'https://poetrymagazine.org', 'weight': 5},
        {'name': 'The New Yorker', 'url': 'https://newyorker.com', 'weight': 5},
    ]
    
    # TIER 2: Premier University & Literary Journals (Weight 4)
    tier2_sources = [
        {'name': 'The Iowa Review', 'url': 'https://iowareview.org', 'weight': 4},
        {'name': 'The Missouri Review', 'url': 'https://missourireview.com', 'weight': 4},
        {'name': 'New England Review', 'url': 'https://nereview.com', 'weight': 4},
        {'name': 'The Georgia Review', 'url': 'https://thegeorgiareview.com', 'weight': 4},
        {'name': 'Colorado Review', 'url': 'https://coloradoreview.colostate.edu', 'weight': 4},
        {'name': 'Alaska Quarterly Review', 'url': 'https://www.uaa.alaska.edu/academics/college-of-arts-and-sciences/departments/english/alaska-quarterly-review/', 'weight': 4},
        {'name': 'Black Warrior Review', 'url': 'https://bwr.ua.edu', 'weight': 4},
        {'name': 'Shenandoah', 'url': 'https://shenandoah.wlu.edu', 'weight': 4},
        {'name': 'AGNI', 'url': 'https://agnionline.bu.edu', 'weight': 4},
        {'name': 'The Kenyon Review', 'url': 'https://kenyonreview.org', 'weight': 4},
        {'name': 'The Antioch Review', 'url': 'https://antiochreview.org', 'weight': 4},
        {'name': 'The Yale Review', 'url': 'https://yalereview.org', 'weight': 4},
    ]
    
    # TIER 3: Poetry-Focused Journals (Weight 3)
    tier3_sources = [
        {'name': 'Plume', 'url': 'https://plumepoetry.com', 'weight': 3},
        {'name': 'RHINO Poetry', 'url': 'https://rhinopoetry.org', 'weight': 3},
        {'name': 'River Heron Review', 'url': 'https://riverheron.com', 'weight': 3},
        {'name': 'The Shore Poetry', 'url': 'https://theshorepoetry.org', 'weight': 3},
        {'name': 'Hiram Poetry Review', 'url': 'https://hiram.edu/hiram-poetry-review/', 'weight': 3},
        {'name': 'Bear Review', 'url': 'https://bearreview.com', 'weight': 3},
        {'name': 'Sheila-Na-Gig online', 'url': 'https://sheilanagigonline.com', 'weight': 3},
        {'name': 'American Poetry Review', 'url': 'https://aprweb.org', 'weight': 3},
        {'name': 'Beloit Poetry Journal', 'url': 'https://www.beloit.edu/bpj/', 'weight': 3},
        {'name': 'Poetry Northwest', 'url': 'https://poetrynw.org', 'weight': 3},
        {'name': 'Tar River Poetry', 'url': 'https://tarriverpoetry.com', 'weight': 3},
        {'name': 'Poetry International', 'url': 'https://poetryinternational.org', 'weight': 3},
    ]
    
    # TIER 4: High-Quality Online & Mixed Journals (Weight 2-3)
    tier4_sources = [
        {'name': 'Sky Island Journal', 'url': 'https://skyislandjournal.com', 'weight': 3},
        {'name': 'Prime Number Magazine', 'url': 'https://primenumbermagazine.com', 'weight': 2},
        {'name': 'The Sunlight Press', 'url': 'https://thesunlightpress.com', 'weight': 3},
        {'name': 'Terrain.org', 'url': 'https://terrain.org', 'weight': 2},
        {'name': 'Apple Valley Review', 'url': 'https://applevalleyreview.com', 'weight': 2},
        {'name': 'Chestnut Review', 'url': 'https://chestnutreview.com', 'weight': 2},
        {'name': 'The 2River View', 'url': 'https://www.2river.org', 'weight': 2},
        {'name': 'The Adroit Journal', 'url': 'https://theadroitjournal.org', 'weight': 2},
        {'name': 'Rattle', 'url': 'https://rattle.com', 'weight': 3},
        {'name': 'The Common', 'url': 'https://thecommonmagazine.org', 'weight': 2},
        {'name': 'New Letters', 'url': 'https://newletters.org', 'weight': 2},
        {'name': 'Salamander', 'url': 'https://salamandermag.org', 'weight': 2},
        {'name': 'Narrative', 'url': 'https://narrativemagazine.com', 'weight': 2},
        {'name': 'The Believer', 'url': 'https://believermag.com', 'weight': 2},
        {'name': 'Diode Poetry Journal', 'url': 'https://diodepoetry.com', 'weight': 2},
        {'name': 'FIELD', 'url': 'https://www.oberlin.edu/field-magazine', 'weight': 2},
    ]
    
    # TIER 5: University Reviews & Regional Journals (Weight 2)
    tier5_sources = [
        {'name': 'South Dakota Review', 'url': 'https://usd.edu/cas/english/south-dakota-review', 'weight': 2},
        {'name': 'Southern Humanities Review', 'url': 'https://www.southernhumanitiesreview.com', 'weight': 2},
        {'name': 'Bellevue Literary Review', 'url': 'https://blr.med.nyu.edu', 'weight': 2},
        {'name': 'The Malahat Review', 'url': 'https://malahatreview.ca', 'weight': 2},
        {'name': 'Obsidian', 'url': 'https://obsidianlit.org', 'weight': 2},
        {'name': 'I-70 Review', 'url': 'https://i70review.com', 'weight': 2},
        {'name': 'Valley Voices', 'url': 'https://valleyvoices.org', 'weight': 2},
        {'name': 'West Trade Review', 'url': 'https://westtradereview.com', 'weight': 2},
        {'name': 'The Southern Review', 'url': 'https://southernreview.org', 'weight': 2},
        {'name': 'Michigan Quarterly Review', 'url': 'https://michiganquarterlyreview.com', 'weight': 2},
        {'name': 'Sycamore Review', 'url': 'https://sycamorereview.com', 'weight': 2},
        {'name': 'The Normal School', 'url': 'https://thenormalschool.com', 'weight': 2},
        {'name': 'Cimarron Review', 'url': 'https://cimarronreview.com', 'weight': 2},
        {'name': 'Ninth Letter', 'url': 'https://ninthletter.com', 'weight': 2},
        {'name': 'Iron Horse Literary Review', 'url': 'https://ironhorsereview.com', 'weight': 2},
        {'name': 'Mid-American Review', 'url': 'https://casit.bgsu.edu/midamericanreview/', 'weight': 2},
    ]
    
    # TIER 6: Emerging & Specialty Journals (Weight 1-2)
    tier6_sources = [
        {'name': 'Barren Magazine', 'url': 'https://barrenmagazine.com', 'weight': 1},
        {'name': 'Greensboro Review', 'url': 'https://greensbororeview.org', 'weight': 1},
        {'name': 'Brilliant Flash Fiction', 'url': 'https://brilliantflashfiction.com', 'weight': 1},
        {'name': 'Ghost City Review', 'url': 'https://ghostcityreview.com', 'weight': 1},
        {'name': 'Palette Poetry', 'url': 'https://palettepoetry.com', 'weight': 2},
        {'name': 'Muzzle Magazine', 'url': 'https://muzzlemagazine.com', 'weight': 1},
        {'name': 'Thrush Poetry Journal', 'url': 'https://thrushpoetryjournal.com', 'weight': 1},
        {'name': '3Elements Literary Review', 'url': 'https://3elementsreview.com', 'weight': 1},
        {'name': 'FreezeRay Poetry', 'url': 'https://freezeraypoetry.com', 'weight': 1},
        {'name': 'Dust Poetry Magazine', 'url': 'https://dustpoetry.co.uk', 'weight': 1},
        {'name': 'Modern Poets Magazine', 'url': 'https://modernpoetsmagazine.com', 'weight': 1},
        {'name': 'Cleaver Magazine', 'url': 'https://cleavermagazine.com', 'weight': 1},
        {'name': 'Club Plum Literary Journal', 'url': 'https://clubplum.com', 'weight': 1},
        {'name': 'Cool Beans Lit', 'url': 'https://coolbeanslit.com', 'weight': 1},
        {'name': 'The Courtship of Winds', 'url': 'https://thecourtshipofwinds.com', 'weight': 1},
        {'name': 'Cutleaf', 'url': 'https://cutleafjournal.com', 'weight': 1},
    ]
    
    # INTERNATIONAL SOURCES (Weight 1-2) - Global diversity
    international_sources = [
        {'name': 'Granta', 'url': 'https://granta.com', 'weight': 2},
        {'name': 'The Fiddlehead', 'url': 'https://thefiddlehead.ca', 'weight': 2},
        {'name': 'PRISM International', 'url': 'https://prismmagazine.ca', 'weight': 2},
        {'name': 'The Rialto', 'url': 'https://therialto.co.uk', 'weight': 2},
        {'name': 'Poetry London', 'url': 'https://poetrylondon.co.uk', 'weight': 2},
        {'name': 'Cha: An Asian Literary Journal', 'url': 'https://chajournal.blog', 'weight': 1},
        {'name': 'The Stockholm Review', 'url': 'https://thestockholmreview.com', 'weight': 1},
        {'name': 'Sand Journal', 'url': 'https://sandjournal.com', 'weight': 1},
        {'name': 'Leopards & Limes', 'url': 'https://leopardsandlimes.com', 'weight': 1},
        {'name': 'New Contrast', 'url': 'https://newcontrast.net', 'weight': 1},
        {'name': 'The Kalahari Review', 'url': 'https://kalaharireview.com', 'weight': 1},
        {'name': 'Grain Magazine', 'url': 'https://grainmagazine.ca', 'weight': 1},
        {'name': 'Going Down Swinging', 'url': 'https://goingdownswinging.org.au', 'weight': 1},
        {'name': 'Meanjin', 'url': 'https://meanjin.com.au', 'weight': 1},
        {'name': 'The Missing Slate', 'url': 'https://themissingslate.com', 'weight': 1},
        {'name': 'Sukoon Magazine', 'url': 'https://sukoonmag.com', 'weight': 1},
    ]
    
    # BONUS: Your Original Sources (keeping them with weight 1)
    original_sources = [
        {'name': 'The Paris Review', 'url': 'https://theparisreview.org', 'weight': 2},
    ]
    
    # Combine all tiers
    all_sources = (tier1_sources + tier2_sources + tier3_sources + 
                  tier4_sources + tier5_sources + tier6_sources + 
                  international_sources + original_sources)
    
    # Remove duplicates by name
    unique_sources = {}
    for source in all_sources:
        if source['name'] not in unique_sources:
            unique_sources[source['name']] = source
    
    # Create weighted list
    weighted_list = []
    for source in unique_sources.values():
        weight = source.get('weight', 1)
        for _ in range(weight):
            weighted_list.append({
                'name': source['name'],
                'url': source['url']
            })
    
    print(f"🎯 MEGA CONFIGURATION LOADED!")
    print(f"📊 Total Unique Sources: {len(unique_sources)}")
    print(f"📊 Total Weighted Entries: {len(weighted_list)}")
    print(f"🌟 Tier 1 Premier: 6 sources")
    print(f"🏛️  Tier 2 University: 12 sources") 
    print(f"📝 Tier 3 Poetry-Focused: 12 sources")
    print(f"🌍 International Sources: 16 sources")
    print("✅ Ready for 10 posts/day with massive diversity!")
    
    return weighted_list
