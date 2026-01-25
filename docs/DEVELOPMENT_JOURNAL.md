# Development Journal

## Purpose
Daily log of development progress, decisions, challenges, and learnings.

---

## Week 1: Foundation & Basic Note Processor

### Day 1 - January 24, 2026 (Continued)

**Additional Testing Completed**:
Tested with 3 different note types:
1. Literature (The Frog and Nightingale) - 1364 words
2. History (Russian Revolution) - 269 words  
3. Math (Arithmetic Progression) - 76 words

**Critical Issues Discovered**:

🔴 **Definition Detection: 0/5+ definitions found across all notes**
- Missed "Russia was an autocracy"
- Missed "nth term is given by..."
- Missed multiple historical definitions
- Current patterns too narrow (only "is defined as", "means", "X:")

🔴 **Concept Extraction: ~20% quality**
- Literature: Got "There", "Said", "Listen" instead of "Nightingale", "Fable"
- History: Got "Over", "But Lenin" (fragments!)
- Math: Got "First", "Given", "Number" (useless math words)
- Frequency-based approach is fundamentally flawed

🔴 **Formula Handling: Complete failure**
- Math formulas (an = a + (n-1)d) completely ignored
- Need special handling for mathematical notation

🔴 **Web Text Pollution**
- Literature note had website navigation mixed in
- Need pre-processing to clean scraped content

🔴 **Note Classification: 33% accuracy**
- Only got math correct (procedural)
- Missed narrative (literature) and factual (history)

**Quantitative Results**:
- Total notes tested: 4
- Definitions detected: 0/12+ (0%)
- Concept quality: 2/10 average
- Classification accuracy: 1/3 (33%)

**Key Insight**: 
The basic frequency-based approach works as a "hello world" but 
reveals fundamental limitations. Need proper NLP (spaCy), better 
pattern matching, and formula detection for Week 2.

**Week 2 Priority Tasks** (based on testing):
1. Fix definition detection - add 5+ new patterns
2. Implement spaCy for proper noun phrase extraction
3. Add formula detection for math notes
4. Improve note type classification
5. Add text cleaning for web-scraped content

---

### Day 2 - January 25, 2026
**Goals**:
- [ ] TBD

**Work Done**:
- TBD

**Technical Decisions**:
- TBD

**Challenges**:
- TBD

**Tomorrow's Plan**:
- TBD

**Notes**:
- TBD

---

## Template for Daily Entry

### Day X - Date
**Goals**:
- [ ] Goal 1
- [ ] Goal 2

**Work Done**:
- What was completed

**Technical Decisions**:
- Key decisions made

**Challenges**:
- Problems encountered
- How they were solved

**Tomorrow's Plan**:
- Next steps

**Notes**:
- Additional observations

---

## Weekly Summary Template

### Week X Summary
**Overall Progress**: X%  
**Major Achievements**:
- Achievement 1
- Achievement 2

**Key Learnings**:
- Learning 1
- Learning 2

**Next Week Focus**:
- Focus area 1
- Focus area 2

### Day 2 - January 25, 2026 ✅ COMPLETE

**Goals**:
- [x] Fix definition detection (Issue #1)
- [x] Improve from 0% to >70%
- [x] Learn about precision/recall trade-offs
- [x] Iterate to find balance

**Work Done - Full Journey**:

**v0.2 - Initial Improvements**:
- Added 7 new definition patterns
- Results: 14/12 (116.7%) 
- Issue: False positives (pronouns, fragments)

**v0.3 - Precision Fix (Too Strict)**:
- Added pronoun filtering
- Added aggressive lowercase filtering
- Results: 4/12 (33.3%) - OVER-FILTERED!
- Lesson: Too strict is worse than too loose

**v0.3.1 - Balanced Approach (FINAL)**:
- Kept pronoun filtering ✅
- Removed aggressive filters ✅
- Simplified math pattern ✅
- Results: 13/12 (108.3% nominal, 92% real)

**Final Testing Results**:
- Biology: 9/8 (8 real + 1 fragment)
- History: 3/2 (2 real + 1 debatable)
- Math: 1/2 (found 1 of 2 formulas!)
- Literature: 0/0 ✅ PERFECT

**Real Performance Metrics**:
- True definitions found: 11/12 (92% recall) ✅
- Precision: 11/13 (85%) ✅
- **Both metrics exceed 70% target!**

**Improvement**:
- v0.1: 0% → v0.3.1: 92% (+92 points!) 🎉

**What Worked**:
- Pronoun blacklist (20+ pronouns) - eliminated "She", "He", "They"
- "is/are" pattern - caught all biology definitions
- "was/were" pattern - caught history definitions
- "is given by" pattern - caught 1/2 math formulas
- "known as" pattern - worked perfectly
- Literature: 0 false positives ✅

**Remaining Edge Cases** (documented for future):
1. Biology: 1 sentence fragment ("...which: unicellular")
2. Math: 1 complex formula with parentheses missed
3. History: 1 borderline historical fact vs definition

**Key Learnings**:
1. **Iteration is essential**: v0.1 → v0.2 → v0.3 (failed) → v0.3.1 (success)
2. **Balance matters**: Over-filtering (v0.3: 33%) worse than under-filtering (v0.2: 116%)
3. **Simpler is better**: Permissive patterns + smart validation > complex regex
4. **Diminishing returns**: 92% is excellent; chasing 100% not worth it
5. **Real-world data is messy**: Edge cases like parenthetical formulas will always exist

**Tomorrow's Plan** (Day 3):
- [x] DONE with Issue #1 (92% >> 70% target)
- [ ] Move to Issue #2: Concept extraction with spaCy
- [ ] Target: 3/10 → 7/10 concept quality
- [ ] (Future: Can revisit definition edge cases if needed)

**Time Invested**: ~3 hours (4 iterations, testing, learning)

**Status**: ✅ ISSUE #1 RESOLVED - Exceeded target!