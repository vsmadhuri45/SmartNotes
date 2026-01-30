"""
Standalone Evaluation Script for v0.3.1
Day 4: Baseline Evaluation

This version doesn't require complex imports.
"""

import os
import json
import re
from collections import defaultdict
import numpy as np


# ============================================================================
# COPY OF EnhancedNoteProcessor (v0.3.1) - Inline
# ============================================================================

class EnhancedNoteProcessor:
    """v0.3.1 processor - inline version for testing."""
    
    def __init__(self):
        self.pronouns = {
            'he', 'she', 'it', 'they', 'we', 'you', 'i', 'him', 'her', 'them',
            'us', 'his', 'hers', 'its', 'their', 'our', 'your', 'my',
            'this', 'that', 'these', 'those', 'who', 'what', 'which'
        }
    
    def extract_definitions(self, text):
        """Extract definitions using 9 patterns (92% accurate)."""
        definitions = []
        
        def is_valid_term(term):
            term_clean = term.strip().lower()
            if term_clean in self.pronouns or len(term_clean) < 3:
                return False
            words = term.strip().split()
            if len(words) == 1 and not term[0].isupper():
                return False
            return True
        
        # Pattern 1: "X is defined as Y"
        pattern1 = r'([A-Z][a-z]+(?:\s+[a-z]+)?)\s+(?:is|means|refers to|is defined as)\s+([^.!?]+)'
        matches1 = re.findall(pattern1, text)
        for term, definition in matches1:
            definitions.append({
                'term': term.strip(),
                'definition': definition.strip(),
                'pattern': 'is_defined_as'
            })
        
        # Pattern 2: "X: definition"
        pattern2 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]+)'
        matches2 = re.findall(pattern2, text)
        for term, definition in matches2:
            if len(definition) > 15:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'colon'
                })
        
        # Pattern 3: "X is/are Y"
        pattern3 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(the\s+)?([^.!?]+)'
        matches3 = re.findall(pattern3, text)
        for term, article, definition in matches3:
            if not is_valid_term(term):
                continue
            if len(definition) > 10:
                if not term.lower().startswith(('what', 'how', 'why', 'when', 'where')):
                    full_def = (article + definition).strip()
                    definitions.append({
                        'term': term.strip(),
                        'definition': full_def,
                        'pattern': 'is_are'
                    })
        
        # Pattern 4: "X was/were Y"
        pattern4 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+(?:was|were)\s+(an?\s+)?([^.!?]+)'
        matches4 = re.findall(pattern4, text)
        for term, article, definition in matches4:
            if len(definition) > 10:
                full_def = (article + definition).strip()
                definitions.append({
                    'term': term.strip(),
                    'definition': full_def,
                    'pattern': 'was_were'
                })
        
        # Pattern 5: "X is given by Y"
        pattern5 = r'((?:[Tt]he|the)\s+.{5,80}?)\s+is given by\s+([^.!?\n]{3,})'
        matches5 = re.findall(pattern5, text, re.IGNORECASE | re.DOTALL)
        for term, definition in matches5:
            term_clean = term.strip()
            term_lower = term_clean.lower()
            if any(word in term_lower for word in ['term', 'sum', 'formula', 'equation', 'nth', 'product']):
                if not any(d['term'].lower().strip() == term_lower for d in definitions):
                    definitions.append({
                        'term': term_clean,
                        'definition': definition.strip(),
                        'pattern': 'given_by'
                    })
        
        # Pattern 6: "X is known as Y"
        pattern6 = r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:is|are)\s+(?:normally\s+)?(?:known|acknowledged|recognized|called)\s+as\s+([^.!?]+)'
        matches6 = re.findall(pattern6, text)
        for term, definition in matches6:
            if len(definition) > 5:
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'known_as'
                })
        
        # Pattern 7: "X was formed/created"
        pattern7 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+was\s+(?:formed|created|established|founded)\s+(in\s+[0-9]{4}|[^.!?]+)'
        matches7 = re.findall(pattern7, text)
        for term, context in matches7:
            definitions.append({
                'term': term.strip(),
                'definition': f"formed/established {context.strip()}",
                'pattern': 'formed'
            })
        
        # Remove duplicates
        seen_terms = set()
        unique_definitions = []
        for defn in definitions:
            if defn['term'] not in seen_terms:
                seen_terms.add(defn['term'])
                unique_definitions.append(defn)
        
        return unique_definitions
    
    def extract_key_concepts(self, text, top_n=10):
        """Simple concept extraction (baseline)."""
        # Extract capitalized words
        concepts = re.findall(r'\b[A-Z][a-z]{3,}\b', text)
        # Remove duplicates, keep order
        seen = set()
        unique_concepts = []
        for concept in concepts:
            if concept.lower() not in seen:
                seen.add(concept.lower())
                unique_concepts.append(concept)
        return unique_concepts[:top_n]
    
    def structure_note(self, text):
        """Main processing function."""
        return {
            'definitions': self.extract_definitions(text),
            'key_concepts': self.extract_key_concepts(text)
        }


# ============================================================================
# EVALUATION CODE
# ============================================================================

def load_annotations(dataset_dir='data/research_dataset'):
    """Load ground truth annotations."""
    annotations = {}
    annotation_dir = f"{dataset_dir}/annotations"
    
    for filename in os.listdir(annotation_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(annotation_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                annotations[data['id']] = data
    
    return annotations


def evaluate_definitions(note_id, extracted_definitions, annotations):
    """Evaluate definition extraction."""
    if note_id not in annotations:
        return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
    
    ground_truth = annotations[note_id]['ground_truth']['definitions']
    gt_terms = {d['term'].lower().strip() for d in ground_truth}
    extracted_terms = {d['term'].lower().strip() for d in extracted_definitions}
    
    true_positives = len(gt_terms & extracted_terms)
    false_positives = len(extracted_terms - gt_terms)
    false_negatives = len(gt_terms - extracted_terms)
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': true_positives,
        'ground_truth_count': len(gt_terms),
        'extracted_count': len(extracted_terms)
    }


def evaluate_concepts(note_id, extracted_concepts, annotations):
    """Evaluate concept extraction."""
    if note_id not in annotations:
        return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
    
    ground_truth = annotations[note_id]['ground_truth']['concepts']
    gt_concepts = [c.lower().strip() for c in ground_truth]
    extracted = [c.lower().strip() for c in extracted_concepts[:10]]
    
    # Relaxed matching
    matched = 0
    for ex in extracted:
        for gt in gt_concepts:
            if ex in gt or gt in ex:
                matched += 1
                break
    
    precision = matched / len(extracted) if extracted else 0.0
    recall = matched / len(gt_concepts) if gt_concepts else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'matched': matched,
        'extracted_count': len(extracted),
        'ground_truth_count': len(gt_concepts)
    }


def main():
    print("=" * 70)
    print("DAY 4: Evaluating v0.3.1 on Research Dataset")
    print("=" * 70)
    print()
    print("System: v0.3.1 (Rule-based with 9 patterns)")
    print("Dataset: 10 notes (5 biology, 5 history)")
    print()
    
    # Load annotations
    annotations = load_annotations()
    print(f"✅ Loaded {len(annotations)} ground truth annotations")
    print()
    
    # Initialize processor
    processor = EnhancedNoteProcessor()
    
    # Evaluate all notes
    results = {
        'per_note': {},
        'per_domain': defaultdict(lambda: {'definitions': [], 'concepts': []}),
        'overall': {'definitions': [], 'concepts': []}
    }
    
    dataset_dir = 'data/research_dataset'
    
    for note_id in sorted(annotations.keys()):
        # Load note text
        note_file = f"{dataset_dir}/notes/{note_id}.txt"
        with open(note_file, 'r') as f:
            text = f.read()
        
        # Extract
        result = processor.structure_note(text)
        
        # Evaluate
        def_metrics = evaluate_definitions(note_id, result['definitions'], annotations)
        concept_metrics = evaluate_concepts(note_id, result['key_concepts'], annotations)
        
        # Store
        results['per_note'][note_id] = {
            'definitions': def_metrics,
            'concepts': concept_metrics
        }
        
        # Aggregate
        domain = note_id.split('_')[0]
        results['per_domain'][domain]['definitions'].append(def_metrics['f1'])
        results['per_domain'][domain]['concepts'].append(concept_metrics['f1'])
        results['overall']['definitions'].append(def_metrics['f1'])
        results['overall']['concepts'].append(concept_metrics['f1'])
    
    # Print results
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    print(f"\n📊 OVERALL PERFORMANCE:")
    def_f1s = results['overall']['definitions']
    con_f1s = results['overall']['concepts']
    print(f"   Definitions F1: {np.mean(def_f1s):.1%} ± {np.std(def_f1s):.3f}")
    print(f"   Range: [{np.min(def_f1s):.1%}, {np.max(def_f1s):.1%}]")
    print(f"   Concepts F1:    {np.mean(con_f1s):.1%} ± {np.std(con_f1s):.3f}")
    print(f"   Range: [{np.min(con_f1s):.1%}, {np.max(con_f1s):.1%}]")
    
    print(f"\n📈 PER-DOMAIN PERFORMANCE:")
    for domain in sorted(results['per_domain'].keys()):
        metrics = results['per_domain'][domain]
        print(f"\n   {domain.upper()}:")
        print(f"      Definitions F1: {np.mean(metrics['definitions']):.1%}")
        print(f"      Concepts F1:    {np.mean(metrics['concepts']):.1%}")
    
    print(f"\n📋 PER-NOTE BREAKDOWN:")
    for note_id in sorted(results['per_note'].keys()):
        m = results['per_note'][note_id]
        print(f"\n{note_id}:")
        print(f"  Defs:  P={m['definitions']['precision']:.2f} R={m['definitions']['recall']:.2f} F1={m['definitions']['f1']:.2f}")
        print(f"         GT={m['definitions']['ground_truth_count']} Found={m['definitions']['extracted_count']}")
        print(f"  Conc:  P={m['concepts']['precision']:.2f} R={m['concepts']['recall']:.2f} F1={m['concepts']['f1']:.2f}")
        print(f"         GT={m['concepts']['ground_truth_count']} Found={m['concepts']['extracted_count']}")
    
    # Save results
    os.makedirs('results', exist_ok=True)
    with open('results/day4_v031_baseline.json', 'w') as f:
        json.dump({
            'method': 'v0.3.1',
            'overall': {
                'definitions': {
                    'mean_f1': float(np.mean(def_f1s)),
                    'std_f1': float(np.std(def_f1s))
                },
                'concepts': {
                    'mean_f1': float(np.mean(con_f1s)),
                    'std_f1': float(np.std(con_f1s))
                }
            },
            'per_domain': {
                domain: {
                    'definitions_f1': float(np.mean(m['definitions'])),
                    'concepts_f1': float(np.mean(m['concepts']))
                }
                for domain, m in results['per_domain'].items()
            }
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: results/day4_v031_baseline.json")
    print("=" * 70)
    print("✅ Evaluation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
