# Relationship Types for Knowledge Graph

## Goal
Extract semantic relationships between concepts to build knowledge graph

## Relationship Types (Week 4)

### 1. Prerequisite (is_prerequisite_for)
- "X is needed to understand Y"
- "Before learning X, students must know Y"
- Example: Algebra → Calculus

### 2. Example (is_example_of)
- "X is an example of Y"
- "For instance, X demonstrates Y"
- Example: Mitochondria → Organelles

### 3. Part-Whole (is_part_of)
- "X is part of Y"
- "Y consists of X"
- Example: Neuron → Nervous System

### 4. Contrast (contrasts_with)
- "X differs from Y"
- "Unlike X, Y..."
- Example: DNA vs RNA

### 5. Cause-Effect (causes)
- "X leads to Y"
- "Y results from X"
- Example: Mutation → Evolution

## Implementation Plan

**Week 4 Tasks**:
1. Define patterns for each relationship type
2. Implement extraction in unified_processor
3. Test on 40 notes
4. Evaluate accuracy (target: 70%)

**Week 11-12** (per roadmap):
- Build Neo4j knowledge graph
- Add semantic similarity (BERT)
- Create visualization

## Next Actions
1. Analyze current notes for relationship examples
2. Design regex patterns
3. Test on sample notes
