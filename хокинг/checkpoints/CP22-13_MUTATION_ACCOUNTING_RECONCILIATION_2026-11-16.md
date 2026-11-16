# OMEGA-ISOP — CP22-13 MUTATION ACCOUNTING RECONCILIATION

DATE: 2026-11-16
SCOPE: CP22-13 mutation-test accounting only
STATUS: OPEN — PRIMARY MUTATION MATRIX REQUIRED
AUDITED SOURCE COMMIT: 43762921640e59941089ff90a49dab87fa59d4b5

## 1. Purpose

This checkpoint isolates and records an arithmetic and classification ambiguity in the CP22-13 audit report and its evidence register. It does not replace, rewrite, or silently correct the original audit. It does not search for or depend on the post-audit file OMEGA_CP22-13_AUDIT_EVIDENCE.txt.

## 2. Statements currently recorded in the audit

The CP22-13 audit/evidence register reports all of the following:

1. Total mutation set: 13 mutations.
2. Repository test suite detected: 10/13 mutations.
3. M07, M08 and M09 were not detected by the repository test suite, but were reportedly detected by independent analytical fixtures.
4. M13 was reportedly not detected by either the repository test suite or the independent analytical fixtures.

These are reported audit statements. The complete primary mutation table and per-mutation raw outcomes are not present in the audit Markdown currently read back for this reconciliation.

## 3. Arithmetic ambiguity

If M07, M08, M09 and M13 are all members of the same 13-mutation denominator, and if the first three are repository-suite misses while M13 is also a repository-suite miss, then there are at least four repository-suite misses. Under that interpretation, repository-suite detection would be 9/13, not 10/13.

The recorded 10/13 figure can be consistent only if at least one premise differs, for example:
- M13 is not part of the same 13-mutation denominator;
- one of the mutation classifications has been described imprecisely;
- the 10/13 figure uses a different test layer or denominator;
- the audit's summary count is erroneous.

The currently available audit text does not establish which interpretation is correct. Therefore this checkpoint does NOT replace 10/13 with 9/13 and does NOT assert a corrected score.

## 4. Required evidence structure

The mutation results must be reconciled using one row per mutation ID, with at least these fields:

| Field | Required meaning |
|---|---|
| Mutation ID | Stable identifier, e.g. M01–M13 |
| Mutated location | Exact file, symbol and mutation description |
| Included in denominator | Yes/No, with denominator definition |
| Repository test outcome | KILLED / SURVIVED / NOT RUN / INVALID |
| Repository detecting test | Exact test name or test ID |
| Independent fixture outcome | KILLED / SURVIVED / NOT RUN / INVALID |
| Independent detecting fixture | Exact fixture name or ID |
| Raw evidence reference | Exact log/file and relevant lines |
| Classification note | Explanation of any exclusion or special treatment |

Repository-test detection and independent analytical-fixture detection MUST remain separate columns and separate counts. They must not be merged into one detection score.

## 5. Current defensible status

FACT:
- The audit and evidence register report 10/13 repository mutation detection.
- The same records identify M07, M08 and M09 as repository-suite misses and report them detected by independent analytical fixtures.
- The same records identify M13 as not detected by either layer.

AUDIT FINDING:
- The reported counts are arithmetically ambiguous if all four IDs belong to the same 13-mutation denominator.

NOT ESTABLISHED:
- The corrected repository mutation score.
- The exact denominator membership for every mutation ID.
- The independent-fixture detection count as a complete score.
- The full per-mutation outcome matrix.

NO CORRECTED SCORE IS ASSIGNED.

## 6. Closure requirements

This checkpoint can close only after the primary mutation matrix and raw mutation results are supplied from an identified source and reconciled row by row. Closure must:

1. enumerate every mutation ID in the denominator;
2. identify the exact denominator used for each reported score;
3. record repository-suite outcome separately from independent-fixture outcome;
4. map every detected mutation to the exact test/fixture that detected it;
5. map every surviving, invalid or unrun mutation to its raw result and reason;
6. recompute both layer-specific scores from the row-level matrix;
7. have the arithmetic independently checked.

Do not infer missing outcomes from the summary prose.

## 7. Status locks

CP22-13: CONDITIONAL PASS — NOT CERTIFIED.
Mutation accounting: OPEN — RECONCILIATION REQUIRED.
F1–F7: OPEN, unless separately closed by documented evidence and review.
CAPD: NOT ESTABLISHED.
Interval certification: NOT ESTABLISHED.
Mathematical certification: NOT ESTABLISHED.
Universality: NOT ESTABLISHED.
Frozen Core: UNCHANGED.
Volume V: ACTIVE RESEARCH ARCHITECTURE.
CE-V-07: RESERVED.

END OF CHECKPOINT
