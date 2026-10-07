# Task 3 development evaluation

Actual outcome: **11/13 checks passed; 2 failed.**

These manually specified cases were visible during development. They test expected behavior, not generalization or complete factual correctness.

| Case | Category | Outcome |
|---|---|---|
| S01 | single | PASS |
| S02 | single | PASS |
| C01 | compare | PASS |
| C02 | compare | PASS |
| C03 | compare | PASS |
| C04 | compare | PASS |
| U01 | single | PASS |
| U02 | single | PASS |
| E01 | error | PASS |
| E02 | error | PASS |
| E03 | error | PASS |
| F01 | challenge | FAIL |
| F02 | challenge | FAIL |

## Failure analysis

The challenge probes ask about a named paper using terms belonging to another note. Lexical retrieval may select the other paper and respond instead of declining the unsupported attribution. A returned citation and a high match score do not establish that the answer addresses the named paper.

Comparison mode avoids one part of this problem by keeping explicit paper selections and testing topic evidence within each selected note. Single-question mode remains a limited baseline. Neither mode handles logical negation or verifies entailment.

Next steps: paper-name-aware question routing, a held-out set of misleading/negated questions, and manual assessment of relevance and evidence support. Full PDF indexing and semantic retrieval remain outside this version.
