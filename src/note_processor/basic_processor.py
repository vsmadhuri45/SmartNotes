"""
SmartNotes - Basic Note Processor (Prototype v0.1)
Module: note_processor
Author: Madhuri
Date: January 24, 2026

Purpose: Extract key concepts from raw educational notes
This is our FIRST working prototype!
"""

import re
from typing import List, Dict, Set
from collections import Counter
import os


class BasicNoteProcessor:
    """
    Basic note processor that extracts key information from raw text.
    
    Features:
    1. Extract key concepts (important terms/phrases)
    2. Identify definitions
    3. Detect examples
    4. Structure output
    """
    
    def __init__(self):
        # Common words to ignore when identifying key concepts
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
            'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
            'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'just', 'also'
        }
        
    def extract_key_concepts(self, text: str, top_n: int = 10) -> List[str]:
        """
        Extract key concepts from text using frequency analysis and pattern matching.
        
        Args:
            text: Raw note text
            top_n: Number of top concepts to return
            
        Returns:
            List of key concepts
        """
        # Convert to lowercase
        text_lower = text.lower()
        
        # Remove punctuation except hyphens (for compound terms)
        text_clean = re.sub(r'[^\w\s-]', ' ', text_lower)
        
        # Extract words
        words = text_clean.split()
        
        # Filter out stop words and short words
        meaningful_words = [
            word for word in words 
            if word not in self.stop_words and len(word) > 3
        ]
        
        # Count frequency
        word_freq = Counter(meaningful_words)
        
        # Get top N words
        key_concepts = [word for word, _ in word_freq.most_common(top_n)]
        
        # Also look for capitalized terms (proper nouns, important concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        capitalized_lower = [term.lower() for term in capitalized if len(term) > 3]
        
        # Combine and deduplicate
        all_concepts = list(set(key_concepts + capitalized_lower[:5]))
        
        return all_concepts[:top_n]
    
    def extract_definitions(self, text: str) -> List[Dict[str, str]]:
        """
        Extract definitions from text using pattern matching.
        
        Patterns like:
        - "X is defined as Y"
        - "X means Y"
        - "X: Y" (colon definitions)
        
        Returns:
            List of dictionaries with 'term' and 'definition'
        """
        definitions = []
        
        # Pattern 1: "X is/means/refers to Y"
        pattern1 = r'([A-Z][a-z]+(?:\s+[a-z]+)?)\s+(?:is|means|refers to|is defined as)\s+([^.!?]+)'
        matches1 = re.findall(pattern1, text)
        
        for term, definition in matches1:
            definitions.append({
                'term': term.strip(),
                'definition': definition.strip()
            })
        
        # Pattern 2: "Term: definition"
        pattern2 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]+)'
        matches2 = re.findall(pattern2, text)
        
        for term, definition in matches2:
            if len(definition) > 15:  # Filter out short non-definitions
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip()
                })
        
        return definitions
    
    def extract_examples(self, text: str) -> List[str]:
        """
        Extract examples from text.
        
        Looks for patterns like:
        - "for example"
        - "e.g."
        - "such as"
        """
        examples = []
        
        # Pattern: sentences containing example indicators
        example_patterns = [
            r'(?:for example|e\.g\.|such as|for instance)[,:]?\s+([^.!?]+)',
            r'Example:\s+([^.!?\n]+)'
        ]
        
        for pattern in example_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            examples.extend([match.strip() for match in matches])
        
        return examples
    
    def identify_note_type(self, text: str) -> str:
        """
        Classify note type based on content.
        
        Types:
        - Conceptual: definitions, explanations
        - Procedural: steps, processes, how-to
        - Factual: lists, data, facts
        - Analytical: comparisons, arguments
        """
        text_lower = text.lower()
        
        # Count indicators
        procedural_indicators = ['step', 'first', 'second', 'then', 'next', 'finally', 'how to']
        conceptual_indicators = ['define', 'concept', 'theory', 'principle', 'means', 'refers to']
        factual_indicators = ['fact', 'data', 'statistic', 'number', 'date', 'year']
        analytical_indicators = ['compare', 'contrast', 'analyze', 'however', 'whereas', 'although']
        
        scores = {
            'procedural': sum(1 for ind in procedural_indicators if ind in text_lower),
            'conceptual': sum(1 for ind in conceptual_indicators if ind in text_lower),
            'factual': sum(1 for ind in factual_indicators if ind in text_lower),
            'analytical': sum(1 for ind in analytical_indicators if ind in text_lower)
        }
        
        # Return type with highest score
        note_type = max(scores, key=scores.get)
        return note_type if scores[note_type] > 0 else 'general'
    
    def structure_note(self, text: str) -> Dict:
        """
        Main function: Process raw note and return structured output.
        
        Args:
            text: Raw note text
            
        Returns:
            Dictionary with structured note components
        """
        structured = {
            'original_text': text,
            'note_type': self.identify_note_type(text),
            'key_concepts': self.extract_key_concepts(text),
            'definitions': self.extract_definitions(text),
            'examples': self.extract_examples(text),
            'word_count': len(text.split())
        }
        
        return structured
    
    def format_structured_note(self, structured: Dict) -> str:
        """
        Format structured note into readable markdown.
        """
        output = []
        output.append(f"# Structured Note")
        output.append(f"\n**Note Type**: {structured['note_type'].title()}")
        output.append(f"**Word Count**: {structured['word_count']}")
        
        output.append(f"\n## Key Concepts")
        for concept in structured['key_concepts']:
            output.append(f"- {concept.title()}")
        
        if structured['definitions']:
            output.append(f"\n## Definitions")
            for defn in structured['definitions']:
                output.append(f"- **{defn['term']}**: {defn['definition']}")
        
        if structured['examples']:
            output.append(f"\n## Examples")
            for example in structured['examples']:
                output.append(f"- {example}")
        
        output.append(f"\n## Original Text")
        output.append(f"{structured['original_text']}")
        
        return '\n'.join(output)


def main():
    """
    Demo function to test the processor
    """
    print("=" * 60)
    print("SmartNotes - Basic Note Processor v0.1")
    print("=" * 60)
    
    # Read from YOUR note file
    with open('data/raw_notes/literature_notes.txt', 'r') as f:
        sample_note = f.read()
    
    # Process the note
    processor = BasicNoteProcessor()
    structured = processor.structure_note(sample_note)
    
    # Display results
    print("\n" + processor.format_structured_note(structured))
    print("\n" + "=" * 60)
    print("Processing complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
