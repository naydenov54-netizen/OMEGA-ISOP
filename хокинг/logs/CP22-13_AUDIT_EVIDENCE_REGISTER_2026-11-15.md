# OMEGA-ISOP — CP22-13 AUDIT EVIDENCE REGISTER

- Recorded: 2026-11-15
- Audited source commit: `43762921640e59941089ff90a49dab87fa59d4b5`
- Audit report: [CP22-13 independent second-stage audit](./CP22-13_INDEPENDENT_SECOND_STAGE_AUDIT_2026-11-15.md)
- Scope: evidence inventory and provenance notes only.

## Evidence reported by the auditor

The second-stage audit report states that the following checks were performed against a clean clone of the exact source commit:

- CMake configure and build: exit 0.
- CTest: 4/4 passed.
- Curvature engine test executable: 10/10 checks passed.
- Additional compiler run: clang++ 18.1.3, 10/10.
- ASan+UBSan run: 10/10, no reported sanitizer errors.
- Optimization configurations: -O0, -O3, and -O3 -ffast-math, 10/10.
- Independent analytical fixtures: 37/37 reported passing.
- Mutation testing: 10/13 mutations detected by repository tests; M07, M08, M09 and M13 not detected as described in the audit.
- Numerical stress and conditioning tests: findings F2 and F3 reported; see the audit report.

## Source identity reported

- `curvature_engine.hpp`: Git blob `e3c1c0e37b5e391695d6a8e4c3e6a221ca430832`
- `tensor_storage.hpp`: Git blob `039c0544fe1b47234221547326e130850b90e56c`
- `metric_provider.hpp`: Git blob `4e7514ebfc0ebfab4a05989b540ad3966d1c63d6`
- `test_curvature_engine.cpp`: Git blob `c1aeca276ae2efa5339aeed307faba2328242f1b`
- `CMakeLists.txt`: Git blob `6e75bf936d6ad9f3815a1b2b641c4e9a1b186cb6`

The audit also supplied abbreviated SHA-256 values for source files and logs. Those values were abbreviated in the received report (for example, `cd4c3d79…f689f783`) and are therefore recorded in the audit text, not represented here as complete verifiable digests.

## Raw evidence attachment status

The auditor's report names an attachment `OMEGA_CP22-13_AUDIT_EVIDENCE.txt`, described as containing raw logs and fixture source code, and reports its SHA-256 as:

`f90f6f5e22af9ef1037193b2c3617f8a53767a216411ae016fd6471e3ffb5df0`

**The actual attachment bytes were not available in the material received for this GitHub write.** Consequently, this repository entry does NOT claim to contain the raw logs, fixture source, or a byte-for-byte copy of that attachment. The reported digest has not been independently recomputed here. The raw evidence file must be uploaded or otherwise supplied before it can be committed as an actual evidence artifact.

## Status and limitations

- This register records what the auditor reported; it is not an independent rerun of those tests.
- The raw logs and fixture source are not included in this file.
- No CAPD or interval-arithmetic validation is claimed.
- No mathematical certification or universality is claimed.
- CP22-13 remains **CONDITIONAL PASS**, restricted to the tested domain, with findings F1–F10 and required corrections as detailed in the audit report.
- Frozen Core remains unchanged; Volume V remains the Active Research Architecture; CE-V-07 remains RESERVED.

## Required next evidence action

Add the original `OMEGA_CP22-13_AUDIT_EVIDENCE.txt` only after its actual bytes are available. Verify its complete SHA-256 locally and record the full digest, file size, and provenance. Do not substitute this register for the raw evidence bundle.
