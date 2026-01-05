#!/usr/bin/env python3
"""
Twitter formatter for poetry posts.
Creates clean, consistent tweet format with poem excerpt and link.
"""

from typing import Optional
from sources.base import Poem


class TwitterFormatter:
    """Format poems for Twitter"""

    MAX_TWEET_LENGTH = 280

    def format_tweet(self, poem: Poem, num_lines: int = 4) -> str:
        """
        Format poem as tweet.

        Format:
            [Title]
            by [Author]

            [First N lines]
            ...

            [URL]

            #Poetry
        """
        # Get first N lines
        lines = [line.strip() for line in poem.text.split('\n') if line.strip()]
        excerpt_lines = lines[:num_lines]

        # Build tweet components
        header = f"{poem.title}\nby {poem.author}\n"
        excerpt = '\n'.join(excerpt_lines)

        # Add ellipsis if there are more lines
        if len(lines) > num_lines:
            excerpt += '\n...'

        footer = f"\n\n{poem.source_url}\n\n#Poetry"

        # Construct full tweet
        tweet = f"{header}\n{excerpt}{footer}"

        # If too long, reduce number of lines
        while len(tweet) > self.MAX_TWEET_LENGTH and num_lines > 2:
            num_lines -= 1
            excerpt_lines = lines[:num_lines]
            excerpt = '\n'.join(excerpt_lines)
            if len(lines) > num_lines:
                excerpt += '\n...'
            tweet = f"{header}\n{excerpt}{footer}"

        # If still too long, truncate title
        if len(tweet) > self.MAX_TWEET_LENGTH:
            max_title_len = 40
            truncated_title = poem.title[:max_title_len] + '...' if len(poem.title) > max_title_len else poem.title
            header = f"{truncated_title}\nby {poem.author}\n"
            tweet = f"{header}\n{excerpt}{footer}"

        # Final check - if still too long, use minimal format
        if len(tweet) > self.MAX_TWEET_LENGTH:
            tweet = f"{poem.title}\nby {poem.author}\n\n{poem.source_url}\n\n#Poetry"

        return tweet

    def preview_tweet(self, poem: Poem) -> dict:
        """
        Generate tweet and return preview information.

        Returns:
            {
                'tweet': str,
                'length': int,
                'lines_used': int,
                'total_lines': int,
                'is_truncated': bool
            }
        """
        tweet = self.format_tweet(poem)
        total_lines = poem.line_count()

        # Count lines used in tweet
        lines_in_tweet = tweet.count('\n') - 5  # Subtract header/footer lines
        lines_used = max(2, min(lines_in_tweet, total_lines))

        return {
            'tweet': tweet,
            'length': len(tweet),
            'lines_used': lines_used,
            'total_lines': total_lines,
            'is_truncated': lines_used < total_lines
        }
