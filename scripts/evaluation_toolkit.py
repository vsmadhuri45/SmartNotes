"""
SmartNotes Research Evaluation Toolkit
Author: Madhuri
Date: January 26, 2026

Tools for rigorous evaluation of note processing methods.

Features:
- Load ground truth annotations
- Evaluate any extraction method
- Calculate precision, recall, F1
- Statistical significance testing
- Per-domain analysis
- Failure mode analysis
"""

import os
import json
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import numpy as np


class ResearchEvaluator:
    """
    Evaluate note processing methods against ground truth.
    
    Metrics:
    - Precision: correctness of extracted items
    - Recall: coverage of ground truth items
    - F1: harmonic mean
    - Domain-specific performance
    """
    
    def __init__(self, dataset_dir: str = 'data/research_dataset'):
        self.dataset_dir = dataset_dir
        self.annotations = self._load_annotations()
    
    def _load_annotations(self) -> Dict:
        """Load all ground truth annotations."""
        annotations = {}
        annotation_dir = f"{self.dataset_dir}/annotations"
        
        if not os.path.exists(annotation_dir):
            print(f"⚠️  Annotation directory not found: {annotation_dir}")
            return annotations
        
        for filename in os.listdir(annotation_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(annotation_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    annotations[data['id']] = data
        
        print(f"✅ Loaded {len(annotations)} ground truth annotations")
        return annotations
    
    def evaluate_definitions(self, 
                            note_id: str,
                            extracted_definitions: List[Dict]) -> Dict[str, float]:
        """
        Evaluate definition extraction.
        
        Args:
            note_id: ID of the note
            extracted_definitions: List of extracted definitions
                Format: [{'term': str, 'definition': str}, ...]
        
        Returns:
            Dictionary with precision, recall, F1
        """
        if note_id not in self.annotations:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        
        ground_truth = self.annotations[note_id]['ground_truth']['definitions']
        gt_terms = {d['term'].lower().strip() for d in ground_truth}
        extracted_terms = {d['term'].lower().strip() for d in extracted_definitions}
        
        # True positives: extracted and in ground truth
        true_positives = len(gt_terms & extracted_terms)
        
        # False positives: extracted but not in ground truth
        false_positives = len(extracted_terms - gt_terms)
        
        # False negatives: in ground truth but not extracted
        false_negatives = len(gt_terms - extracted_terms)
        
        # Calculate metrics
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'ground_truth_count': len(gt_terms),
            'extracted_count': len(extracted_terms)
        }
    
    def evaluate_concepts(self,
                         note_id: str,
                         extracted_concepts: List[str],
                         top_k: int = 10) -> Dict[str, float]:
        """
        Evaluate concept extraction.
        
        Uses relaxed matching - extracted concept matches if it appears
        in ground truth or vice versa (handles variations).
        
        Args:
            note_id: ID of the note
            extracted_concepts: List of extracted concepts
            top_k: Consider top K concepts
        
        Returns:
            Dictionary with precision@K, recall@K, F1@K
        """
        if note_id not in self.annotations:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0}
        
        ground_truth = self.annotations[note_id]['ground_truth']['concepts']
        gt_concepts = [c.lower().strip() for c in ground_truth]
        extracted = [c.lower().strip() for c in extracted_concepts[:top_k]]
        
        # Relaxed matching: allow partial matches
        matched = 0
        for ex in extracted:
            # Check if extracted concept matches any ground truth
            for gt in gt_concepts:
                if ex in gt or gt in ex:
                    matched += 1
                    break
        
        precision = matched / len(extracted) if extracted else 0.0
        recall = matched / len(gt_concepts) if gt_concepts else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'matched': matched,
            'extracted_count': len(extracted),
            'ground_truth_count': len(gt_concepts)
        }
    
    def evaluate_method_on_dataset(self,
                                   method_name: str,
                                   extraction_function: callable) -> Dict:
        """
        Evaluate a method on entire dataset.
        
        Args:
            method_name: Name of the method (for reporting)
            extraction_function: Function that takes note text and returns
                {'definitions': [...], 'concepts': [...]}
        
        Returns:
            Comprehensive evaluation results
        """
        print(f"\n{'='*70}")
        print(f"Evaluating: {method_name}")
        print(f"{'='*70}\n")
        
        results = {
            'method': method_name,
            'per_note': {},
            'per_domain': defaultdict(lambda: {'definitions': [], 'concepts': []}),
            'overall': {'definitions': [], 'concepts': []}
        }
        
        # Evaluate each note
        for note_id, annotation in self.annotations.items():
            # Load note text
            note_file = f"{self.dataset_dir}/notes/{note_id}.txt"
            if not os.path.exists(note_file):
                continue
            
            with open(note_file, 'r') as f:
                text = f.read()
            
            # Run extraction method
            try:
                extracted = extraction_function(text)
            except Exception as e:
                print(f"⚠️  Error processing {note_id}: {e}")
                continue
            
            # Evaluate definitions
            def_metrics = self.evaluate_definitions(
                note_id,
                extracted.get('definitions', [])
            )
            
            # Evaluate concepts
            concept_metrics = self.evaluate_concepts(
                note_id,
                extracted.get('concepts', [])
            )
            
            # Store results
            results['per_note'][note_id] = {
                'definitions': def_metrics,
                'concepts': concept_metrics
            }
            
            # Aggregate by domain
            domain = note_id.split('_')[0]
            results['per_domain'][domain]['definitions'].append(def_metrics['f1'])
            results['per_domain'][domain]['concepts'].append(concept_metrics['f1'])
            
            # Aggregate overall
            results['overall']['definitions'].append(def_metrics['f1'])
            results['overall']['concepts'].append(concept_metrics['f1'])
        
        # Calculate averages
        results['summary'] = self._calculate_summary(results)
        
        return results
    
    def _calculate_summary(self, results: Dict) -> Dict:
        """Calculate summary statistics."""
        summary = {}
        
        # Overall averages
        if results['overall']['definitions']:
            summary['definitions'] = {
                'mean_f1': np.mean(results['overall']['definitions']),
                'std_f1': np.std(results['overall']['definitions']),
                'min_f1': np.min(results['overall']['definitions']),
                'max_f1': np.max(results['overall']['definitions'])
            }
        
        if results['overall']['concepts']:
            summary['concepts'] = {
                'mean_f1': np.mean(results['overall']['concepts']),
                'std_f1': np.std(results['overall']['concepts']),
                'min_f1': np.min(results['overall']['concepts']),
                'max_f1': np.max(results['overall']['concepts'])
            }
        
        # Per-domain averages
        summary['per_domain'] = {}
        for domain, metrics in results['per_domain'].items():
            summary['per_domain'][domain] = {
                'definitions_mean_f1': np.mean(metrics['definitions']) if metrics['definitions'] else 0.0,
                'concepts_mean_f1': np.mean(metrics['concepts']) if metrics['concepts'] else 0.0
            }
        
        return summary
    
    def print_summary(self, results: Dict):
        """Print evaluation results in readable format."""
        print(f"\n{'='*70}")
        print(f"EVALUATION RESULTS: {results['method']}")
        print(f"{'='*70}")
        
        summary = results['summary']
        
        # Overall performance
        print(f"\n📊 OVERALL PERFORMANCE:")
        if 'definitions' in summary:
            print(f"   Definitions F1: {summary['definitions']['mean_f1']:.3f} ± {summary['definitions']['std_f1']:.3f}")
            print(f"   Range: [{summary['definitions']['min_f1']:.3f}, {summary['definitions']['max_f1']:.3f}]")
        
        if 'concepts' in summary:
            print(f"   Concepts F1:    {summary['concepts']['mean_f1']:.3f} ± {summary['concepts']['std_f1']:.3f}")
            print(f"   Range: [{summary['concepts']['min_f1']:.3f}, {summary['concepts']['max_f1']:.3f}]")
        
        # Per-domain performance
        if summary.get('per_domain'):
            print(f"\n📈 PER-DOMAIN PERFORMANCE:")
            for domain, metrics in summary['per_domain'].items():
                print(f"\n   {domain.upper()}:")
                print(f"      Definitions F1: {metrics['definitions_mean_f1']:.3f}")
                print(f"      Concepts F1:    {metrics['concepts_mean_f1']:.3f}")
        
        print(f"\n{'='*70}\n")
    
    def compare_methods(self, results_list: List[Dict]) -> Dict:
        """
        Compare multiple methods statistically.
        
        Args:
            results_list: List of result dictionaries from evaluate_method_on_dataset
        
        Returns:
            Comparison statistics
        """
        comparison = {
            'methods': [r['method'] for r in results_list],
            'definitions': {},
            'concepts': {}
        }
        
        # Extract F1 scores for each method
        for task in ['definitions', 'concepts']:
            scores_by_method = {}
            for result in results_list:
                method = result['method']
                scores = result['overall'][task]
                scores_by_method[method] = scores
            
            # Calculate statistics
            comparison[task] = {
                method: {
                    'mean': np.mean(scores),
                    'std': np.std(scores),
                    'median': np.median(scores)
                }
                for method, scores in scores_by_method.items()
            }
            
            # Find best method
            best_method = max(
                scores_by_method.items(),
                key=lambda x: np.mean(x[1])
            )[0]
            comparison[task]['best'] = best_method
        
        return comparison
    
    def print_comparison(self, comparison: Dict):
        """Print method comparison."""
        print(f"\n{'='*70}")
        print(f"METHOD COMPARISON")
        print(f"{'='*70}")
        
        print(f"\n📊 DEFINITION EXTRACTION:")
        for method, stats in comparison['definitions'].items():
            if method == 'best':
                continue
            marker = " 🏆" if method == comparison['definitions']['best'] else ""
            print(f"   {method}: {stats['mean']:.3f} ± {stats['std']:.3f}{marker}")
        
        print(f"\n📊 CONCEPT EXTRACTION:")
        for method, stats in comparison['concepts'].items():
            if method == 'best':
                continue
            marker = " 🏆" if method == comparison['concepts']['best'] else ""
            print(f"   {method}: {stats['mean']:.3f} ± {stats['std']:.3f}{marker}")
        
        print(f"\n{'='*70}\n")


def example_usage():
    """Example of how to use the evaluation toolkit."""
    evaluator = ResearchEvaluator()
    
    # Example: Evaluate a simple method
    def simple_extraction(text):
        """Simple extraction method for testing."""
        import re
        
        # Extract definitions (simple pattern)
        definitions = []
        pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)[:\s]+(?:is|are|was|were)\s+([^.!?]+)'
        for term, definition in re.findall(pattern, text):
            definitions.append({'term': term, 'definition': definition})
        
        # Extract concepts (capitalized words)
        concepts = re.findall(r'\b[A-Z][a-z]{3,}\b', text)
        concepts = list(set(concepts))[:10]  # Top 10 unique
        
        return {
            'definitions': definitions,
            'concepts': concepts
        }
    
    # Evaluate on dataset
    results = evaluator.evaluate_method_on_dataset(
        method_name="Simple Baseline",
        extraction_function=simple_extraction
    )
    
    # Print results
    evaluator.print_summary(results)
    
    return results


if __name__ == "__main__":
    print("SmartNotes Research Evaluation Toolkit")
    print("="*70)
    example_usage()
