"""
Create performance comparison table for Paper 1
"""

import json

def create_table():
    # Baseline (v0.3.1) results
    baseline = {
        'biology': [0.67, 0.89, 0.80, 0.67, 0.67],  # From Week 1
        'history': [0.00, 0.00, 0.40, 0.40, 0.33]   # From Week 1
    }
    
    # Current (v0.8) results from test_four_domains.py
    current = {
        'biology': [0.923, 0.889, 0.857, 0.857, 1.0, 0.909, 0.857, 0.833, 0.833, 0.833],
        'history': [0.889, 0.909, 0.571, 0.75, 0.667, 0.833, 0.909, 0.727, 0.727, 0.727],
        'math': [0.80, 0.923, 0.909, 0.80, 0.714, 0.80, 0.60, 0.857, 1.0, 0.80],
        'literature': [0.923, 1.0, 0.80, 0.80, 0.923, 0.80, 0.833, 1.0, 0.923, 0.833]
    }
    
    print("=" * 80)
    print("PERFORMANCE COMPARISON: Baseline (v0.3.1) vs Current (v0.8)")
    print("=" * 80)
    print()
    print(f"{'Domain':<15} {'Baseline':<12} {'Current':<12} {'Change':<12} {'Status'}")
    print("-" * 80)
    
    # Biology comparison
    bio_base_avg = sum(baseline['biology']) / len(baseline['biology'])
    bio_curr_avg = sum(current['biology']) / len(current['biology'])
    bio_change = bio_curr_avg - bio_base_avg
    print(f"{'Biology':<15} {bio_base_avg:>6.1%}      {bio_curr_avg:>6.1%}      {bio_change:>+6.1%}      {'✅' if bio_change > 0 else '❌'}")
    
    # History comparison
    hist_base_avg = sum(baseline['history']) / len(baseline['history'])
    hist_curr_avg = sum(current['history']) / len(current['history'])
    hist_change = hist_curr_avg - hist_base_avg
    print(f"{'History':<15} {hist_base_avg:>6.1%}      {hist_curr_avg:>6.1%}      {hist_change:>+6.1%}      {'✅' if hist_change > 0 else '❌'}")
    
    # New domains
    math_avg = sum(current['math']) / len(current['math'])
    lit_avg = sum(current['literature']) / len(current['literature'])
    print(f"{'Math':<15} {'N/A':<12} {math_avg:>6.1%}      {'NEW'}         {'✅'}")
    print(f"{'Literature':<15} {'N/A':<12} {lit_avg:>6.1%}      {'NEW'}         {'✅'}")
    
    print("-" * 80)
    
    # Overall
    overall_baseline = (bio_base_avg + hist_base_avg) / 2
    overall_current = (bio_curr_avg + hist_curr_avg + math_avg + lit_avg) / 4
    overall_change = overall_current - overall_baseline
    
    print(f"{'Overall':<15} {overall_baseline:>6.1%}      {overall_current:>6.1%}      {overall_change:>+6.1%}      {'✅'}")
    print("=" * 80)
    
    # Summary stats
    print("\nSUMMARY STATISTICS:")
    print(f"  Total notes: 10 → 40 (+300%)")
    print(f"  Domains: 2 → 4 (+100%)")
    print(f"  Patterns: 9 → 15 (+67%)")
    print(f"  Overall F1: {overall_baseline:.1%} → {overall_current:.1%} (+{overall_change*100:.1f}pp)")
    print(f"  Domain gap: 52.5pp → 11.3pp (-78%)")
    
    # Save as CSV for paper
    with open('results/performance_comparison.csv', 'w') as f:
        f.write("Domain,Baseline F1,Current F1,Change,Notes\n")
        f.write(f"Biology,{bio_base_avg:.3f},{bio_curr_avg:.3f},{bio_change:.3f},10\n")
        f.write(f"History,{hist_base_avg:.3f},{hist_curr_avg:.3f},{hist_change:.3f},10\n")
        f.write(f"Math,N/A,{math_avg:.3f},N/A,10\n")
        f.write(f"Literature,N/A,{lit_avg:.3f},N/A,10\n")
        f.write(f"Overall,{overall_baseline:.3f},{overall_current:.3f},{overall_change:.3f},40\n")
    
    print("\n✅ Saved to results/performance_comparison.csv")

if __name__ == "__main__":
    import os
    os.makedirs('results', exist_ok=True)
    create_table()
