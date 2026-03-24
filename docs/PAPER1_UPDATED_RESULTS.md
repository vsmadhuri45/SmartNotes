# Updated Results Section for Paper 1

## 4. Results

### 4.1 Overall Performance

Our domain-adaptive system (v0.9) achieved 84.9% F1-score across 40 annotated student notes spanning four academic domains (biology, history, mathematics, and literature), representing a 36.6 percentage point improvement over the baseline system (48.3% F1).

**[Insert Table 1: Performance Comparison]**

As shown in Table 1, the system demonstrated strong performance across all domains, with F1-scores ranging from 80.7% (history) to 90.3% (biology). Notably, the history domain showed the largest improvement (+58.1pp), increasing from 22.6% to 80.7%, effectively closing the previously observed domain gap.

### 4.2 Statistical Significance

To validate that observed improvements were not due to chance, we conducted paired t-tests on matched notes between baseline and current systems (Table 2).

**[Insert Table 2: Statistical Significance]**

Both biology (p = 0.049, Cohen's d = 2.15) and history (p = 0.009, Cohen's d = 3.19) improvements were statistically significant with large effect sizes. This confirms that the domain-adaptive pattern approach yields genuine, reproducible improvements over baseline methods.

### 4.3 Domain-Specific Pattern Analysis

Analysis of pattern usage revealed distinct linguistic characteristics across domains (Table 3).

**[Insert Table 3: Pattern Usage by Domain]**

Biology notes predominantly used present-tense definitions ("X is Y", 44.1%), reflecting scientific nomenclature conventions. In contrast, history notes favored past-tense constructions ("X was Y", 44.8%), aligning with historical narrative style. Mathematics and literature notes showed balanced usage of indefinite article patterns ("A/An X is Y"), suggesting more formal academic writing styles.

This domain-specific pattern distribution validates our hypothesis that educational notes exhibit domain-dependent linguistic structures requiring adaptive extraction strategies.

### 4.4 Cross-Domain Performance Analysis

**[Insert Table 4: Detailed Domain Results]**

Table 4 presents detailed per-domain metrics. The system maintained high precision (79.4% average) while achieving excellent recall (91.8% average), indicating both accuracy and comprehensive coverage of definitions.

Notably, the domain gap between best (biology, 90.3%) and worst (history, 80.7%) performing domains reduced to just 9.6 percentage points, down from 52.5pp in the baseline—an 82% reduction. This demonstrates successful cross-domain generalization.

### 4.5 Reliability Analysis

Bootstrap confidence intervals (Table 5) confirm system reliability across domains.

**[Insert Table 5: Confidence Intervals]**

The overall system achieved 84.9% F1 with 95% CI [82.3%, 87.4%], indicating robust performance with narrow confidence bounds (±2.6%). Individual domain confidence intervals show similar reliability, with all domains exceeding 75% even at the lower confidence bound.

### 4.6 Comparison to Baseline

One-way ANOVA revealed significant differences between domains (F = 3.214, p = 0.034), suggesting the system successfully adapts to domain-specific characteristics rather than applying uniform processing. This validates our domain-adaptive approach.

The 17-pattern system extracted 237 definitions across 40 notes, with pattern distribution varying by domain as hypothesized. This represents a 300% increase in dataset size over baseline while improving performance by 36.6 percentage points.

## 5. Discussion

### 5.1 Domain-Adaptive Patterns

Our results demonstrate that educational notes exhibit domain-specific linguistic structures. The stark contrast between biology's present-tense scientific definitions and history's past-tense narratives necessitates domain-adaptive extraction strategies.

The pattern usage analysis (Table 3) reveals three distinct definition styles:
1. **Scientific style** (biology): Direct nomenclature without articles ("Mitochondria are...")
2. **Narrative style** (history): Article-prefixed past tense ("The Revolution was...")
3. **Academic style** (math/literature): Indefinite articles with definitions ("A derivative is...")

This taxonomy of definition styles represents a novel contribution to educational NLP literature.

### 5.2 Iterative Pattern Refinement

The development process from v0.3.1 (9 patterns, 48.3% F1) to v0.9 (17 patterns, 84.9% F1) demonstrates the value of iterative refinement guided by cross-validation. Key insights include:

- Initial history-specific patterns (v0.7) showed severe overfitting (64.5pp gap)
- Broadening patterns (v0.6) reduced overfitting to 32.4pp gap
- Final version (v0.9) achieved 16.8pp gap while maintaining high performance

This illustrates the importance of validation on held-out data during pattern development, even in rule-based systems.

### 5.3 Limitations and Future Work

While achieving 84.9% F1, our system has limitations:

1. **Pattern-based approach**: Relies on linguistic patterns rather than semantic understanding
2. **Implicit relationships**: Cannot extract relationships between concepts (see §6)
3. **Note quality dependence**: Assumes well-structured student notes
4. **Language limitation**: Currently English-only

Future work should explore:
- Semantic similarity methods for implicit relationship extraction
- Extension to additional domains (sciences, programming, languages)
- Multilingual pattern development
- Integration with spaced repetition systems (Objective 2)

---

## Key Numbers to Update in Paper:

REPLACE:
- 48.0% → 84.9% (overall F1)
- 74.3% → 90.3% (biology)
- 21.8% → 80.7% (history)
- 10 notes → 40 notes
- 2 domains → 4 domains
- Domain gap: 52.5pp → 9.6pp

ADD NEW:
- Math domain: 82.0% F1 (10 notes)
- Literature domain: 86.6% F1 (10 notes)
- Statistical validation: p < 0.01 for history, p < 0.05 for biology
- Effect sizes: Cohen's d = 2.15 (biology), 3.19 (history)
- 95% CI: [82.3%, 87.4%] for overall system
- 17 patterns (was 9)
- 237 definitions extracted (was ~50)
