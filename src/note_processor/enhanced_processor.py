"""
SmartNotes - Enhanced Note Processor (v0.3.1)
Module: note_processor
Author: Madhuri
Date: January 25, 2026

DAY 2 IMPROVEMENTS (v0.3.1 - BALANCED APPROACH):
- Keep pronoun filtering (prevents "She", "He", "They" false positives)
- Remove overly aggressive lowercase filtering (was breaking biology)
- Simplified math pattern (more permissive with validation)
- Target: Balance precision and recall

Changes in v0.3.1 (Balance fix):
1. Reverted overly aggressive Pattern 3 filters (was breaking biology)
2. Simplified math pattern - permissive regex + validation
3. Keep pronoun blacklist (works well)
4. Simpler is better!

Changes in v0.3 (Precision improvements):
1. Added pronoun blacklist (filters "he", "she", "they", etc.)
2. Added is_valid_term() validation function
3. Fixed "is given by" pattern: [a-zA-Z0-9] instead of [a-z]
4. Pattern 4 (was/were) requires multi-word capitalized terms only

Changes from v0.1 to v0.2:
1. extract_definitions() - SIGNIFICANTLY ENHANCED
   - Added "X is/are Y" pattern
   - Added "X was/were Y" pattern  
   - Added "X is given by Y" pattern (for formulas)
   - Added "X is known/acknowledged as Y" pattern
   - Added "X was formed/created/established" pattern
   - Better handling of multi-word terms
2. All other functions same as v0.1 (for now)
"""

import re
from typing import List, Dict, Set
from collections import Counter
import os


class EnhancedNoteProcessor:
    """
    Enhanced note processor with improved definition detection.
    
    v0.2 Improvements:
    - 7+ definition patterns (vs. 3 in v0.1)
    - Better multi-word term recognition
    - Formula-aware definitions
    """
    
    def __init__(self):
        # Same stop words as v0.1
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
        Extract key concepts from text (SAME AS v0.1 - will improve in Week 2)
        """
        text_lower = text.lower()
        text_clean = re.sub(r'[^\w\s-]', ' ', text_lower)
        words = text_clean.split()
        meaningful_words = [
            word for word in words 
            if word not in self.stop_words and len(word) > 3
        ]
        word_freq = Counter(meaningful_words)
        key_concepts = [word for word, _ in word_freq.most_common(top_n)]
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        capitalized_lower = [term.lower() for term in capitalized if len(term) > 3]
        all_concepts = list(set(key_concepts + capitalized_lower[:5]))
        return all_concepts[:top_n]
    
    def extract_definitions(self, text: str) -> List[Dict[str, str]]:
        """
        ⭐ ENHANCED v0.3: Extract definitions with PRECISION improvements.
        
        NEW in v0.3 (Day 2 - Precision Fix):
        - Pronoun filtering (no "He", "She", "They", etc.)
        - Better math formula handling (variables like "nth")
        - Term validation (multi-word or capitalized only)
        - Fragment filtering
        
        v0.2: 7+ patterns vs. 3 in v0.1
        
        Patterns covered:
        1. "X is defined as Y"
        2. "X means Y"  
        3. "X: Y" (colon)
        4. "X is/are Y" ← NEW v0.2
        5. "X was/were Y" ← NEW v0.2
        6. "X is given by Y" ← NEW v0.2 (for formulas) + FIXED v0.3
        7. "X is known/acknowledged as Y" ← NEW v0.2
        8. "X was formed/created/established" ← NEW v0.2
        
        Returns:
            List of dictionaries with 'term' and 'definition'
        """
        definitions = []
        
        # Pronoun blacklist (v0.3 addition)
        pronouns = {
            'he', 'she', 'it', 'they', 'we', 'you', 'i', 'him', 'her', 'them', 
            'us', 'his', 'hers', 'its', 'their', 'our', 'your', 'my',
            'this', 'that', 'these', 'those', 'who', 'what', 'which'
        }
        
        def is_valid_term(term: str) -> bool:
            """
            Validate if a term is a real concept (not pronoun/fragment).
            v0.3 addition for precision.
            """
            term_clean = term.strip().lower()
            
            # Filter 1: No pronouns
            if term_clean in pronouns:
                return False
            
            # Filter 2: Must be capitalized OR multi-word
            # (Single lowercase words are usually not terms)
            words = term.strip().split()
            if len(words) == 1 and not term[0].isupper():
                return False
            
            # Filter 3: Minimum length (avoid fragments like "A", "An")
            if len(term_clean) < 3:
                return False
            
            return True
        
        
        # ===== PATTERN 1: "X is defined as Y" (EXISTING) =====
        pattern1 = r'([A-Z][a-z]+(?:\s+[a-z]+)?)\s+(?:is|means|refers to|is defined as)\s+([^.!?]+)'
        matches1 = re.findall(pattern1, text)
        for term, definition in matches1:
            definitions.append({
                'term': term.strip(),
                'definition': definition.strip(),
                'pattern': 'is_defined_as'
            })
        
        # ===== PATTERN 2: "X: definition" (EXISTING) =====
        pattern2 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]+)'
        matches2 = re.findall(pattern2, text)
        for term, definition in matches2:
            if len(definition) > 15:  # Filter out short non-definitions
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'colon'
                })
        
        # ===== PATTERN 3: "X is/are Y" (NEW v0.2, IMPROVED v0.3.1) =====
        # Example: "Vertebrates are the animals possessing backbones"
        # Example: "Amphibians are species that live..."
        # v0.3.1: Simplified - only filter pronouns, don't over-filter
        pattern3 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(the\s+)?([^.!?]+)'
        matches3 = re.findall(pattern3, text)
        for term, article, definition in matches3:
            # v0.3: Validate term (no pronouns)
            if not is_valid_term(term):
                continue
            
            # Filter out very short definitions
            if len(definition) > 10:
                # Avoid catching questions
                if not term.lower().startswith(('what', 'how', 'why', 'when', 'where')):
                    full_def = (article + definition).strip()
                    definitions.append({
                        'term': term.strip(),
                        'definition': full_def,
                        'pattern': 'is_are'
                    })
        
        # ===== PATTERN 4: "X was/were Y" (NEW!) =====
        # Example: "Russia was an autocracy"
        # Updated: Filter out pronouns to avoid false positives like "She was nervous"
        pattern4 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:was|were)\s+(an?\s+)?([^.!?]+)'
        matches4 = re.findall(pattern4, text)
        for term, article, definition in matches4:
            # Filter out single-word subjects (likely pronouns)
            # Only accept multi-word capitalized terms
            if len(definition) > 10:
                full_def = (article + definition).strip()
                definitions.append({
                    'term': term.strip(),
                    'definition': full_def,
                    'pattern': 'was_were'
                })
        
        # ===== PATTERN 5: "X is given by Y" (NEW v0.2, SIMPLIFIED v0.3.1) =====
        # Example: "The nth term is given by an = a + (n-1)d"
        # v0.3.1: SIMPLIFIED - be very permissive, then validate
        # Just look for "is given by" and capture everything before/after
        pattern5 = r'((?:[Tt]he|the)\s+.{5,80}?)\s+is given by\s+([^.!?\n]{3,})'
        matches5 = re.findall(pattern5, text, re.IGNORECASE | re.DOTALL)
        
        for term, definition in matches5:
            term_clean = term.strip()
            definition_clean = definition.strip()
            
            # Validate: term must be math-related
            term_lower = term_clean.lower()
            if any(word in term_lower for word in ['term', 'sum', 'formula', 'equation', 'nth', 'product']):
                # Avoid duplicates
                if not any(d['term'].lower().strip() == term_lower for d in definitions):
                    definitions.append({
                        'term': term_clean,
                        'definition': definition_clean,
                        'pattern': 'given_by'
                    })
        
        # ===== PATTERN 6: "X is known/acknowledged as Y" (NEW!) =====
        # Example: "Bryozoans are normally acknowledged as moss animals"
        pattern6 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(?:normally\s+)?(?:known|acknowledged|recognized|called)\s+as\s+([^.!?]+)'
        matches6 = re.findall(pattern6, text)
        for term, definition in matches6:
            if len(definition) > 5:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'known_as'
                })
        
        # ===== PATTERN 7: "X was formed/created/established in Y" (NEW!) =====
        # Example: "The party was formed in 1900"
        pattern7 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+was\s+(?:formed|created|established|founded)\s+(in\s+[0-9]{4}|[^.!?]+)'
        matches7 = re.findall(pattern7, text)
        for term, context in matches7:
            definitions.append({
                'term': term.strip(),
                'definition': f"formed/established {context.strip()}",
                'pattern': 'formed'
            })
        
        # Remove duplicates (same term defined multiple times)
        seen_terms = set()
        unique_definitions = []
        for defn in definitions:
            if defn['term'] not in seen_terms:
                seen_terms.add(defn['term'])
                unique_definitions.append(defn)
        
        return unique_definitions
    
    def extract_examples(self, text: str) -> List[str]:
        """
        Extract examples from text (SAME AS v0.1)
        """
        examples = []
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
        Classify note type (SAME AS v0.1 - will improve later)
        """
        text_lower = text.lower()
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
        note_type = max(scores, key=scores.get)
        return note_type if scores[note_type] > 0 else 'general'
    
    def structure_note(self, text: str) -> Dict:
        """
        Main function: Process raw note and return structured output.
        """
        structured = {
            'original_text': text,
            'note_type': self.identify_note_type(text),
            'key_concepts': self.extract_key_concepts(text),
            'definitions': self.extract_definitions(text),  # ⭐ ENHANCED!
            'examples': self.extract_examples(text),
            'word_count': len(text.split()),
            'version': 'v0.3.1'  # Track version - balanced approach
        }
        return structured
    
    def format_structured_note(self, structured: Dict) -> str:
        """
        Format structured note into readable markdown.
        """
        output = []
        output.append(f"# Structured Note (v{structured.get('version', '0.3')})")
        output.append(f"\n**Note Type**: {structured['note_type'].title()}")
        output.append(f"**Word Count**: {structured['word_count']}")
        
        output.append(f"\n## Key Concepts")
        for concept in structured['key_concepts']:
            output.append(f"- {concept.title()}")
        
        if structured['definitions']:
            output.append(f"\n## Definitions ({len(structured['definitions'])} found)")
            for defn in structured['definitions']:
                # Show which pattern caught it (for debugging)
                pattern_label = defn.get('pattern', 'unknown')
                output.append(f"- **{defn['term']}**: {defn['definition']} `[{pattern_label}]`")
        
        if structured['examples']:
            output.append(f"\n## Examples")
            for example in structured['examples']:
                output.append(f"- {example}")
        
        output.append(f"\n## Original Text")
        output.append(f"{structured['original_text'][:500]}...")  # Truncate for readability
        
        return '\n'.join(output)


def test_with_all_notes():
    """
    Test the enhanced processor with all 4 test notes and calculate metrics.
    """
    print("=" * 70)
    print("SmartNotes - Enhanced Note Processor v0.3.1")
    print("DAY 2: Testing BALANCED Definition Detection")
    print("=" * 70)
    
    processor = EnhancedNoteProcessor()
    
    # Ground truth: how many definitions SHOULD be in each note
    ground_truth = {
        'biology_notes.txt': 8,
        'history_notes.txt': 2,
        'math_notes.txt': 2,
        'literature_notes.txt': 0
    }
    
    total_found = 0
    total_expected = sum(ground_truth.values())
    
    # Test each note
    test_files = [
        'data/raw_notes/biology_notes.txt',
        'data/raw_notes/history_notes.txt',
        'data/raw_notes/math_notes.txt',
        'data/raw_notes/literature_notes.txt'
    ]
    
    results = []
    
    for filepath in test_files:
        filename = filepath.split('/')[-1]
        
        # Check if file exists
        if not os.path.exists(filepath):
            print(f"\n⚠️  File not found: {filepath}")
            print(f"   Please make sure your test notes are in data/raw_notes/")
            continue
        
        # Read and process
        with open(filepath, 'r') as f:
            text = f.read()
        
        structured = processor.structure_note(text)
        found = len(structured['definitions'])
        expected = ground_truth.get(filename, 0)
        
        total_found += found
        
        # Calculate accuracy for this note
        if expected > 0:
            accuracy = (found / expected) * 100
        else:
            accuracy = 100 if found == 0 else 0
        
        results.append({
            'file': filename,
            'expected': expected,
            'found': found,
            'accuracy': accuracy
        })
        
        # Print results for this note
        print(f"\n{'='*70}")
        print(f"File: {filename}")
        print(f"Expected definitions: {expected}")
        print(f"Found definitions: {found}")
        print(f"Accuracy: {accuracy:.1f}%")
        
        if structured['definitions']:
            print(f"\nDefinitions found:")
            for defn in structured['definitions']:
                print(f"  - {defn['term']}: {defn['definition'][:60]}... [{defn['pattern']}]")
        
    # Overall metrics
    print(f"\n{'='*70}")
    print(f"OVERALL RESULTS:")
    print(f"{'='*70}")
    print(f"Total definitions expected: {total_expected}")
    print(f"Total definitions found: {total_found}")
    
    overall_accuracy = (total_found / total_expected * 100) if total_expected > 0 else 0
    print(f"Overall accuracy: {overall_accuracy:.1f}%")
    
    # Comparison with previous versions
    print(f"\n{'='*70}")
    print(f"IMPROVEMENT OVER PREVIOUS VERSIONS:")
    print(f"{'='*70}")
    print(f"v0.1 (Day 1 - baseline):     0/12 definitions (0%)")
    print(f"v0.2 (Day 2 - first try):   14/12 definitions (116.7% - had false positives)")
    print(f"v0.3 (Day 2 - too strict):  4/12 definitions (33.3% - over-filtered)")
    print(f"v0.3.1 (Day 2 - balanced):  {total_found}/{total_expected} definitions ({overall_accuracy:.1f}%)")
    print(f"\nBalance: Pronoun filtering + permissive patterns")
    
    if overall_accuracy >= 90 and total_found <= total_expected + 1:
        print(f"\n🎉 EXCELLENT! High recall AND precision!")
    elif overall_accuracy >= 70:
        print(f"\n✅ SUCCESS! Exceeded 70% target!")
    elif overall_accuracy >= 50:
        print(f"\n⚡ Good progress! Close to 70% target.")
    else:
        print(f"\n⚠️  Need more work to reach 70% target.")
    
    # Precision check
    if total_found > total_expected:
        print(f"⚠️  Note: Found more than expected - check for false positives")
    
    print(f"\n{'='*70}")
    
    return {
        'total_expected': total_expected,
        'total_found': total_found,
        'accuracy': overall_accuracy,
        'details': results
    }


def main():
    """
    Run tests and show results
    """
    results = test_with_all_notes()
    
    print("\n" + "=" * 70)
    print("Testing complete! Check results above.")
    print("=" * 70)


if __name__ == "__main__":
    main()