# Critical Issues to Fix

## 🔴 P0 - Must Fix for Week 2

### Issue #1: Definition Detection Failure (0% accuracy)
**Impact**: High - definitions are core to learning
**Current**: Only catches 3 patterns
**Need**: 
- "X is/are Y"
- "X was/were Y"  
- "X is given by Y"
- "X is known as Y"
- "X can be defined as Y"

**Test cases**:
- "Russia was an autocracy" ✗
- "nth term is given by..." ✗
- "Amphibians are species that..." ✗

### Issue #2: Concept Extraction Quality (20% success)
**Impact**: High - extracts wrong concepts
**Current**: Frequency-based word counting
**Problems**:
- Extracts common words ("Over", "There", "First")
- Breaks multi-word concepts ("Bingle Bog Once")
- Ignores proper nouns and entities

**Solution**: Use spaCy for NLP
```python
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
entities = [ent.text for ent in doc.ents]  # Proper nouns
noun_chunks = [chunk.text for chunk in doc.noun_chunks]  # Multi-word
```

### Issue #3: Formula Detection (0% success)
**Impact**: Critical for STEM notes
**Current**: Formulas completely ignored
**Examples missed**:
- an = a + (n – 1)d
- Sn = n/2[2a + (n – 1)d]

**Solution**: Regex for math patterns
```python
formula_pattern = r'[a-zA-Z]+\s*=\s*[^.!?\n]+'
```

### Issue #4: Note Classification (33% accuracy)
**Impact**: Medium - affects template selection
**Wrong classifications**:
- Story → "Procedural" (should be "Narrative")
- History → "General" (should be "Factual")

**Solution**: Better keyword indicators, consider sentence structure

## 🟡 P1 - Should Fix Soon

### Issue #5: Web Text Cleaning
- Remove navigation text, ads, language fragments
- Implement text cleaning pre-processor

### Issue #6: Multi-word Concept Handling
- "Bingle Bog" split into "Bingle" and "Bog"
- Need proper noun phrase extraction

### Issue #7: Stop Words Too Aggressive
- Removing important small words
- Need domain-specific stop word lists

## 🟢 P2 - Nice to Have

### Issue #8: Output Formatting
- Could be prettier with colors, sections
- Add confidence scores

### Issue #9: Example Detection Limited
- Only finds "for example", "e.g.", "such as"
- Could detect more example patterns

### Issue #10: No Summary Generation
- Should create a brief summary of the note