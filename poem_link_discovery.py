#!/usr/bin/env python3
"""
Enhanced Poem Link Discovery and Validation System
Improved accuracy for detecting actual poems vs other content
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

# Example usage and testing
if __name__ == "__main__":
    # Test URLs (replace with your actual discovered URLs)
    test_urls = [
        "https://poems.com/poem/the-road-not-taken/",
        "https://www.poetryfoundation.org/poems/44272/the-road-not-taken",
        "https://poems.com/about/",  # This should be filtered out
    ]
    
    print("🧪 Testing Enhanced Poem Validation")
    print("=" * 50)
    
    # Validate URLs
    results = batch_validate_urls(test_urls)
    
    # Filter high-quality poems
    high_quality_poems = filter_high_quality_poems(results, min_confidence=0.7)
    
    print(f"\n📊 Results Summary:")
    print(f"Total URLs tested: {len(test_urls)}")
    print(f"Valid poems found: {len([r for r in results.values() if r.is_poem])}")
    print(f"High-confidence poems: {len(high_quality_poems)}")
    
    print(f"\n✅ High-Quality Poem URLs:")
    for url in high_quality_poems:
        print(f"  {url}")
