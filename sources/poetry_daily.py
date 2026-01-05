#!/usr/bin/env python3
"""
Poetry Daily (poems.com) extractor.
Publishes one poem per day with high editorial standards.
"""

from typing import Optional
import re
from .base import PoetrySource, Poem


class PoetryDailySource(PoetrySource):
    """Extract poems from Poetry Daily (poems.com)"""

    @property
    def name(self) -> str:
        return "Poetry Daily"

    @property
    def base_url(self) -> str:
        return "https://poems.com"

    def get_todays_poem_url(self) -> Optional[str]:
        """
        Poetry Daily always has today's poem at the homepage.
        """
        return self.base_url + "/"

    def extract_poem(self, url: str) -> Optional[Poem]:
        """
        Extract poem from Poetry Daily.

        Verified structure as of Jan 2026:
        - Title: <title> tag contains "POEM_TITLE – Poetry Daily"
        - Author: .daily_poem_author class
        - Poem text: .elementor-widget-theme-post-content
        """
        soup = self.fetch_html(url)
        if not soup:
            return None

        try:
            # Extract title from page title
            title = self._extract_title(soup)
            if not title:
                print(f"❌ Could not extract title from {url}")
                return None

            # Extract author
            author = self._extract_author(soup)
            if not author:
                print(f"❌ Could not extract author from {url}")
                return None

            # Extract poem text
            poem_text = self._extract_poem_text(soup)
            if not poem_text:
                print(f"❌ Could not extract poem text from {url}")
                return None

            # Create poem object (validation happens in __post_init__)
            poem = Poem(
                title=title,
                author=author,
                text=poem_text,
                source_name=self.name,
                source_url=url
            )

            print(f"✅ Extracted: '{poem.title}' by {poem.author} ({poem.line_count()} lines)")
            return poem

        except Exception as e:
            print(f"❌ Extraction failed for {url}: {e}")
            return None

    def _extract_title(self, soup) -> Optional[str]:
        """Extract title from page title tag"""
        title_elem = soup.find('title')
        if not title_elem:
            return None

        # Format: "POEM_TITLE – Poetry Daily"
        page_title = title_elem.get_text().strip()

        # Remove " – Poetry Daily" suffix
        if ' – Poetry Daily' in page_title:
            title = page_title.replace(' – Poetry Daily', '').strip()
        else:
            title = page_title.strip()

        # Remove quotes if present
        title = title.strip('"').strip("'").strip()

        # Validate title
        if not title or len(title) < 1:
            return None

        # Check for red flags (not a poem page)
        red_flags = ['home', 'archive', 'about', 'contact', 'poetry daily']
        if title.lower() in red_flags:
            return None

        return title

    def _extract_author(self, soup) -> Optional[str]:
        """Extract author name"""
        # Primary selector
        author_elem = soup.select_one('.daily_poem_author')
        if not author_elem:
            # Fallback selectors
            author_elem = soup.select_one('.author')
            if not author_elem:
                author_elem = soup.select_one('[class*="author"]')

        if not author_elem:
            return None

        author = author_elem.get_text().strip()

        # Clean up author name
        author = re.sub(r'^(by\s+)', '', author, flags=re.IGNORECASE)
        author = re.sub(r'\s+', ' ', author)
        author = author.strip()

        # Validate author
        if not author or len(author) < 2:
            return None

        # Check for red flags
        red_flags = ['unknown', 'anonymous', 'poetry', 'poems', 'instagram', 'facebook', 'twitter']
        if author.lower() in red_flags:
            return None

        return author

    def _extract_poem_text(self, soup) -> Optional[str]:
        """Extract clean poem text"""
        # Primary selector for Poetry Daily
        poem_elem = soup.select_one('.elementor-widget-theme-post-content')

        if not poem_elem:
            # Fallback selectors
            poem_elem = soup.select_one('.poem-content')
            if not poem_elem:
                poem_elem = soup.select_one('[class*="poem"]')

        if not poem_elem:
            return None

        # Get text with line breaks preserved
        poem_text = poem_elem.get_text(separator='\n').strip()

        # Split into lines
        lines = poem_text.split('\n')

        # Clean each line and filter
        clean_lines = []
        for line in lines:
            line = line.strip()

            # Skip empty lines (we'll preserve intentional stanza breaks later)
            if not line:
                continue

            # Skip navigation/metadata patterns
            skip_patterns = [
                r'^(home|about|contact|subscribe|archive|browse)$',
                r'www\.',
                r'http',
                r'\.com',
                r'\.org',
                r'published',
                r'copyright',
                r'all rights reserved',
                r'read more',
                r'continue reading',
                r'\d{4}©',  # Copyright years
            ]

            should_skip = False
            for pattern in skip_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_skip = True
                    break

            if should_skip:
                continue

            # Skip very short lines (likely metadata)
            if len(line) <= 2:
                continue

            clean_lines.append(line)

        # Rejoin with single line breaks
        poem_text = '\n'.join(clean_lines)

        # Basic validation
        if len(poem_text) < 20:
            return None

        return poem_text
