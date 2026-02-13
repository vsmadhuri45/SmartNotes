"""
Analyze which patterns are catching which definitions
"""

from src.note_processor.unified_processor import UnifiedProcessor
import json
from collections import Counter

def analyze_patterns():
    processor = UnifiedProcessor()
    
    all_notes = []
    for domain in ['bio', 'hist', 'math', 'lit']:
        for i in range(1, 11):
            all_notes.append(f'{domain}_{i:03d}')
    
    pattern_counts = Counter()
    pattern_by_domain = {
        'biology': Counter(),
        'history': Counter(),
        'math': Counter(),
        'literature': Counter()
    }
    
    print("=" * 70)
    print("PATTERN USAGE ANALYSIS")
    print("=" * 70)
    
    for note_id in all_notes:
        try:
            with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
                text = f.read()
            
            result = processor.structure_note(text)
            
            # Get domain
            domain = 'biology' if 'bio' in note_id else \
                    'history' if 'hist' in note_id else \
                    'math' if 'math' in note_id else 'literature'
            
            for defn in result['definitions']:
                pattern = defn.get('pattern', 'unknown')
                pattern_counts[pattern] += 1
                pattern_by_domain[domain][pattern] += 1
        
        except FileNotFoundError:
            pass
    
    print("\nOVERALL PATTERN USAGE:")
    print("-" * 70)
    for pattern, count in pattern_counts.most_common():
        pct = count / sum(pattern_counts.values()) * 100
        print(f"  {pattern:<25} {count:>4} definitions ({pct:>5.1f}%)")
    
    print(f"\n  {'TOTAL':<25} {sum(pattern_counts.values()):>4} definitions")
    
    print("\n" + "=" * 70)
    print("PATTERN USAGE BY DOMAIN:")
    print("=" * 70)
    
    for domain, counts in pattern_by_domain.items():
        if counts:
            print(f"\n{domain.upper()}:")
            total = sum(counts.values())
            for pattern, count in counts.most_common():
                pct = count / total * 100
                print(f"  {pattern:<25} {count:>3} ({pct:>5.1f}%)")
    
    # Save results
    with open('results/pattern_usage.csv', 'w') as f:
        f.write("Pattern,Count,Percentage\n")
        for pattern, count in pattern_counts.most_common():
            pct = count / sum(pattern_counts.values()) * 100
            f.write(f"{pattern},{count},{pct:.1f}\n")
    
    print("\n✅ Saved to results/pattern_usage.csv")

if __name__ == "__main__":
    analyze_patterns()
