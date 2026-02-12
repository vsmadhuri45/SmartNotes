"""
Test relationship extraction on actual dataset
"""

from src.note_processor.unified_processor import UnifiedProcessor
from src.note_processor.relationship_extractor import RelationshipExtractor
import json

def test_on_dataset():
    processor = UnifiedProcessor()
    rel_extractor = RelationshipExtractor()
    
    # Test on a few notes from each domain
    test_notes = ['bio_001', 'hist_001', 'math_001', 'lit_001']
    
    print("=" * 70)
    print("RELATIONSHIP EXTRACTION: Real Notes Test")
    print("=" * 70)
    
    total_relationships = 0
    
    for note_id in test_notes:
        print(f"\n{'='*70}")
        print(f"Note: {note_id}")
        print('='*70)
        
        # Read note
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        # Extract definitions first
        result = processor.structure_note(text)
        definitions = result['definitions']
        
        print(f"\nFound {len(definitions)} definitions")
        
        # Extract relationships
        relationships = rel_extractor.extract_relationships(text, definitions)
        
        print(f"Found {len(relationships)} relationships:\n")
        
        for rel in relationships:
            print(f"  {rel['source']} --[{rel['type']}]--> {rel['target']}")
            print(f"  Confidence: {rel['confidence']:.0%}")
        
        total_relationships += len(relationships)
    
    print("\n" + "="*70)
    print(f"TOTAL: {total_relationships} relationships across {len(test_notes)} notes")
    print(f"Average: {total_relationships/len(test_notes):.1f} relationships per note")
    print("="*70)
    
    if total_relationships > 0:
        print("\n✅ Relationship extraction working!")
        print("Next steps:")
        print("  1. Add more relationship types (contrast, cause-effect)")
        print("  2. Improve pattern accuracy")
        print("  3. Test on all 40 notes")
    else:
        print("\n⚠️  No relationships found - patterns may need refinement")

if __name__ == "__main__":
    test_on_dataset()
