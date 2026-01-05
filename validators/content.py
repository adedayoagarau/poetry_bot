#!/usr/bin/env python3
"""
Strict content validation to ensure we only post actual poems.
Zero tolerance for false positives.
"""

from typing import Tuple
import re
from sources.base import Poem


class ContentValidator:
    """Validates that extracted content is actually a poem"""

    # Patterns that indicate NOT a poem
    BLOCKLIST_PATTERNS = [
        # Reviews and criticism
        r'\breview(ed|s)?\s+by\b',
        r'\bbook\s+review\b',
        r'\bcritique\b',
        r'\banalysis\s+of\b',

        # Interviews and features
        r'\binterview\s+with\b',
        r'\bconversation\s+with\b',
        r'\bprofile\s+of\b',
        r'\bin\s+conversation\b',

        # Obituaries and memorials
        r'\b\d{4}\s*[-–]\s*\d{4}\b',  # Birth-death years
        r'\bpassed\s+away\b',
        r'\bin\s+memoriam\b',
        r'\bobituary\b',

        # Table of contents / Issue pages
        r'\bno\.\s*\d+\b.*\d{4}',  # "No. 44 Winter 2025"
        r'\bissue\s+\d+\b',
        r'\btable\s+of\s+contents\b',
        r'\bcontributors?\b.*\bissue\b',

        # Submissions and announcements
        r'\bcall\s+for\s+submissions\b',
        r'\bsubmission\s+guidelines\b',
        r'\baccepting\s+submissions\b',
        r'\bdeadline\b.*\bsubmit\b',

        # About pages
        r'\babout\s+the\s+author\b',
        r'\babout\s+the\s+poet\b',
        r'\bbiography\b',
        r'\babout\s+us\b',

        # News and announcements
        r'\bpress\s+release\b',
        r'\bannouncement\b',
        r'\bwinners?\b.*\bcontest\b',
        r'\baward\s+winner\b',
    ]

    # Title patterns that indicate NOT a poem
    BAD_TITLE_PATTERNS = [
        r'\breview(ed|s)?\s+by\b',
        r'\bno\.\s*\d+\b',  # Issue numbers
        r'\b\d{4}\s*[-–]\s*\d{4}\b',  # Year ranges
        r'\bissue\b',
        r'\bwinter\s+\d{4}\b',
        r'\bspring\s+\d{4}\b',
        r'\bsummer\s+\d{4}\b',
        r'\bfall\s+\d{4}\b',
    ]

    def validate(self, poem: Poem) -> Tuple[bool, str]:
        """
        Validate that poem is actually a poem.

        Returns:
            (is_valid, reason)
        """

        # 1. Title validation
        is_valid, reason = self._validate_title(poem.title)
        if not is_valid:
            return False, f"Invalid title: {reason}"

        # 2. Author validation
        is_valid, reason = self._validate_author(poem.author)
        if not is_valid:
            return False, f"Invalid author: {reason}"

        # 3. Text structure validation
        is_valid, reason = self._validate_text_structure(poem.text)
        if not is_valid:
            return False, f"Invalid structure: {reason}"

        # 4. Content validation (check for blocklisted patterns)
        is_valid, reason = self._validate_content(poem.text, poem.title)
        if not is_valid:
            return False, f"Content check failed: {reason}"

        # 5. Word count validation
        word_count = poem.word_count()
        if word_count < 20:
            return False, f"Too short: {word_count} words"
        if word_count > 600:
            return False, f"Too long: {word_count} words (likely essay)"

        # 6. Line count validation
        line_count = poem.line_count()
        if line_count < 4:
            return False, f"Too few lines: {line_count}"
        if line_count > 100:
            return False, f"Too many lines: {line_count}"

        return True, "Poem validated successfully"

    def _validate_title(self, title: str) -> Tuple[bool, str]:
        """Validate title is not a red flag"""
        if not title or len(title) < 1:
            return False, "Empty title"

        # Check for bad patterns
        for pattern in self.BAD_TITLE_PATTERNS:
            if re.search(pattern, title, re.IGNORECASE):
                return False, f"Title contains blocklisted pattern: {pattern}"

        # Check for generic titles
        generic_titles = ['untitled', 'blog', 'home', 'archive', 'about']
        if title.lower().strip() in generic_titles:
            return False, f"Generic title: {title}"

        return True, "Title OK"

    def _validate_author(self, author: str) -> Tuple[bool, str]:
        """Validate author name"""
        if not author or len(author) < 2:
            return False, "Author too short"

        # Check for invalid authors
        invalid_authors = ['unknown', 'anonymous', 'poetry', 'poems']
        if author.lower().strip() in invalid_authors:
            return False, f"Invalid author: {author}"

        # Author shouldn't be ridiculously long
        if len(author) > 60:
            return False, "Author name too long"

        return True, "Author OK"

    def _validate_text_structure(self, text: str) -> Tuple[bool, str]:
        """Validate text has poem-like structure"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]

        # Check average line length (poems have shorter lines than prose)
        line_lengths = [len(line) for line in lines]
        avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0

        # If average line length is very long, it's likely prose
        if avg_line_length > 120:
            return False, f"Average line too long ({avg_line_length:.0f} chars) - likely prose"

        # Check for very long lines (prose paragraphs)
        very_long_lines = sum(1 for length in line_lengths if length > 200)
        if very_long_lines > len(lines) * 0.2:  # More than 20% very long lines
            return False, f"{very_long_lines} lines over 200 chars - likely prose"

        return True, "Structure OK"

    def _validate_content(self, text: str, title: str) -> Tuple[bool, str]:
        """Validate content doesn't match blocklisted patterns"""
        combined_text = f"{title}\n{text}".lower()

        # Check against blocklist
        for pattern in self.BLOCKLIST_PATTERNS:
            if re.search(pattern, combined_text, re.IGNORECASE):
                return False, f"Matches blocklist pattern: {pattern}"

        return True, "Content OK"

    def validate_with_details(self, poem: Poem) -> dict:
        """
        Validate and return detailed information.

        Returns:
            {
                'is_valid': bool,
                'reason': str,
                'word_count': int,
                'line_count': int,
                'avg_line_length': float
            }
        """
        is_valid, reason = self.validate(poem)

        lines = [line.strip() for line in poem.text.split('\n') if line.strip()]
        line_lengths = [len(line) for line in lines]
        avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0

        return {
            'is_valid': is_valid,
            'reason': reason,
            'word_count': poem.word_count(),
            'line_count': poem.line_count(),
            'avg_line_length': avg_line_length
        }
