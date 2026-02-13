"""
Create heatmap data showing performance across all notes
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def create_heatmap():
    processor = UnifiedProcessor()
    
    domains = {
        'Biology': ['bio_001', 'bio_002', 'bio_003', 'bio_004', 'bio_005',
                    'bio_006', 'bio_007', 'bio_008', 'bio_009', 'bio_010'],
        'History': ['hist_001', 'hist_002', 'hist_003', 'hist_004', 'hist_005',
                   'hist_006', 'hist_007', 'hist_008', 'hist_009', 'hist_010'],
        'Math': ['math_001', 'math_002', 'math_003', 'math_004', 'math_005',
                'math_006', 'math_007', 'math_008', 'math_009', 'math_010'],
        'Literature': ['lit_001', 'lit_002', 'lit_003', 'lit_004', 'lit_005',
                      'lit_006', 'lit_007', 'lit_008', 'lit_009', 'lit_010']
    }
    
    print("=" * 70)
    print("PER-NOTE PERFORMANCE HEATMAP")
    print("=" * 70)
    
    # Header
    print(f"\n{'Domain':<12} ", end='')
    for i in range(1, 11):
        print(f"{i:>6}", end='')
    print(f"  {'Avg':>6}")
    print("-" * 70)
    
    heatmap_data = []
    
    for domain, notes in domains.items():
        scores = []
        print(f"{domain:<12} ", end='')
        
        for note_id in notes:
            try:
                with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
                    text = f.read()
                with open(f'data/research_dataset/annotations/{note_id}.json', 'r') as f:
                    annotation = json.load(f)
                
                extracted = processor.structure_note(text)
                
                gt = [d['term'].lower() for d in annotation['ground_truth']['definitions']]
                ex = [d['term'].lower() for d in extracted['definitions']]
                
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
                
                scores.append(f1)
                
                # Color code: Green ≥80%, Yellow 60-80%, Red <60%
                if f1 >= 0.80:
                    symbol = "🟩"
                elif f1 >= 0.60:
                    symbol = "🟨"
                else:
                    symbol = "🟥"
                
                print(f"{f1*100:>5.0f}{symbol}", end='')
                
            except FileNotFoundError:
                print("   -- ", end='')
                scores.append(0)
        
        avg = sum(scores) / len(scores) if scores else 0
        print(f"  {avg*100:>5.1f}%")
        
        heatmap_data.append({
            'domain': domain,
            'scores': scores,
            'average': avg
        })
    
    print("=" * 70)
    print("\nLegend: 🟩 ≥80%  🟨 60-80%  🟥 <60%")
    
    # Save CSV
    with open('results/heatmap_data.csv', 'w') as f:
        f.write("Domain," + ",".join([f"Note_{i}" for i in range(1,11)]) + ",Average\n")
        for row in heatmap_data:
            f.write(f"{row['domain']},")
            f.write(",".join([f"{s:.3f}" for s in row['scores']]))
            f.write(f",{row['average']:.3f}\n")
    
    print("\n✅ Saved to results/heatmap_data.csv")

if __name__ == "__main__":
    create_heatmap()
