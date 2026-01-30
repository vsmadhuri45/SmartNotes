# Day 8 Action Plan - Week 2 Begins!

## 🎯 Today's Mission
Fix the history domain gap (22% → 70% F1) by designing history-specific patterns

**Time Budget**: 3-4 hours
**Difficulty**: Medium
**Importance**: HIGH (Foundation for Paper 1)

---

## ✅ Morning Session (90 minutes)

### **Task 1: Deep Analysis of hist_001 Failure** (45 min)

**What to do**:
```bash
cd ~/Documents/SmartNotes

# 1. Review the note again
cat data/research_dataset/notes/hist_001.txt

# 2. Review ground truth
cat data/research_dataset/annotations/hist_001.json

# 3. Create analysis document
touch docs/hist_001_failure_analysis.md
```

**In the analysis document, answer**:
1. What definitions exist in the note?
   - List all 4 from ground truth
   - Note their format (how they're written)

2. Why did v0.3.1 miss them?
   - Which patterns should have caught them?
   - What specifically broke?

3. What did v0.3.1 extract instead?
   - Run the processor manually
   - See what 6 things it found
   - Why are they wrong?

**Code to run**:
```python
# Quick test script
from src.note_processor.enhanced_processor import EnhancedNoteProcessor

processor = EnhancedNoteProcessor()

with open('data/research_dataset/notes/hist_001.txt', 'r') as f:
    text = f.read()

result = processor.structure_note(text)

print("FOUND DEFINITIONS:")
for d in result['definitions']:
    print(f"  - {d['term']}: {d['definition'][:50]}...")

print("\nGROUND TRUTH:")
print("  - French Revolution")
print("  - Estates-General")
print("  - Declaration of the Rights of Man")
print("  - Reign of Terror")
```

**Expected insight**: Patterns fail because of "The" prefix!

---

### **Task 2: Design History-Specific Patterns** (45 min)

**What to do**:
Create a new file: `docs/history_patterns_design.md`

**Document these new patterns**:

**Pattern 8: "The X was/were Y"**
```python
# For: "The French Revolution was a period..."
pattern8 = r'(?:The|the)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an)?\s*([^.!?]+)'

# Matches:
# - "The French Revolution was a period of radical change"
# - "The Reign of Terror was a period of extreme violence"
```

**Pattern 9: "The X: definition"**
```python
# For: "The Estates-General: representative assembly..."
pattern9 = r'(?:The|the)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]+)'

# Matches:
# - "The Estates-General: representative assembly"
# - "The Bastille: fortress and prison"
```

**Pattern 10: Multi-word proper noun definitions**
```python
# For: "Declaration of the Rights of Man: document..."
pattern10 = r'([A-Z][a-z]+(?:\s+(?:of|the|and|in)\s+[A-Z][a-z]+)+):\s+([^.!?\n]+)'

# Matches:
# - "Declaration of the Rights of Man: document proclaiming..."
# - "Battle of the Bulge: major German offensive"
```

**Test each pattern**:
```python
import re

text = "The French Revolution was a period of radical change in France."

pattern = r'(?:The|the)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an)?\s*([^.!?]+)'

matches = re.findall(pattern, text)
print(matches)
# Should print: [('French Revolution', 'period of radical change in France')]
```

---

## ✅ Afternoon Session (90 minutes)

### **Task 3: Implement New Patterns** (60 min)

**What to do**:
Create `src/note_processor/history_processor.py`

```python
"""
History-Specific Note Processor
Version: 0.5
Date: Day 8

Adds history-specific patterns to handle:
- "The X was Y" format
- Multi-word historical terms
- Proper nouns with articles
"""

import re
from src.note_processor.enhanced_processor import EnhancedNoteProcessor


class HistoryProcessor(EnhancedNoteProcessor):
    """Enhanced processor with history-specific patterns."""
    
    def extract_definitions(self, text):
        """
        Extract definitions with HISTORY-SPECIFIC patterns added.
        
        New patterns (8-10) handle:
        - "The X was/were Y"
        - "The X: definition"
        - Multi-word proper nouns
        """
        # Get base definitions from parent class
        definitions = super().extract_definitions(text)
        
        # Pattern 8: "The X was/were Y"
        pattern8 = r'(?:The|the)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:was|were)\s+(?:a|an)?\s*([^.!?]+)'
        matches8 = re.findall(pattern8, text)
        for term, definition in matches8:
            # Check if not already found
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'history_was_were'
                })
        
        # Pattern 9: "The X: definition"
        pattern9 = r'(?:The|the)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*):\s+([^.!?\n]{10,})'
        matches9 = re.findall(pattern9, text)
        for term, definition in matches9:
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'history_colon_with_article'
                })
        
        # Pattern 10: Multi-word with connectors
        pattern10 = r'([A-Z][a-z]+(?:\s+(?:of|the|and|in)\s+(?:the\s+)?[A-Z][a-z]+)+):\s+([^.!?\n]{10,})'
        matches10 = re.findall(pattern10, text)
        for term, definition in matches10:
            if not any(d['term'].lower() == term.lower() for d in definitions):
                definitions.append({
                    'term': term.strip(),
                    'definition': definition.strip(),
                    'pattern': 'history_multiword'
                })
        
        return definitions


def test_history_processor():
    """Test the history processor on hist_001."""
    processor = HistoryProcessor()
    
    with open('data/research_dataset/notes/hist_001.txt', 'r') as f:
        text = f.read()
    
    result = processor.structure_note(text)
    
    print("HISTORY PROCESSOR TEST")
    print("=" * 60)
    print(f"Found {len(result['definitions'])} definitions:")
    for d in result['definitions']:
        print(f"\n{d['term']}")
        print(f"  Definition: {d['definition'][:60]}...")
        print(f"  Pattern: {d['pattern']}")
    
    print("\n" + "=" * 60)
    print("GROUND TRUTH (should find all 4):")
    print("  1. French Revolution")
    print("  2. Estates-General")
    print("  3. Declaration of the Rights of Man")
    print("  4. Reign of Terror")


if __name__ == "__main__":
    test_history_processor()
```

**Run the test**:
```bash
python src/note_processor/history_processor.py
```

**Expected output**:
```
HISTORY PROCESSOR TEST
============================================================
Found 4+ definitions:

French Revolution
  Definition: a period of radical political and social change in France...
  Pattern: history_was_were

Estates-General
  Definition: representative assembly with three estates...
  Pattern: history_colon_with_article

Declaration of the Rights of Man
  Definition: document proclaiming liberty, equality, and fraternity...
  Pattern: history_multiword

Reign of Terror
  Definition: a period of extreme violence from 1793-1794...
  Pattern: history_was_were
```

**Success**: Should find all 4 definitions! ✅

---

### **Task 4: Evaluate Improvement** (30 min)

**What to do**:
Test on ALL 5 history notes

```python
# Create test_history_improvement.py

from src.note_processor.history_processor import HistoryProcessor
from scripts.evaluation_toolkit import ResearchEvaluator

def evaluate_history_only():
    """Test history processor on history notes only."""
    processor = HistoryProcessor()
    evaluator = ResearchEvaluator()
    
    # Test on history notes only
    history_notes = ['hist_001', 'hist_002', 'hist_003', 'hist_004', 'hist_005']
    
    results = []
    for note_id in history_notes:
        with open(f'data/research_dataset/notes/{note_id}.txt', 'r') as f:
            text = f.read()
        
        extracted = processor.structure_note(text)
        metrics = evaluator.evaluate_definitions(note_id, extracted['definitions'], evaluator.annotations)
        
        print(f"{note_id}: F1 = {metrics['f1']:.1%}")
        results.append(metrics['f1'])
    
    print(f"\nHistory Average: {sum(results)/len(results):.1%}")
    print(f"Previous: 21.8%")
    print(f"Improvement: +{(sum(results)/len(results) - 0.218)*100:.1f} percentage points")

if __name__ == "__main__":
    evaluate_history_only()
```

**Run it**:
```bash
python test_history_improvement.py
```

**Target**: 
- Previous: 21.8% F1
- Target: 70% F1
- Improvement: +48 percentage points! 🎉

---

## ✅ Evening Session (Optional 30 min)

### **Task 5: Document Today's Progress**

Create `docs/DAY8_PROGRESS.md`:

```markdown
# Day 8 Progress Report

## ✅ Accomplished Today

1. **Deep Analysis**: Identified why hist_001 failed (0% F1)
   - Root cause: "The X was Y" format not handled
   - Patterns expect "X was Y" without article

2. **Pattern Design**: Created 3 new history-specific patterns
   - Pattern 8: "The X was/were Y"
   - Pattern 9: "The X: definition"  
   - Pattern 10: Multi-word proper nouns

3. **Implementation**: Built HistoryProcessor (v0.5)
   - Extends EnhancedNoteProcessor
   - Adds history-specific patterns
   - Tested on hist_001

4. **Results**: 
   - hist_001: 0% → XX% F1 (HUGE improvement!)
   - History average: 21.8% → XX% F1
   - Improvement: +XX percentage points

## 🎯 Impact on Project

**Week 2 Goal**: Fix domain gap ✅ (on track!)
**Paper 1**: Foundation strengthened
**Learning**: Domain-specific patterns are essential

## 📝 Tomorrow (Day 9)

1. Test on all 10 history notes (if collected more)
2. Fine-tune patterns based on results
3. Start planning domain classifier
4. Document pattern library

## 💡 Insights

- History domain has unique linguistic patterns
- Article prefixes ("The") are common in history
- Multi-word proper nouns need special handling
- Simple pattern additions can close huge gaps!

---

**Time spent**: X hours
**Energy level**: High/Medium/Low
**Confidence**: Improving!
```

---

## 📊 Success Metrics for Day 8

### **Must Achieve**:
- [ ] Analyzed hist_001 failure
- [ ] Designed 3 new patterns
- [ ] Implemented HistoryProcessor
- [ ] Tested on hist_001
- [ ] Documented progress

### **Target Metrics**:
- [ ] hist_001: 0% → 60%+ F1
- [ ] History average: 22% → 50%+ F1
- [ ] All 4 hist_001 definitions found

### **Stretch Goals**:
- [ ] History average: 70%+ F1
- [ ] Test on all 5 history notes
- [ ] Start domain classifier design

---

## 🎯 End of Day Checklist

Before you stop for the day:

- [ ] Committed code to Git
- [ ] Updated DAY8_PROGRESS.md
- [ ] Tested all code (no broken tests)
- [ ] Planned Day 9 tasks
- [ ] Celebrated progress! 🎉

---

## 💡 Tips for Success Today

1. **Start with analysis** - Don't jump to coding
2. **Test patterns in isolation** - Use regex testers
3. **Document as you go** - Write down insights
4. **Test frequently** - Run code every 15 minutes
5. **Take breaks** - 3-4 hours is a lot!

---

## 🚨 If You Get Stuck

**Problem**: Patterns not matching
→ Test patterns on regex101.com first

**Problem**: Code errors
→ Start with simpler version, add complexity

**Problem**: Not sure if working
→ Print intermediate results, check manually

**Problem**: Taking too long
→ It's OK! This is learning. Document what's hard.

---

## 🎉 Celebrate Small Wins

- ✅ Identified the problem → Victory!
- ✅ Designed patterns → Victory!
- ✅ Code compiles → Victory!
- ✅ First test passes → Victory!
- ✅ Found 1 definition → Victory!

**Every step forward counts!**

---

**GOOD LUCK ON DAY 8!** 🚀

You're about to close a 48-point gap with clever engineering. That's real research impact!

**See you tomorrow for Day 9!**
