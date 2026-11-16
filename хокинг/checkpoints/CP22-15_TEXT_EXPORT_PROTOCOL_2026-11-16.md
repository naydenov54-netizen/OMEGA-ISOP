# CP22-15 — OMEGA-ISOP TEXT EXPORT PROTOCOL

Date: 2026-11-16
Status: WORKFLOW REQUIREMENT RECORDED

## Authoritative protocol

OMEGA-ISOP TEXT EXPORT PROTOCOL

1. NO ZIP ARCHIVES.
2. ONE SOURCE FILE = ONE OR MORE TXT PARTS.
3. EVERY PART HAS A SEQUENTIAL NUMBER.
4. EVERY PART IDENTIFIES ITS ORIGINAL SOURCE.
5. EVERY SOURCE HAS A SHA-256 HASH.
6. MANIFEST RECORDS ALL EXPORTED PARTS.
7. MISSING FILES ARE EXPLICITLY REPORTED.
8. ORIGINAL FILES ARE NEVER MODIFIED.
9. PART COUNT MUST MATCH MANIFEST.
10. NO AUDIT RESULT IS ACCEPTED FROM AN INCOMPLETE EXPORT.

## Operational interpretation

- Export source files as plain-text .txt parts; do not package exports in ZIP archives.
- Use stable sequential part numbering for every multi-part source.
- Include the original source identity in every part, not only in the manifest.
- Calculate and record SHA-256 for each original source file.
- The manifest must enumerate every exported part and map it to its source, hash, and part sequence.
- Report every missing source explicitly; do not silently omit it.
- Treat source files as read-only. Export operations must not alter originals.
- Validate that the actual exported part count equals the manifest's declared part count before audit use.
- An audit based on an incomplete, unverified, or manifest-inconsistent export is NOT ACCEPTED and must not support a pass, score, or certification claim.

## Status and scope

This is a mandatory data-handling and audit-intake protocol. It does not itself establish source completeness, mathematical correctness, mutation outcomes, CAPD validation, interval certification, or mathematical certification.

Frozen Core: PRESERVED / UNCHANGED.
Volume V: ACTIVE RESEARCH ARCHITECTURE.
CE-V-07: RESERVED.
Universality: NOT ESTABLISHED.
CAPD / interval certification: NOT ESTABLISHED.
Mathematical certification: NOT ESTABLISHED.

END OF CP22-15
