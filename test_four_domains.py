"""
Test UnifiedProcessor on ALL 4 domains
Week 3 - Cross-domain expansion test
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json

def test_four_domains():
    processor = UnifiedProcessor()
    
    domains = {
        'biology': ['bio_001', 'bio_002', 'bio_003', 'bio_004', 'bio_005', 'bio_006', 'bio_007', 'bio_008', 'bio_009', 'bio_010'],
        'history': ['hist_001', 'hist_002', 'hist_003', 'hist_004', 'hist_005', 'hist_006', 'hist_007', 'hist_008', 'hist_009', 'hist_010'],
        'math':    ['math_001', 'math_002', 'math_003', 'math_004', 'math_005', 'math_006', 'math_007', 'math_008', 'math_009', 'math_010'],
        'literature': ['lit_001', 'lit_002', 'lit_003', 'lit_004', 'lit_005', 'lit_006', 'lit_007', 'lit_008', 'lit_009', 'lit_010']
    }
    
    print("=" * 70)
    print("4-DOMAIN TEST: UnifiedProcessor v0.8")
    print("Week 3 - Cross-domain expansion")
    print("=" * 70)
    
    domain_averages = {}
    
    for domain, notes in domains.items():
        print(f"\n{'='*70}")
        print(f"DOMAIN: {domain.upper()}")
        print('='*70)
        
        results = []
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
                
                print(f"  {note_id}: {f1:.1%} F1 (P:{precision:.1%} R:{recall:.1%})")
                results.append(f1)
                
            except FileNotFoundError:
                print(f"  {note_id}: FILE NOT FOUND")
        
        if results:
            avg = sum(results) / len(results)
            domain_averages[domain] = avg
            print(f"\n  {domain.upper()} AVERAGE: {avg:.1%}")
    
    # Summary
    print("\n" + "="*70)
    print("CROSS-DOMAIN SUMMARY")
    print("="*70)
    
    baseline = {'biology': 0.743, 'history': 0.218, 'math': 0, 'literature': 0}
    
    for domain, avg in domain_averages.items():
        base = baseline.get(domain, 0)
        change = f"(+{(avg-base)*100:.1f}pp from baseline)" if base > 0 else "(NEW DOMAIN)"
        print(f"  {domain.capitalize():<12}: {avg:.1%} {change}")
    
    if domain_averages:
        overall = sum(domain_averages.values()) / len(domain_averages)
        print(f"\n  Overall Average: {overall:.1%}")
        
        max_d = max(domain_averages, key=domain_averages.get)
        min_d = min(domain_averages, key=domain_averages.get)
        gap = domain_averages[max_d] - domain_averages[min_d]
        
        print(f"\n  Best Domain:  {max_d} ({domain_averages[max_d]:.1%})")
        print(f"  Worst Domain: {min_d} ({domain_averages[min_d]:.1%})")
        print(f"  Domain Gap:   {gap*100:.1f}pp")
        
        print(f"\n  {'='*60}")
        if gap < 0.15:
            print("  ✅ EXCELLENT: All domains performing similarly!")
        elif gap < 0.30:
            print("  ⚠️  GOOD: Some domain variation, investigate lowest")
        else:
            print(f"  ❌ LARGE GAP: {min_d} needs domain-specific patterns!")
        print("="*70)

if __name__ == "__main__":
    test_four_domains()
