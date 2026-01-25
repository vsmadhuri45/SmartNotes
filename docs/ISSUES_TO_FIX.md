# Critical Issues to Fix

## 🔴 P0 - Must Fix for Week 2

### Issue #1: Definition Detection Failure
**Status**: ✅ Mostly Resolved (91.7% recall achieved)
**Priority**: P0 - Critical

**Resolution (Day 2)**:
- Implemented 7+ new patterns
- Improved from 0% to 91.7% recall
- Found 11/12 real definitions

**Patterns Effectiveness**:
- "is/are Y" - ⭐⭐⭐⭐⭐ Excellent (caught 8 definitions)
- "was/were Y" - ⭐⭐⭐⭐ Very good (caught 2 definitions)
- "known/acknowledged as" - ⭐⭐⭐⭐⭐ Perfect (caught 1 definition)
- "is given by" - ⭐ Poor (caught 0/2 - needs fix)

**Remaining Issues**:
- False positives (pronouns, narrative text)
- Math formula pattern needs to handle variables
- Precision: 78.6% (could be better)

**Future Work** (Low priority):
- Add pronoun filter
- Fix math pattern: `[a-zA-Z0-9\s]+`
- Confidence scoring for matches