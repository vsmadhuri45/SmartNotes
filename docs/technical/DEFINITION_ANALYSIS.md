# Definition Analysis - Test Notes

## Purpose
Manually identify ALL definitions in our test notes to create comprehensive test cases.

---

## Biology Notes (Vertebrates, Bryozoans, Protozoa)

**Definitions to Find**:

1. "Vertebrates are the animals possessing backbones"
   - Pattern: [Term] are [definition]
   
2. "Amphibians are species that live in the land and move to water for breeding"
   - Pattern: [Term] are [definition]
   
3. "Reptiles are covered by scutes"
   - Pattern: [Term] are [definition]
   
4. "Mammals are terrestrial, aquatic or aerial"
   - Pattern: [Term] are [definition]
   
5. "Birds are covered with feathers and have streamlined avenues"
   - Pattern: [Term] are [definition]
   
6. "Bryozoans are normally acknowledged as moss animals"
   - Pattern: [Term] are normally acknowledged as [definition]
   
7. "Zooids are individuals in bryozoans"
   - Pattern: [Term] are [definition]
   
8. "Protozoa are the different group of eukaryotic organisms which are unicellular"
   - Pattern: [Term] are [definition with description]

**Total Definitions**: 8

---

## Literature Notes (The Frog and Nightingale)

**Definitions to Find**: 0
- This is a narrative story, no formal definitions
- Correct that we found 0!

**Total Definitions**: 0 ✅

---

## History Notes (Russian Revolution)

**Definitions to Find**:

1. "The Russian Socialist Democratic Labour Party was formed in 1900"
   - Pattern: [Term] was formed in [date]
   
2. "Russia was an autocracy"
   - Pattern: [Term] was [definition]
   
3. "The Tzar was not subject to the Parliament"
   - Pattern: [Term] was not [description]
   - (Debatable if this is a definition - maybe skip)

4. "A Military Revolutionary Committee was appointed by the Soviet"
   - Pattern: [Term] was appointed [context]
   - (This is more of a fact than definition)

**Total Definitions**: 2-3 (let's say 2 clear ones)

---

## Math Notes (Arithmetic Progression)

**Definitions to Find**:

1. "In an A.P. with first term a and common difference d, the nth term (or the general term) is given by an = a + (n – 1)d"
   - Pattern: [Term] is given by [formula]
   
2. "The sum of the first n terms of an A.P. is given by Sn = n/2[2a + (n – 1)d]"
   - Pattern: [Term] is given by [formula]

**Total Definitions**: 2

---

## Summary: Ground Truth

| Note Type | Definitions | Patterns Needed |
|-----------|-------------|-----------------|
| Biology   | 8           | "X are Y", "X are acknowledged as Y" |
| Literature| 0           | N/A |
| History   | 2           | "X was Y", "X was formed in Y" |
| Math      | 2           | "X is given by Y" |
| **TOTAL** | **12**      | Multiple patterns required |

---

## Pattern Requirements

Based on analysis, we need to catch:

### Pattern 1: "X is/are Y"
- "Vertebrates are the animals..."
- "Reptiles are covered..."
- "Russia was an autocracy"

### Pattern 2: "X is/are known/acknowledged as Y"
- "Bryozoans are normally acknowledged as..."
- "X is known as Y"

### Pattern 3: "X is given by Y" (for formulas)
- "The nth term is given by..."
- "The sum is given by..."

### Pattern 4: "X was/were formed/created/established in Y"
- "The party was formed in 1900"

### Pattern 5: "X means/refers to/denotes Y"
- General purpose pattern

### Pattern 6: "X is defined as Y"
- Already have this one!

### Pattern 7: "X: Y" (colon definitions)
- Already have this one!

---

## Test Cases for Validation

After implementing, check these specific cases:

✅ = Should find
❌ = Currently misses

Biology:
- ✅ "Vertebrates are the animals possessing backbones"
- ✅ "Amphibians are species that..."
- ✅ "Bryozoans are normally acknowledged as..."

History:
- ✅ "Russia was an autocracy"
- ✅ "The party was formed in 1900"

Math:
- ✅ "The nth term is given by..."
- ✅ "The sum is given by..."

---

## Success Criteria

**Baseline**: 0/12 definitions (0%)
**Target**: 8-9/12 definitions (67-75%)
**Stretch Goal**: 10-11/12 definitions (83-92%)

If we get 8+, we've succeeded! 🎯