#!/usr/bin/env python3
"""
Base class for poetry source extractors.
Each source has custom extraction logic for reliable quality.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import requests
from bs4 import BeautifulSoup


@dataclass
class Poem:
    """Structured poem data"""
    title: str
    author: str
    text: str  # Full poem text with line breaks preserved
    source_name: str
    source_url: str

    def __post_init__(self):
        """Validate required fields"""
        if not self.title or self.title == "Untitled":
            raise ValueError("Poem must have a valid title")
        if not self.author or self.author == "Unknown":
            raise ValueError("Poem must have a known author")
        if not self.text or len(self.text.strip()) < 20:
            raise ValueError("Poem text is too short or empty")

    def word_count(self) -> int:
        """Count words in poem"""
        return len(self.text.split())

    def line_count(self) -> int:
        """Count non-empty lines in poem"""
        lines = [line.strip() for line in self.text.split('\n') if line.strip()]
        return len(lines)


class PoetrySource(ABC):
    """Abstract base class for poetry sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; PoetryBot/2.0; +https://github.com/poetrybot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })

    @property
    @abstractmethod
    def name(self) -> str:
        """Source name (e.g., 'Poetry Daily')"""
        pass

    @property
    @abstractmethod
    def base_url(self) -> str:
        """Base URL for the source"""
        pass

    @abstractmethod
    def get_todays_poem_url(self) -> Optional[str]:
        """
        Get URL for today's poem.
        Returns None if unable to find.
        """
        pass

    @abstractmethod
    def extract_poem(self, url: str) -> Optional[Poem]:
        """
        Extract poem from a specific URL.
        Returns None if extraction fails.
        """
        pass

    def fetch_html(self, url: str, timeout: int = 15) -> Optional[BeautifulSoup]:
        """
        Fetch and parse HTML from URL.
        Returns None if request fails.
        """
        try:
            response = self.session.get(url, timeout=timeout)
            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code} for {url}")
                return None
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return None

    def get_daily_poem(self) -> Optional[Poem]:
        """
        Get today's poem (convenience method).
        Returns None if unable to get poem.
        """
        try:
            url = self.get_todays_poem_url()
            if not url:
                print(f"❌ Could not get today's poem URL from {self.name}")
                return None

            poem = self.extract_poem(url)
            if not poem:
                print(f"❌ Could not extract poem from {url}")
                return None

            return poem

        except Exception as e:
            print(f"❌ Error getting daily poem from {self.name}: {e}")
            return None
