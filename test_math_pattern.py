"""
Quick test for math formula detection
"""
import re

# Test text from math notes
test_text = """
In an A.P. with first term a and common difference d, the nth term (or the general term) is given
by an = a + (n – 1)d.

The sum of the first n terms of an A.P. is given by
Sn = n/2[2a + (n – 1)d] or n/2[a + l]
where, l is the last term of the finite AP.
"""

# The improved patterns
pattern5_options = [
    # Option 1: Standard
    r'([Tt]he\s+[a-zA-Z0-9\s()]+?\s+(?:term|sum|formula|equation))\s+is given by\s+([^.!?\n]+)',
    # Option 2: Complex with "of"
    r'([Tt]he\s+[a-zA-Z0-9\s()]+?\s+of\s+[^.!?\n]+?)\s+is given by\s+([^.!?\n]+)',
    # Option 3: Flexible
    r'([Tt]he\s+[^.!?\n]+?)\s+is given by\s+([^.!?\n]+)',
]

print("Testing math formula patterns...\n")

for idx, pattern in enumerate(pattern5_options, 1):
    print(f"Pattern {idx}:")
    matches = re.findall(pattern, test_text, re.IGNORECASE)
    print(f"  Matches found: {len(matches)}")
    for term, definition in matches:
        term_lower = term.lower()
        if any(word in term_lower for word in ['term', 'sum', 'formula', 'equation', 'nth', 'first', 'last']):
            print(f"  ✓ '{term.strip()}': {definition.strip()[:50]}...")
        else:
            print(f"  ✗ '{term.strip()}' (filtered - not math-related)")
    print()

print("\nExpected: Should find 2 formulas")
print("1. 'the nth term (or the general term)' ")
print("2. 'The sum of the first n terms of an A.P.'")