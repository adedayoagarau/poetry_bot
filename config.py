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
    },
    
    # Additional sources from NewPages Big List
    {
        'name': 'A Public Space',
        'url': 'https://apublicspace.org/',
        'selector': 'div.poem, .entry-content, article',
        'has_online_poems': True
    },
    {
        'name': 'Able Muse',
        'url': 'https://www.ablemuse.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'About Place Journal',
        'url': 'https://aboutplacejournal.org/',
        'selector': 'div.poem, .entry-content, article',
        'has_online_poems': True
    },
    {
        'name': 'The Account',
        'url': 'https://theaccountmagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Acumen',
        'url': 'https://www.acumen-poetry.co.uk/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'After Happy Hour',
        'url': 'https://afterhappyhourreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Air/Light',
        'url': 'https://airlightmagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Alaska Quarterly Review',
        'url': 'https://www.uaa.alaska.edu/academics/college-of-arts-and-sciences/departments/english/alaska-quarterly-review/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Allegheny Review',
        'url': 'https://sites.allegheny.edu/alleghenyreview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Allegro Poetry Magazine',
        'url': 'https://allegropoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The American Poetry Review',
        'url': 'https://aprweb.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Amsterdam Review',
        'url': 'https://amsterdamreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Antioch Review',
        'url': 'https://antiochreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Appalachian Review',
        'url': 'https://appalachianreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Arc Poetry Magazine',
        'url': 'https://arcpoetry.ca/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Ariel Chart',
        'url': 'https://arielchart.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Arkansas Review',
        'url': 'https://arkansasreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Artemis Journal',
        'url': 'https://artemisjournal.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Arts & Letters',
        'url': 'https://artsandletters.gcsu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Asheville Poetry Review',
        'url': 'https://www.ashevillereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Atlanta Review',
        'url': 'https://atlantareview.com/',
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
        'name': 'Autumn House Review',
        'url': 'https://autumnhouse.org/',
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
        'name': 'Bellevue Literary Review',
        'url': 'https://blr.med.nyu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Beloit Poetry Journal',
        'url': 'https://www.bpj.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Birmingham Poetry Review',
        'url': 'https://www.uab.edu/cas/englishpublications/birmingham-poetry-review',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Blackbird',
        'url': 'https://blackbird.vcu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Blue Fifth Review',
        'url': 'https://www.bluefifthreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Blueline',
        'url': 'https://blueline.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Booth',
        'url': 'https://booth.butler.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Borderlands',
        'url': 'https://www.borderlandsjournal.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Boston Review',
        'url': 'https://www.bostonreview.net/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Brevity',
        'url': 'https://brevitymag.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Brick',
        'url': 'https://brickmag.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Brilliant Corners',
        'url': 'https://brilliantcorners.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Broadsided',
        'url': 'https://broadsidedpress.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Callaloo',
        'url': 'https://callaloo.tamu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Calyx',
        'url': 'https://calyxpress.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'The Capilano Review',
        'url': 'https://www.thecapilanoreview.ca/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Carolina Quarterly',
        'url': 'https://carolinaquarterly.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Catamaran',
        'url': 'https://catamaranliteraryreader.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cave Wall',
        'url': 'https://cavewallpress.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Chariton Review',
        'url': 'https://www.charitonreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Chattahoochee Review',
        'url': 'https://thechattahoocheereview.gpc.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Chicago Review',
        'url': 'https://chicagoreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cimarron Review',
        'url': 'https://cimarronreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cincinnati Review',
        'url': 'https://www.cincinnatimagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cold Mountain Review',
        'url': 'https://coldmountainreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Commonweal',
        'url': 'https://www.commonwealmagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Connotation Press',
        'url': 'https://www.connotationpress.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Contemporary Verse 2',
        'url': 'https://cv2.ca/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Copper Nickel',
        'url': 'https://copper-nickel.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Crab Orchard Review',
        'url': 'https://craborchardreview.siu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Crazyhorse',
        'url': 'https://crazyhorse.cofc.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cream City Review',
        'url': 'https://uwm.edu/creamcityreview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Cutbank',
        'url': 'https://cutbankonline.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Denver Quarterly',
        'url': 'https://www.du.edu/denverquarterly/',
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
        'name': 'Ecotone',
        'url': 'https://ecotonemagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Epoch',
        'url': 'https://epoch.cornell.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Event',
        'url': 'https://www.eventmagazine.ca/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Field',
        'url': 'https://www.oberlin.edu/field-magazine',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Fifth Wednesday',
        'url': 'https://www.fifthwednesdayjournal.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Flyway',
        'url': 'https://flyway.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Folio',
        'url': 'https://www.american.edu/cas/literature/folio/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Fourteen Hills',
        'url': 'https://fourteenhillspress.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Fugue',
        'url': 'https://www.fuguejournal.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Gargoyle',
        'url': 'https://www.gargoylemagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Gettysburg Review',
        'url': 'https://www.gettysburgreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Green Mountains Review',
        'url': 'https://greenmountainsreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Greensboro Review',
        'url': 'https://greensbororeview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Gulf Coast',
        'url': 'https://gulfcoastmag.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Harvard Review',
        'url': 'https://harvardreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Haydens Ferry Review',
        'url': 'https://haydensferryreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Hotel Amerika',
        'url': 'https://hotelamerika.net/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Hudson Review',
        'url': 'https://hudsonreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Image',
        'url': 'https://imagejournal.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Indiana Review',
        'url': 'https://indianareview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Iron Horse Literary Review',
        'url': 'https://www.ironhorsereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Jabberwock Review',
        'url': 'https://jabberwockreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Journal',
        'url': 'https://thejournalmag.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Kalliope',
        'url': 'https://kalliope.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Lake Effect',
        'url': 'https://lakeeffect.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Literary Mama',
        'url': 'https://literarymama.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Louisville Review',
        'url': 'https://louisvillereview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Malahat Review',
        'url': 'https://malahatreview.ca/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Manoa',
        'url': 'https://manoa.hawaii.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Massachusetts Review',
        'url': 'https://www.massreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Meridian',
        'url': 'https://meridian.virginia.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Michigan Quarterly Review',
        'url': 'https://www.michiganquarterlyreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Mid-American Review',
        'url': 'https://casit.bgsu.edu/midamericanreview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Midwest Quarterly',
        'url': 'https://www.pittstate.edu/college/arts-and-sciences/english-and-modern-languages/midwest-quarterly/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Minnesota Review',
        'url': 'https://theminnesotareview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Mississippi Review',
        'url': 'https://mississippireview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'New Letters',
        'url': 'https://newletters.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'New Ohio Review',
        'url': 'https://www.ohio.edu/nor/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'New Orleans Review',
        'url': 'https://neworleansreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Nimrod',
        'url': 'https://nimrod.utulsa.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Ninth Letter',
        'url': 'https://ninthletter.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'North American Review',
        'url': 'https://northamericanreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'North Carolina Literary Review',
        'url': 'https://nclr.ecu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'North Dakota Quarterly',
        'url': 'https://ndquarterly.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Northwest Review',
        'url': 'https://nwr.uoregon.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Notre Dame Review',
        'url': 'https://ndreview.nd.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Obsidian',
        'url': 'https://obsidianlit.wordpress.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Ocean State Review',
        'url': 'https://oceanstatereview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Ohio Review',
        'url': 'https://www.ohioreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Orion',
        'url': 'https://orionmagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Packingtown Review',
        'url': 'https://packingtownreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Painted Bride Quarterly',
        'url': 'https://paintedbrideartscenter.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Paterson Literary Review',
        'url': 'https://www.pccc.edu/poetry/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Pembroke Magazine',
        'url': 'https://pembrokemagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Permafrost',
        'url': 'https://permafrostmag.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Phoebe',
        'url': 'https://phoebe.gmu.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Poet Lore',
        'url': 'https://poetlore.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Poetry East',
        'url': 'https://poetryeast.org/',
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
        'name': 'Poetry South',
        'url': 'https://poetrysouth.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Potomac Review',
        'url': 'https://potomacreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Quarterly West',
        'url': 'https://quarterlywest.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Raritan',
        'url': 'https://raritan.rutgers.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Red Rock Review',
        'url': 'https://sites.google.com/site/redrockreview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'River Styx',
        'url': 'https://riverstyx.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Room',
        'url': 'https://roommagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Salamander',
        'url': 'https://salamandermag.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Salt Hill',
        'url': 'https://salthilljournal.net/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Seneca Review',
        'url': 'https://www.hws.edu/senecareview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Shenandoah',
        'url': 'https://shenandoahliterary.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Slipstream',
        'url': 'https://slipstreampress.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'So to Speak',
        'url': 'https://sotospeakjournal.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'South Carolina Review',
        'url': 'https://southcarolinareview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'South Dakota Review',
        'url': 'https://southdakotareview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Southeast Review',
        'url': 'https://southeastreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Southern Humanities Review',
        'url': 'https://www.southernhumanitiesreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Southern Poetry Review',
        'url': 'https://southernpoetryreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Southwest Review',
        'url': 'https://www.smu.edu/southwestreview',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Spillway',
        'url': 'https://spillway.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Spoon River Poetry Review',
        'url': 'https://spoonriverpoetry.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Subtropics',
        'url': 'https://subtropics.english.ufl.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Sun',
        'url': 'https://thesunmagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Sycamore Review',
        'url': 'https://sycamorereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Tampa Review',
        'url': 'https://tampareview.ut.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Tar River Poetry',
        'url': 'https://tarriverpoetry.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Texas Review',
        'url': 'https://texasreview.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Third Coast',
        'url': 'https://thirdcoastmagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Threepenny Review',
        'url': 'https://threepennyreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Tulane Review',
        'url': 'https://tulanereview.tulane.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Tusculum Review',
        'url': 'https://www.tusculum.edu/academics/tusculum-review/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Valparaiso Poetry Review',
        'url': 'https://www.valpo.edu/vpr/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Virginia Quarterly Review',
        'url': 'https://www.vqronline.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Washington Square Review',
        'url': 'https://www.washingtonsquarereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Water~Stone Review',
        'url': 'https://waterstonereview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Weber',
        'url': 'https://weber.edu/weberreview/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'West Branch',
        'url': 'https://westbranch.blogs.bucknell.edu/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Western Humanities Review',
        'url': 'https://westernhumanitiesreview.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Whiskey Island',
        'url': 'https://whiskeyislandmagazine.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Willow Springs',
        'url': 'https://willowspringsmagazine.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Witness',
        'url': 'https://witness.blackmountaininstitute.org/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'Yale Review',
        'url': 'https://yalereview.yale.edu/',
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
        'name': 'Zone 3',
        'url': 'https://zone3press.com/',
        'selector': 'div.poem, .entry-content',
        'has_online_poems': True
    },
    {
        'name': 'ZYZZYVA',
        'url': 'https://www.zyzzyva.org/',
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