"""
SmartNotes - Final Clean Processor
The definitive version with all issues resolved.

Author: Madhuri
Date: January 26, 2026
"""

import re
from typing import List, Dict
from collections import Counter
import os


class NoteProcessor:
    """Simple, reliable note processor."""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
            'when', 'where', 'why', 'how', 'all', 'each', 'both', 'some', 'such',
            'said', 'came', 'just', 'also', 'once', 'class', 'summary', 'powered',
            'first', 'last', 'given', 'common', 'general', 'different', 'most',
            'upon', 'time', 'book', 'english', 'chapter', 'page'
        }
        
        self.pronouns = {'he', 'she', 'it', 'we', 'you', 'i', 'they', 'them', 'him', 'her', 'us', 'our'}
    
    def extract_concepts(self, text: str, top_n: int = 10) -> List[str]:
        """Extract key concepts from text."""
        concepts = []
        
        # Method 1: Multi-word capitalized phrases (stop at punctuation!)
        # Only match within sentence boundaries
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            # Match 2-5 capitalized words in a row
            matches = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})\b', sentence)
            
            for phrase in matches:
                phrase = phrase.strip()
                words = phrase.split()
                
                # Skip if starts with article/conjunction
                if words[0] in ['The', 'But', 'And', 'Or', 'A', 'An']:
                    continue
                
                # Skip if contains generic words
                phrase_lower = phrase.lower()
                if any(generic in phrase_lower for generic in ['summary', 'class', 'chapter', 'book']):
                    continue
                
                concepts.append((phrase, 10.0))
        
        # Method 2: Important single words
        single_words = re.findall(r'\b[A-Z][a-z]{3,}\b', text)
        word_freq = Counter(single_words)
        
        for word, freq in word_freq.items():
            word_lower = word.lower()
            
            # Skip common words and pronouns
            if word in ['The', 'This', 'That', 'These', 'Those', 'Some', 'There']:
                continue
            if word_lower in self.pronouns or word_lower in self.stop_words:
                continue
            
            concepts.append((word, freq * 2.0))
        
        # Method 3: Frequent meaningful words (for technical notes)
        words = re.findall(r'\b[a-z]{5,}\b', text.lower())
        words = [w for w in words if w not in self.stop_words]
        word_freq = Counter(words)
        
        # Only add if appears multiple times
        for word, freq in word_freq.items():
            if freq >= 3:  # Must appear at least 3 times
                concepts.append((word.capitalize(), freq * 0.8))
        
        # Deduplicate and rank
        concept_dict = {}
        for concept, score in concepts:
            key = concept.lower().strip()
            if len(key) >= 3:
                if key not in concept_dict or score > concept_dict[key][1]:
                    concept_dict[key] = (concept, score)
        
        # Sort and return
        ranked = sorted(concept_dict.values(), key=lambda x: x[1], reverse=True)
        return [concept for concept, score in ranked[:top_n]]
    
    def extract_definitions(self, text: str) -> List[Dict[str, str]]:
        """Extract definitions using proven patterns."""
        definitions = []
        
        # Invalid terms
        invalid = {
            'he', 'she', 'it', 'they', 'we', 'you', 'i', 'this', 'that',
            'what', 'which', 'who', 'when', 'where', 'most', 'some', 'all',
            'these', 'those', 'them', 'him', 'her', 'us', 'our'
        }
        
        def is_valid_term(term: str) -> bool:
            """Check if term is valid."""
            term_lower = term.strip().lower()
            
            # Too short
            if len(term_lower) < 3:
                return False
            
            # Invalid words
            if term_lower in invalid:
                return False
            
            # Contains pronouns
            words = term_lower.split()
            if any(w in invalid for w in words):
                return False
            
            # Starts with article
            if term_lower.startswith(('the ', 'a ', 'an ', 'most ', 'some ')):
                return False
            
            # Single word must be capitalized
            if len(words) == 1 and not term[0].isupper():
                return False
            
            return True
        
        # Pattern 1: "X is/means/refers to Y"
        pattern1 = r'([A-Z][a-z]+(?:\s+[a-z]+)?)\s+(?:is|means|refers to|is defined as)\s+([^.!?]+)'
        for term, definition in re.findall(pattern1, text):
            if is_valid_term(term) and len(definition.strip()) > 5:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        
        # Pattern 2: "X: definition"
        pattern2 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]{15,})'
        for term, definition in re.findall(pattern2, text):
            if is_valid_term(term):
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        
        # Pattern 3: "X is/are Y"
        pattern3 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(the\s+)?([^.!?]{10,})'
        for term, article, definition in re.findall(pattern3, text):
            if is_valid_term(term):
                full_def = (article if article else '') + definition
                definitions.append({
                    'term': term.strip(),
                    'definition': full_def.strip()
                })
        
        # Pattern 4: "X was/were Y"
        pattern4 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:was|were)\s+(an?\s+)?([^.!?]{10,})'
        for term, article, definition in re.findall(pattern4, text):
            if is_valid_term(term):
                full_def = (article if article else '') + definition
                definitions.append({
                    'term': term.strip(),
                    'definition': full_def.strip()
                })
        
        # Pattern 5: "X is known as Y"
        pattern5 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(?:known|called|acknowledged)\s+as\s+([^.!?]+)'
        for term, definition in re.findall(pattern5, text):
            if is_valid_term(term) and len(definition.strip()) > 5:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        
        # Remove duplicates
        seen = set()
        unique = []
        for defn in definitions:
            if defn['term'] not in seen:
                seen.add(defn['term'])
                unique.append(defn)
        
        return unique
    
    def extract_examples(self, text: str) -> List[str]:
        """Extract examples."""
        patterns = [
            r'(?:for example|e\.g\.|such as|for instance)[,:]?\s+([^.!?]+)',
            r'Example:\s+([^.!?\n]+)'
        ]
        
        examples = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            examples.extend([m.strip() for m in matches])
        
        return examples
    
    def process(self, text: str) -> Dict:
        """Process note and return structured data."""
        return {
            'concepts': self.extract_concepts(text),
            'definitions': self.extract_definitions(text),
            'examples': self.extract_examples(text),
            'word_count': len(text.split())
        }
    
    def format_output(self, result: Dict, filename: str = "") -> str:
        """Format results."""
        lines = []
        
        if filename:
            lines.append(f"\n{'='*70}")
            lines.append(f"📄 {filename}")
        
        lines.append(f"{'='*70}")
        
        # Concepts
        lines.append(f"\n📌 CONCEPTS ({len(result['concepts'])}):")
        if result['concepts']:
            for i, concept in enumerate(result['concepts'], 1):
                lines.append(f"   {i}. {concept}")
        else:
            lines.append("   (none found)")
        
        # Definitions
        if result['definitions']:
            lines.append(f"\n📖 DEFINITIONS ({len(result['definitions'])}):")
            for defn in result['definitions']:
                definition = defn['definition']
                if len(definition) > 65:
                    definition = definition[:65] + "..."
                lines.append(f"   • {defn['term']}: {definition}")
        
        # Examples
        if result['examples']:
            lines.append(f"\n💡 EXAMPLES ({len(result['examples'])}):")
            for example in result['examples']:
                if len(example) > 65:
                    example = example[:65] + "..."
                lines.append(f"   • {example}")
        
        # Stats
        lines.append(f"\n📊 STATS:")
        lines.append(f"   Words: {result['word_count']}")
        lines.append(f"   Concepts: {len(result['concepts'])}")
        lines.append(f"   Definitions: {len(result['definitions'])}")
        
        lines.append(f"{'='*70}\n")
        
        return '\n'.join(lines)


def main():
    """Test processor."""
    print("=" * 70)
    print("SmartNotes - Final Clean Processor")
    print("=" * 70)
    print("✅ All issues fixed - production ready!\n")
    
    processor = NoteProcessor()
    
    test_files = [
        'data/raw_notes/biology_notes.txt',
        'data/raw_notes/history_notes.txt',
        'data/raw_notes/math_notes.txt',
        'data/raw_notes/literature_notes.txt'
    ]
    
    for filepath in test_files:
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        result = processor.process(text)
        print(processor.format_output(result, os.path.basename(filepath)))


if __name__ == "__main__":
    main()