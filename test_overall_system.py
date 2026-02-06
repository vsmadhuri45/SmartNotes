"""Overall system performance: Biology + History"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def test_overall_performance():
    processor = UnifiedProcessor()
    
    all_notes = [
        'bio_001', 'bio_002', 'bio_003', 'bio_004', 'bio_005',
        'hist_001', 'hist_002', 'hist_003', 'hist_004', 'hist_005'
    ]
    
    print("=" * 70)
    print("OVERALL SYSTEM PERFORMANCE: v0.8 Unified")
    print("=" * 70)
    
    bio_results = []
    hist_results = []
    
    for note_id in all_notes:
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        with open(f'data/research_dataset/annotations/{note_id}.json', 'r') as f:
            annotation = json.load(f)
        
        extracted = processor.structure_note(text)
        
        ground_truth = [d['term'].lower() for d in annotation['ground_truth']['definitions']]
        extracted_defs = [d['term'].lower() for d in extracted['definitions']]
        
        matches = sum(1 for gt in ground_truth if any(gt in ex or ex in gt for ex in extracted_defs))
        recall = matches / len(ground_truth) if ground_truth else 0
        precision = matches / len(extracted_defs) if extracted_defs else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        if 'bio' in note_id:
            bio_results.append(f1)
        else:
            hist_results.append(f1)
    
    bio_avg = sum(bio_results) / len(bio_results)
    hist_avg = sum(hist_results) / len(hist_results)
    overall_avg = (bio_avg + hist_avg) / 2
    
    print(f"\nBiology Average:  {bio_avg:.1%}")
    print(f"History Average:  {hist_avg:.1%}")
    print(f"Overall Average:  {overall_avg:.1%}")
    print(f"\n{'='*70}")
    print("COMPARISON TO BASELINE (v0.3.1):")
    print('='*70)
    print(f"Biology:  74.3% → {bio_avg:.1%} ({(bio_avg-0.743)*100:+.1f}pp)")
    print(f"History:  21.8% → {hist_avg:.1%} ({(hist_avg-0.218)*100:+.1f}pp)")
    print(f"Overall:  48.0% → {overall_avg:.1%} ({(overall_avg-0.480)*100:+.1f}pp)")
    print(f"\nDomain Gap: {abs(bio_avg - hist_avg)*100:.1f}pp")
    
    if abs(bio_avg - hist_avg) < 0.10:
        print("✅ DOMAIN GAP CLOSED! (<10pp)")
    
    print('='*70)

if __name__ == "__main__":
    test_overall_performance()