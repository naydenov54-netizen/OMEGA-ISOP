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


## 8. Targeted SOURCE_INVENTORY disposition — 2026-11-19

Scope: targeted inspection of the eight exact filenames already listed in CP22-13-MR-01 workbook intake. This is a repository-availability and relevance check, not a claim that every external Drive location was searched.

| Inventory entry | Repository evidence located | Mutation-matrix relevance / disposition |
|---|---|---|
| OI-GR06C-CAPD-T13A-R2-DATE.txt | Exact filename surfaced only in the workbook intake inventory. | Original bytes and contents not retrieved. No M01–M13 row outcome established. |
| VOLUME 5 v2.1–CAPD.txt | Referenced by the workbook intake and archive-discovery record with reported size/hash; exact source bytes not retrieved. | CAPD research insert; extracted workbook rows are not a mutation-result table. No M01–M13 outcome established. |
| OMEGA_ISOP_DRIVE_FORENSIC_REPORT.json | Exact filename surfaced only in the workbook intake inventory. | Original bytes and contents not retrieved. No M01–M13 row outcome established. |
| OMEGA_ISOP_NOTEBOOK_FORENSIC_INDEX_2026-11-07.json | Exact filename surfaced only in the workbook intake inventory. | Original bytes and contents not retrieved. No M01–M13 row outcome established. |
| OMEGA_FORENSIC_AUDIT_PARTS.txt | A separate GitHub checkpoint records its reported Drive path, size and SHA-256; the source report itself is explicitly not uploaded. The source/continuation index warns not to reconstruct it from snippets. | This is a multi-notebook CAPD forensic report, not a primary M01–M13 mutation matrix. No mutation row outcome established. |
| TEST 0–12.txt | Referenced by the archive-discovery record with reported size/hash; exact source bytes not retrieved. | Contents not established. No M01–M13 row outcome established. |
| Untitled44_SOURCE_AUDIT.txt | Referenced by the archive-discovery record with reported size/hash; exact source bytes not retrieved. | Source-audit metadata only in the retrieved records. No M01–M13 row outcome established. |
| OMEGA_ISOP_UNTITLED109_FORENSIC_AUDIT.txt | GitHub contains chunked forensic extracts and a session checkpoint referring to the Drive report; the original report bytes are not established as present. | The retrieved chunks concern CAPD build/rounding evidence and do not provide the CP22-13 curvature-engine M01–M13 mutation matrix. No mutation row outcome established. |

### 8.1 Evidence boundary

The exact-name repository checks did not retrieve the original byte streams for the eight inventory entries. The workbook's reported sizes and SHA-256 values remain inventory metadata, not independently verified source identities in this review. Related GitHub checkpoints and forensic excerpts are secondary records and cannot substitute for the original files or raw mutation execution logs.

The available records also establish that the OMEGA_FORENSIC_AUDIT_PARTS.txt source report was not uploaded, and that the Untitled109 forensic extracts are not the CP22-13 curvature-engine mutation matrix. No source inspected in this targeted pass supplies, for any M01–M13, the required denominator membership, mutated file/symbol, repository detecting test, independent detecting fixture, and raw-result reference.

### 8.2 Result and next action

- Primary mutation matrix: NOT LOCATED IN THE INSPECTED REPOSITORY MATERIAL.
- M01–M13 denominator membership: UNRESOLVED.
- Repository-suite per-mutation outcomes: UNRESOLVED.
- Independent-fixture per-mutation outcomes: UNRESOLVED.
- Repository detection score: NOT RECOMPUTED.
- Independent-fixture detection score: NOT RECOMPUTED.
- Arithmetic ambiguity (10/13 versus four reported repository misses): OPEN.

Do not infer any outcome from the inventory metadata, archive-discovery summaries, CAPD forensic excerpts, or audit prose. Resume only when the actual mutation matrix/raw result bundle or a concrete path to those exact bytes is supplied. The next required artifact is the primary M01–M13 mutation table together with raw repository-suite and independent-fixture outputs.

This disposition does not establish that the files are absent from every external Drive/Colab location. It records only what was and was not retrievable from the targeted repository material inspected here.

CP22-13 remains CONDITIONAL PASS — NOT CERTIFIED. Mutation accounting remains OPEN. Frozen Core remains UNCHANGED.
