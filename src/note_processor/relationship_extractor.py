"""
Relationship Extractor - Week 4
Extracts semantic relationships between concepts for knowledge graph
"""

import re

class RelationshipExtractor:
    """Extract relationships between concepts."""
    
    def __init__(self):
        pass
    
    def extract_relationships(self, text, definitions):
        """
        Extract relationships from text given known definitions.
        
        Args:
            text: Raw note text
            definitions: List of extracted definitions with terms
        
        Returns:
            List of relationships: [{'source': term1, 'target': term2, 'type': rel_type}]
        """
        relationships = []
        terms = [d['term'].lower() for d in definitions]
        
        if len(terms) < 2:
            return relationships  # Need at least 2 terms for relationships
        
        # RELATIONSHIP TYPE 1: IS_EXAMPLE_OF
        # Pattern: "X is an example of Y"
        # Pattern: "For instance, X demonstrates Y"
        # Pattern: "such as X" after mentioning Y
        
        for line in text.split('\n'):
            line_lower = line.lower()
            
            # "X is an example of Y"
            match = re.search(r'(\w+(?:\s+\w+)*)\s+is\s+an?\s+example\s+of\s+(\w+(?:\s+\w+)*)', line_lower)
            if match:
                source, target = match.groups()
                if any(source in t or t in source for t in terms) and any(target in t or t in target for t in terms):
                    relationships.append({
                        'source': source.strip().title(),
                        'target': target.strip().title(),
                        'type': 'is_example_of',
                        'confidence': 0.9
                    })
            
            # "such as X" (X is example of previous term)
            match = re.search(r'such\s+as\s+(\w+(?:\s+\w+)*)', line_lower)
            if match:
                example = match.group(1).strip()
                # Look for term mentioned earlier in same sentence
                for term in terms:
                    if term in line_lower and term != example:
                        if any(example in t or t in example for t in terms):
                            relationships.append({
                                'source': example.title(),
                                'target': term.title(),
                                'type': 'is_example_of',
                                'confidence': 0.7
                            })
                            break
        
        # RELATIONSHIP TYPE 2: IS_PART_OF
        # Pattern: "X is part of Y"
        # Pattern: "Y consists of X"
        # Pattern: "Y contains X"
        
        for line in text.split('\n'):
            line_lower = line.lower()
            
            # "X is part of Y"
            match = re.search(r'(\w+(?:\s+\w+)*)\s+is\s+(?:a\s+)?part\s+of\s+(?:the\s+)?(\w+(?:\s+\w+)*)', line_lower)
            if match:
                source, target = match.groups()
                if any(source in t or t in source for t in terms) and any(target in t or t in target for t in terms):
                    relationships.append({
                        'source': source.strip().title(),
                        'target': target.strip().title(),
                        'type': 'is_part_of',
                        'confidence': 0.9
                    })
            
            # "Y consists of X"
            match = re.search(r'(\w+(?:\s+\w+)*)\s+consists?\s+of\s+(\w+(?:\s+\w+)*)', line_lower)
            if match:
                target, source = match.groups()  # Reversed!
                if any(source in t or t in source for t in terms) and any(target in t or t in target for t in terms):
                    relationships.append({
                        'source': source.strip().title(),
                        'target': target.strip().title(),
                        'type': 'is_part_of',
                        'confidence': 0.8
                    })
        
        # RELATIONSHIP TYPE 3: PREREQUISITE
        # Pattern: "Before learning X, students must know Y"
        # Pattern: "X requires understanding of Y"
        # Pattern: "X builds on Y"
        
        for line in text.split('\n'):
            line_lower = line.lower()
            
            # "X requires Y"
            match = re.search(r'(\w+(?:\s+\w+)*)\s+requires?\s+(?:understanding\s+of\s+)?(\w+(?:\s+\w+)*)', line_lower)
            if match:
                source, target = match.groups()
                if any(source in t or t in source for t in terms) and any(target in t or t in target for t in terms):
                    relationships.append({
                        'source': target.strip().title(),  # Y is prerequisite for X
                        'target': source.strip().title(),
                        'type': 'is_prerequisite_for',
                        'confidence': 0.8
                    })
            
            # "X builds on Y"
            match = re.search(r'(\w+(?:\s+\w+)*)\s+builds?\s+on\s+(\w+(?:\s+\w+)*)', line_lower)
            if match:
                source, target = match.groups()
                if any(source in t or t in source for t in terms) and any(target in t or t in target for t in terms):
                    relationships.append({
                        'source': target.strip().title(),  # Y is prerequisite for X
                        'target': source.strip().title(),
                        'type': 'is_prerequisite_for',
                        'confidence': 0.7
                    })
        
        return relationships


def test_extractor():
    """Quick test on sample text."""
    extractor = RelationshipExtractor()
    
    # Sample note with relationships
    text = """
    Photosynthesis
    
    Photosynthesis is the process by which plants convert sunlight into energy.
    
    Chlorophyll is a pigment that is part of the photosynthesis system.
    
    Plants are an example of organisms that perform photosynthesis.
    
    Understanding cellular respiration is required before learning photosynthesis.
    """
    
    definitions = [
        {'term': 'Photosynthesis'},
        {'term': 'Chlorophyll'},
        {'term': 'Plants'},
        {'term': 'Cellular Respiration'}
    ]
    
    relationships = extractor.extract_relationships(text, definitions)
    
    print("=" * 70)
    print("RELATIONSHIP EXTRACTION TEST")
    print("=" * 70)
    print(f"\nFound {len(relationships)} relationships:\n")
    
    for rel in relationships:
        print(f"  {rel['source']} --[{rel['type']}]--> {rel['target']}")
        print(f"  Confidence: {rel['confidence']:.1%}\n")
    
    print("=" * 70)

if __name__ == "__main__":
    test_extractor()
