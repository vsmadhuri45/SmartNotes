"""
Test HistoryProcessor on ALL 5 history notes
This reveals if we overfitted to hist_001 or discovered real patterns
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def test_all_history_notes():
    """Test on all 5 history notes to check generalization."""
    processor = UnifiedProcessor()
    
    history_notes = [
        'hist_001',  # French Revolution (what we tuned on)
        'hist_002',  # World War II
        'hist_003',  # Industrial Revolution
        'hist_004',  # Ancient Rome
        'hist_005'   # Cold War
    ]
    
    print("=" * 70)
    print("GENERALIZATION TEST: All 5 History Notes")
    print("=" * 70)
    print("\nTesting if patterns generalize beyond hist_001...\n")
    
    results = []
    
    for note_id in history_notes:
        print(f"\n{'='*70}")
        print(f"Testing: {note_id}")
        print('='*70)
        
        # Read note
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        # Read ground truth
        with open(f'data/research_dataset/annotations/{note_id}.json', 'r') as f:
            annotation = json.load(f)
        
        # Extract definitions
        extracted = processor.structure_note(text)
        
        # Compare
        ground_truth_defs = [d['term'].lower() for d in annotation['ground_truth']['definitions']]
        extracted_defs = [d['term'].lower() for d in extracted['definitions']]
        
        print(f"\nGround Truth ({len(ground_truth_defs)} definitions):")
        for gt in ground_truth_defs:
            print(f"  - {gt}")
        
        print(f"\nExtracted ({len(extracted_defs)} definitions):")
        for ex in extracted_defs:
            print(f"  - {ex}")
        
        # Calculate matches
        matches = 0
        for gt in ground_truth_defs:
            if any(gt in ex or ex in gt for ex in extracted_defs):
                matches += 1
        
        recall = matches / len(ground_truth_defs) if ground_truth_defs else 0
        precision = matches / len(extracted_defs) if extracted_defs else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        print(f"\nMetrics:")
        print(f"  Recall: {recall:.1%} ({matches}/{len(ground_truth_defs)})")
        print(f"  Precision: {precision:.1%} ({matches}/{len(extracted_defs)})")
        print(f"  F1: {f1:.1%}")
        
        results.append({
            'note': note_id,
            'f1': f1,
            'recall': recall,
            'precision': precision
        })
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY: Generalization Analysis")
    print("=" * 70)
    
    avg_f1 = sum(r['f1'] for r in results) / len(results)
    
    print(f"\nPer-Note F1 Scores:")
    for r in results:
        marker = "📍" if r['note'] == 'hist_001' else "  "
        print(f"{marker} {r['note']}: {r['f1']:.1%}")
    
    print(f"\n{'='*70}")
    print(f"History Average F1: {avg_f1:.1%}")
    print(f"Previous (v0.3.1): 21.8%")
    print(f"Improvement: +{(avg_f1 - 0.218)*100:.1f} percentage points")
    print('='*70)
    
    # Overfitting check
    hist_001_f1 = [r['f1'] for r in results if r['note'] == 'hist_001'][0]
    other_avg = sum(r['f1'] for r in results if r['note'] != 'hist_001') / 4
    
    print(f"\nOVERFITTING CHECK:")
    print(f"  hist_001 (tuned on): {hist_001_f1:.1%}")
    print(f"  Other 4 notes avg: {other_avg:.1%}")
    print(f"  Gap: {abs(hist_001_f1 - other_avg)*100:.1f} percentage points")
    
    if abs(hist_001_f1 - other_avg) < 0.15:
        print("  ✅ GOOD GENERALIZATION - Patterns work across notes!")
    elif abs(hist_001_f1 - other_avg) < 0.25:
        print("  ⚠️  SOME OVERFITTING - But patterns still useful")
    else:
        print("  ❌ SEVERE OVERFITTING - Patterns memorized hist_001")
    
    print('='*70)
    
    # Target check
    if avg_f1 >= 0.70:
        print("\n🎉 TARGET ACHIEVED! Average F1 ≥ 70%!")
    elif avg_f1 >= 0.60:
        print("\n⚠️  CLOSE! Average F1 ≥ 60%, almost at 70% target")
    else:
        print(f"\n❌ Below target. Need more pattern refinement.")
    
    print('='*70)


if __name__ == "__main__":
    test_all_history_notes()