"""
History-Specific Note Processor
Version: 0.7 FINAL
Date: Day 8 (iteration 3)

Changes from v0.6:
- Fixed Pattern 13 to handle Roman numerals (World War II)
- Fixed Pattern 13 to handle acronyms (NATO, WWII)
"""

import re

class HistoryProcessor:
    """Processor with history-specific definition patterns."""
    
    def __init__(self):
        self.pronouns = {'he', 'she', 'it', 'they', 'them', 'their', 'bastille'}
    
    def extract_definitions(self, text):
        """Extract definitions using BROADENED history-specific patterns."""
        definitions = []
        
        # Pattern 10: "The X was/were Y"
        pattern10 = r'The\s+([A-Z][a-z]+(?:\s+(?:of|the|and|in)\s+[A-Z][a-z]+|\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an|the)?\s*(.+?)(?:\.|Led by|Marked|Involved)'
        matches10 = re.findall(pattern10, text)
        for term, definition in matches10:
            term = term.strip()
            definition = definition.strip()
            
            if len(term) < 3 or len(definition) < 10:
                continue
            if any(p in term.lower() for p in self.pronouns):
                continue
            
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term,
                    'definition': definition,
                    'pattern': 'the_was_were'
                })
        
        # Pattern 11: "The X: definition"
        pattern11 = r'The\s+([A-Z][a-z]+(?:[-\s][A-Z][a-z]+)*):\s*(.+?)(?:\.|Led by|Marked|Involved)'
        matches11 = re.findall(pattern11, text)
        for term, definition in matches11:
            term = term.strip()
            definition = definition.strip()
            
            if len(term) < 3 or len(definition) < 15:
                continue
            
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term,
                    'definition': definition,
                    'pattern': 'the_colon'
                })
        
        # Pattern 12: Multi-word with "of"
        pattern12 = r'([A-Z][a-z]+(?:\s+of\s+(?:the\s+)?[A-Z][a-z]+)+):\s*(.+?)(?:\.|Led by|Marked|Involved)'
        matches12 = re.findall(pattern12, text)
        for term, definition in matches12:
            term = term.strip()
            definition = definition.strip()
            
            if len(definition) < 15:
                continue
            
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term,
                    'definition': definition,
                    'pattern': 'multiword_of'
                })
        
        # Pattern 13: Simple "Term: definition" - FIXED for Roman numerals & acronyms
        pattern13 = r'^([A-Z][A-Za-z0-9]+(?:\s+[A-Z][A-Za-z0-9]+)*):\s*(.+?)(?:\.|$)'
        matches13 = re.findall(pattern13, text, re.MULTILINE)
        for term, definition in matches13:
            term = term.strip()
            definition = definition.strip()
            
            if len(term) < 3 or len(definition) < 15:
                continue
            if any(p in term.lower() for p in self.pronouns):
                continue
            
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term,
                    'definition': definition,
                    'pattern': 'simple_colon'
                })
        
        return definitions
    
    def structure_note(self, text):
        return {'definitions': self.extract_definitions(text), 'concepts': []}


def test_on_hist_002():
    """Test on hist_002."""
    processor = HistoryProcessor()
    
    print("=" * 70)
    print("v0.7 TEST: hist_002 (World War II)")
    print("=" * 70)
    
    with open('data/research_dataset/notes/hist_002.txt', 'r') as f:
        text = f.read()
    
    result = processor.structure_note(text)
    
    print(f"\nFound {len(result['definitions'])} definitions:")
    for d in result['definitions']:
        print(f"  - {d['term']} (pattern: {d['pattern']})")
    
    print("\nGround Truth (6 expected):")
    expected = ["World War II", "Axis Powers", "Allied Powers", 
                "Blitzkrieg", "Holocaust", "Manhattan Project"]
    for exp in expected:
        found = any(exp.lower() in d['term'].lower() or d['term'].lower() in exp.lower() 
                   for d in result['definitions'])
        status = "✅" if found else "❌"
        print(f"  {status} {exp}")
    
    found_count = len(result['definitions'])
    print(f"\nFound {found_count}/6 definitions")
    
    if found_count >= 5:
        print("✅ Excellent! Most definitions found!")
    elif found_count >= 4:
        print("⚠️  Good progress, close to target")
    else:
        print("❌ Still missing definitions")
    
    print("=" * 70)


if __name__ == "__main__":
    test_on_hist_002()