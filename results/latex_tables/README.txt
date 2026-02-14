LaTeX TABLES - USAGE INSTRUCTIONS
=====================================

5 publication-ready tables generated for Paper 1:

TABLE 1 (table1_performance.tex):
  - Overall performance comparison (baseline vs current)
  - Use in: Results section, first subsection
  - Shows: 84.9% F1, +36.6pp improvement

TABLE 2 (table2_statistics.tex):
  - Statistical significance tests
  - Use in: Results section, validation subsection
  - Shows: p-values, Cohen's d effect sizes

TABLE 3 (table3_patterns.tex):
  - Pattern usage by domain
  - Use in: Analysis section
  - Shows: Domain-specific linguistic patterns

TABLE 4 (table4_domain_details.tex):
  - Detailed per-domain metrics
  - Use in: Results section, domain analysis
  - Shows: Precision, recall, min/max for each domain

TABLE 5 (table5_confidence.tex):
  - Bootstrap confidence intervals
  - Use in: Results section, reliability analysis
  - Shows: 95% CI for all metrics

HOW TO USE:
-----------
1. Add to your LaTeX preamble:
   \usepackage{booktabs}

2. Include individual table:
   \input{table1_performance.tex}

3. OR include all tables:
   \input{all_tables_combined.tex}

FORMATTING NOTES:
-----------------
- Uses booktabs package for professional horizontal lines
- Table* for wide tables (Table 4)
- All tables have proper captions and labels
- Use \ref{tab:performance} to reference Table 1
- Use \ref{tab:statistics} to reference Table 2
- etc.

READY TO PASTE INTO OVERLEAF OR TeXShop!
