"""
Test the 2 problem notes specifically
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def test_problem_notes():
    processor = UnifiedProcessor()
    
    problem_notes = [
        ('hist_003', 57.1, "Industrial Revolution"),
        ('math_007', 60.0, "Number Theory")
    ]
    
    print("=" * 70)
    print("TESTING PROBLEM NOTES: hist_003 and math_007")
    print("=" * 70)
    
    for note_id, old_f1, title in problem_notes:
        print(f"\n{'='*70}")
        print(f"{note_id} ({title}) - Was: {old_f1:.1f}%")
        print('='*70)
        
        # Read note and annotation
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        with open(f'data/research_dataset/annotations/{note_id}.json', 'r') as f:
            annotation = json.load(f)
        
        # Extract
        result = processor.structure_note(text)
        
        gt = [d['term'].lower() for d in annotation['ground_truth']['definitions']]
        ex = [d['term'].lower() for d in result['definitions']]
        
        # Calculate F1
        matched_gt = set()
        matched_ex = set()
        for i, g in enumerate(gt):
            for j, e in enumerate(ex):
                if g in e or e in g:
                    if i not in matched_gt and j not in matched_ex:
                        matched_gt.add(i)
                        matched_ex.add(j)
                        break
        
        matches = len(matched_gt)
        recall = matches / len(gt) if gt else 0
        precision = matches / len(ex) if ex else 0
        f1 = 2*(precision*recall)/(precision+recall) if (precision+recall) > 0 else 0
        
        print(f"\nGround truth: {len(gt)} definitions")
        print(f"Extracted: {len(ex)} definitions")
        print(f"Matches: {matches}")
        print(f"\nRecall: {recall:.1%}")
        print(f"Precision: {precision:.1%}")
        print(f"F1: {f1:.1%}")
        
        change = f1 - (old_f1/100)
        if f1 >= 0.70:
            print(f"\n✅ FIXED! {old_f1:.1f}% → {f1:.1%} ({change*100:+.1f}pp)")
        else:
            print(f"\n⚠️  Still below target: {old_f1:.1f}% → {f1:.1%} ({change*100:+.1f}pp)")
        
        # Show what was caught
        print(f"\nExtracted terms:")
        for d in result['definitions']:
            status = "✅" if any(d['term'].lower() in g or g in d['term'].lower() for g in gt) else "❌"
            print(f"  {status} {d['term']} (pattern: {d['pattern']})")

if __name__ == "__main__":
    test_problem_notes()
