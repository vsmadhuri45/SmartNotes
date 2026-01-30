"""
Evaluate v0.3.1 System on Research Dataset
Day 4: Baseline Evaluation

This script tests your proven v0.3.1 system (92% from Day 2)
on the new research dataset to get baseline metrics.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.evaluation_toolkit import ResearchEvaluator
from src.note_processor.enhanced_processor import EnhancedNoteProcessor


def extract_with_v031(text):
    """
    Extract using v0.3.1 processor.
    
    This is your proven system from Day 2 that achieved:
    - 92% recall on definitions
    - 85% precision on definitions
    """
    processor = EnhancedNoteProcessor()
    result = processor.structure_note(text)
    
    return {
        'definitions': result['definitions'],
        'concepts': result['key_concepts']
    }


def main():
    print("=" * 70)
    print("DAY 4: Evaluating v0.3.1 on Research Dataset")
    print("=" * 70)
    print()
    print("System: v0.3.1 (Rule-based with 9 patterns)")
    print("Dataset: 10 notes (5 biology, 5 history)")
    print("Metrics: Precision, Recall, F1-Score")
    print()
    
    # Initialize evaluator
    evaluator = ResearchEvaluator(dataset_dir='data/research_dataset')
    
    # Evaluate v0.3.1 system
    print("Running evaluation... (this may take 10-20 seconds)")
    print()
    
    results = evaluator.evaluate_method_on_dataset(
        method_name="v0.3.1 Rule-based (Day 2)",
        extraction_function=extract_with_v031
    )
    
    # Print detailed results
    evaluator.print_summary(results)
    
    # Print per-note breakdown
    print("\n" + "=" * 70)
    print("PER-NOTE RESULTS:")
    print("=" * 70)
    
    for note_id, metrics in results['per_note'].items():
        print(f"\n{note_id}:")
        print(f"  Definitions - P: {metrics['definitions']['precision']:.3f}, "
              f"R: {metrics['definitions']['recall']:.3f}, "
              f"F1: {metrics['definitions']['f1']:.3f}")
        print(f"  Concepts    - P: {metrics['concepts']['precision']:.3f}, "
              f"R: {metrics['concepts']['recall']:.3f}, "
              f"F1: {metrics['concepts']['f1']:.3f}")
        print(f"  Ground truth: {metrics['definitions']['ground_truth_count']} definitions, "
              f"{metrics['concepts']['ground_truth_count']} concepts")
        print(f"  Extracted:    {metrics['definitions']['extracted_count']} definitions, "
              f"{metrics['concepts']['extracted_count']} concepts")
    
    # Summary for documentation
    print("\n" + "=" * 70)
    print("SUMMARY FOR DOCUMENTATION:")
    print("=" * 70)
    summary = results['summary']
    
    print(f"\n📊 DEFINITION EXTRACTION:")
    if 'definitions' in summary:
        print(f"   Mean F1:  {summary['definitions']['mean_f1']:.1%}")
        print(f"   Std Dev:  {summary['definitions']['std_f1']:.3f}")
        print(f"   Range:    {summary['definitions']['min_f1']:.1%} - {summary['definitions']['max_f1']:.1%}")
    
    print(f"\n📊 CONCEPT EXTRACTION:")
    if 'concepts' in summary:
        print(f"   Mean F1:  {summary['concepts']['mean_f1']:.1%}")
        print(f"   Std Dev:  {summary['concepts']['std_f1']:.3f}")
        print(f"   Range:    {summary['concepts']['min_f1']:.1%} - {summary['concepts']['max_f1']:.1%}")
    
    print(f"\n📊 BY DOMAIN:")
    for domain, metrics in summary['per_domain'].items():
        print(f"   {domain.upper()}:")
        print(f"      Definitions F1: {metrics['definitions_mean_f1']:.1%}")
        print(f"      Concepts F1:    {metrics['concepts_mean_f1']:.1%}")
    
    print("\n" + "=" * 70)
    print("✅ Evaluation complete!")
    print("=" * 70)
    
    # Save results to file
    import json
    output_file = 'results/day4_v031_baseline.json'
    os.makedirs('results', exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump({
            'method': 'v0.3.1',
            'date': '2026-01-27',
            'dataset': 'research_dataset_v1.0',
            'summary': summary,
            'per_note': {
                note_id: {
                    'definitions': {
                        'precision': m['definitions']['precision'],
                        'recall': m['definitions']['recall'],
                        'f1': m['definitions']['f1']
                    },
                    'concepts': {
                        'precision': m['concepts']['precision'],
                        'recall': m['concepts']['recall'],
                        'f1': m['concepts']['f1']
                    }
                }
                for note_id, m in results['per_note'].items()
            }
        }, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    print()


if __name__ == "__main__":
    main()
