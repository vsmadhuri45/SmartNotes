"""
Week 4 Task 1: Error Analysis
Find which definitions are being missed and why
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def analyze_errors():
    processor = UnifiedProcessor()
    
    # Focus on worst performing notes
    problem_notes = [
        ('hist_003', 57.1),  # Worst overall
        ('math_007', 60.0),  # Math problem
        ('hist_005', 66.7),  # History problem
        ('math_005', 71.4),  # Math problem
    ]
    
    print("=" * 70)
    print("ERROR ANALYSIS: Why are these notes failing?")
    print("=" * 70)
    
    for note_id, expected_f1 in problem_notes:
        print(f"\n{'='*70}")
        print(f"ANALYZING: {note_id} (F1: {expected_f1}%)")
        print('='*70)
        
        # Read note and annotation
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        with open(f'data/research_dataset/annotations/{note_id}.json', 'r') as f:
            annotation = json.load(f)
        
        # Extract definitions
        result = processor.structure_note(text)
        
        gt_terms = {d['term'].lower(): d['definition'] for d in annotation['ground_truth']['definitions']}
        ex_terms = {d['term'].lower(): d for d in result['definitions']}
        
        # Find misses
        print("\n❌ MISSED DEFINITIONS (should have caught):")
        for gt_term, gt_def in gt_terms.items():
            found = False
            for ex_term in ex_terms.keys():
                if gt_term in ex_term or ex_term in gt_term:
                    found = True
                    break
            
            if not found:
                # Find in original text
                for line in text.split('\n'):
                    if gt_term.replace('_', ' ') in line.lower():
                        print(f"\n  Term: '{gt_term}'")
                        print(f"  In text: '{line.strip()}'")
                        print(f"  Why missed: ???")
                        break
        
        # Find false positives
        print("\n⚠️  FALSE POSITIVES (shouldn't have caught):")
        for ex_term, ex_data in ex_terms.items():
            found = False
            for gt_term in gt_terms.keys():
                if gt_term in ex_term or ex_term in gt_term:
                    found = True
                    break
            
            if not found:
                print(f"\n  Term: '{ex_term}' (pattern: {ex_data['pattern']})")
                print(f"  Definition: '{ex_data['definition'][:60]}...'")
    
    print("\n" + "="*70)
    print("SUMMARY: Common Error Patterns")
    print("="*70)
    print("\nNext steps:")
    print("1. Look for missing patterns")
    print("2. Refine existing patterns")
    print("3. Add domain-specific rules")

if __name__ == "__main__":
    analyze_errors()
