"""Quick test: Does v0.7 maintain biology performance?"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def test_biology_notes():
    processor = UnifiedProcessor()
    bio_notes = ['bio_001', 'bio_002', 'bio_003', 'bio_004', 'bio_005']
    
    print("=" * 70)
    print("BIOLOGY VALIDATION: v0.8 UnifiedProcessor")
    print("=" * 70)
    print("Testing if history patterns hurt biology performance...\n")
    
    results = []
    for note_id in bio_notes:
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
        
        print(f"{note_id}: {f1:.1%} F1")
        results.append(f1)
    
    avg = sum(results) / len(results)
    print(f"\n{'='*70}")
    print(f"Biology Average: {avg:.1%}")
    print(f"Previous (v0.3.1): 74.3%")
    print(f"Change: {(avg - 0.743)*100:+.1f}pp")
    
    if avg >= 0.70:
        print("✅ MAINTAINED: Biology performance still strong!")
    else:
        print("⚠️ REGRESSION: Biology performance dropped")
    
    print('='*70)
    return avg

if __name__ == "__main__":
    bio_f1 = test_biology_notes()