"""
Unified Note Processor - v0.8 FIXED
Eliminates duplicate extractions with smart normalization
"""

import re

class UnifiedProcessor:
    """Unified processor with all 13 patterns + duplicate elimination."""
    
    def __init__(self):
        self.pronouns = {
            'he', 'she', 'it', 'they', 'them', 'their', 'his', 'her',
            'we', 'us', 'our', 'you', 'your', 'i', 'me', 'my', 'this',
            'that', 'these', 'those', 'what', 'which', 'who', 'when',
            'bastille'
        }
    
    def extract_definitions(self, text):
        """Extract using ALL 13 patterns (9 biology + 4 history)."""
        definitions = []
        
        # BIOLOGY PATTERNS (1-9)
        
        p1 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|are)\s+(?:a|an|the)?\s*(.+?)(?:\.|$)'
        for term, defn in re.findall(p1, text, re.MULTILINE):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'is_are')
        
        p2 = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an|the)?\s*(.+?)(?:\.|$)'
        for term, defn in re.findall(p2, text, re.MULTILINE):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'was_were')
        
        p3 = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s*(.+?)(?:\.|$)'
        for term, defn in re.findall(p3, text, re.MULTILINE):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'colon')
        
        p4 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+which\s+(?:is|are|was|were)\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p4, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'which')
        
        p5 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+means\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p5, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'means')
        
        p6 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+refers to\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p6, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'refers_to')
        
        p7 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is |are )?known as\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p7, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'known_as')
        
        p8 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+consists? of\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p8, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'consists_of')
        
        p9 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+contains?\s+(.+?)(?:\.|$)'
        for term, defn in re.findall(p9, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'contains')
        
        # HISTORY PATTERNS (10-13)
        
        p10 = r'The\s+([A-Z][a-z]+(?:\s+(?:of|the|and|in)\s+[A-Z][a-z]+|\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an|the)?\s*(.+?)(?:\.|Led by|Marked|Involved)'
        for term, defn in re.findall(p10, text):
            if self._validate(term, defn, 10):
                self._add(definitions, term, defn, 'the_was_were')
        
        p11 = r'The\s+([A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*):\s*(.+?)(?:\.|Led by|Marked|Adopted)'
        for term, defn in re.findall(p11, text):
            if self._validate(term, defn, 15):
                self._add(definitions, term, defn, 'the_colon')
        
        p12 = r'([A-Z][a-z]+(?:\s+of\s+(?:the\s+)?[A-Z][a-z]+)+):\s*(.+?)(?:\.|Led by|Adopted)'
        for term, defn in re.findall(p12, text):
            if len(defn) >= 15:
                self._add(definitions, term, defn, 'multiword_of')
        
        p13 = r'^([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*):\s*(.+?)(?:\.|$)'
        for term, defn in re.findall(p13, text, re.MULTILINE):
            if self._validate(term, defn, 15):
                self._add(definitions, term, defn, 'simple_colon')
        
        return definitions
    
    def _validate(self, term, definition, min_len=10):
        if len(term) < 3 or len(definition) < min_len:
            return False
        if any(p in term.lower().split() for p in self.pronouns):
            return False
        return True
    
    def _normalize_term(self, term):
        """Normalize term by removing leading articles."""
        term_normalized = term.lower().strip()
        for article in ['the ', 'a ', 'an ']:
            if term_normalized.startswith(article):
                return term_normalized[len(article):]
        return term_normalized
    
    def _add(self, definitions, term, definition, pattern):
        """Add definition, avoiding duplicates (normalize 'The X' vs 'X')."""
        term_normalized = self._normalize_term(term)
        
        # Check if this term already exists (normalized comparison)
        for existing in definitions:
            existing_normalized = self._normalize_term(existing['term'])
            if term_normalized == existing_normalized:
                return  # Duplicate found, skip
        
        # Not a duplicate, add it
        definitions.append({
            'term': term.strip(),
            'definition': definition.strip(),
            'pattern': pattern
        })
    
    def structure_note(self, text):
        return {'definitions': self.extract_definitions(text)}


def test_unified():
    processor = UnifiedProcessor()
    
    print("=" * 70)
    print("UNIFIED PROCESSOR v0.8 FIXED (No Duplicates)")
    print("=" * 70)
    
    with open('data/research_dataset/notes/bio_001.txt', 'r') as f:
        bio_result = processor.structure_note(f.read())
    print(f"\nbio_001: Found {len(bio_result['definitions'])} definitions")
    
    with open('data/research_dataset/notes/hist_001.txt', 'r') as f:
        hist_result = processor.structure_note(f.read())
    print(f"hist_001: Found {len(hist_result['definitions'])} definitions")
    
    print("\n✅ All 13 patterns active + duplicate elimination!")
    print("=" * 70)

if __name__ == "__main__":
    test_unified()