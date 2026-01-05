#!/usr/bin/env python3
"""
Track posted poems to avoid duplicates.
"""

import json
import os
from datetime import datetime
from typing import Set, List, Dict, Optional
from sources.base import Poem


class PostedTracker:
    """Track which poems have been posted"""

    def __init__(self, storage_file: str = 'data/posted_poems.json'):
        self.storage_file = storage_file
        self.posted_urls: Set[str] = set()
        self.posted_history: List[Dict] = []
        self._load()

    def _load(self):
        """Load posted poems from file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)

            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.posted_urls = set(data.get('posted_urls', []))
                    self.posted_history = data.get('history', [])
                print(f"📚 Loaded {len(self.posted_urls)} posted poems")
            else:
                print("📚 No existing posted poems file, starting fresh")

        except Exception as e:
            print(f"⚠️  Error loading posted poems: {e}")
            self.posted_urls = set()
            self.posted_history = []

    def _save(self):
        """Save posted poems to file"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)

            data = {
                'posted_urls': list(self.posted_urls),
                'history': self.posted_history[-500:]  # Keep last 500 entries
            }

            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"⚠️  Error saving posted poems: {e}")

    def has_posted(self, poem: Poem) -> bool:
        """Check if poem has been posted before"""
        return poem.source_url in self.posted_urls

    def mark_posted(self, poem: Poem, tweet_url: Optional[str] = None):
        """Mark poem as posted"""
        self.posted_urls.add(poem.source_url)

        # Add to history
        entry = {
            'url': poem.source_url,
            'title': poem.title,
            'author': poem.author,
            'source': poem.source_name,
            'posted_at': datetime.now().isoformat(),
            'word_count': poem.word_count(),
            'line_count': poem.line_count()
        }

        if tweet_url:
            entry['tweet_url'] = tweet_url

        self.posted_history.append(entry)

        # Save to disk
        self._save()

        print(f"💾 Marked as posted: '{poem.title}' by {poem.author}")

    def get_recent_posts(self, count: int = 10) -> List[Dict]:
        """Get recent posted poems"""
        return self.posted_history[-count:]

    def get_stats(self) -> Dict:
        """Get posting statistics"""
        return {
            'total_posted': len(self.posted_urls),
            'history_entries': len(self.posted_history),
            'sources': {}
        }
