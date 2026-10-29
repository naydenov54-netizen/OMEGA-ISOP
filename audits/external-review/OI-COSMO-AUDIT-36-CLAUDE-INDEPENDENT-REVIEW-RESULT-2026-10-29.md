# OMEGA-ISOP M3.2 — Audit #36 Independent Mathematical Review Record

**Date received:** 2026-10-29  
**Reviewed:** Baseline Audit #36 (Part A) and proposed revision v3.1 (Part B)  
**Overall status:** `MATERIAL_ISSUES`  
**Baseline status:** `MATERIAL_ISSUES`  
**v3.1 status:** `VALID_WITH_ASSUMPTIONS`

## Executive conclusion

The review reports that the baseline contains material overclaims: equality of single-experiment marginals does not imply equality of repeated/joint observation laws, and a stopping rule stated with minima/maxima is not justified when infima/suprema may fail to be attained. Its robust extension also needs separate treatment.

The review did not find a critical error in v3.1's main numerical examples, but identified missing assumptions and scope issues. The most important repairs concern Markov-kernel measurability, tying admissible policies to protocol class Π, conditional versus root-level invariance, measurable decision rules, mixed stop/continue policies, and the robust recursion example.

This file is a normalized record of the received review, not a verbatim transcript. The complete JSON-form finding record is stored alongside it. The review does **not** establish physical validity, empirical support, completeness of the model, or canonical status.

## Findings register

| ID | Severity | Status | Core finding |
|---|---|---|---|
| F001 | MAJOR | `FALSE_AS_WRITTEN` | Single-experiment marginal equivalence does not imply equality of repeated/joint observation laws. |
| F002 | MAJOR | `NOT_ESTABLISHED` | Minimum/maximum formulations require attainment; a continuation infimum may not be attained. |
| F003 | MAJOR | `NOT_ESTABLISHED` | Expected-loss stopping logic cannot be transferred to robust criteria without separate definitions and proof. |
| F004 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | EVSI nonnegativity needs well-defined risks, posterior, measurability and integrability/extended-real conventions. |
| F005 | MAJOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Measurability of h↦P_h^e(B) and h↦Law_h^π(B) is needed to construct joint/prior-predictive laws and posteriors. |
| F006 | MAJOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Protocol equivalence does not cover an arbitrary policy unless every admissible policy induces a protocol in Π. |
| F007 | MAJOR | `NOT_ESTABLISHED` | Equal likelihood of a past history preserves posterior odds but not future kernels or continuation values; root proof alone is insufficient. |
| F008 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Equality between integrated pointwise posterior infimum and infimum over measurable decision rules needs measurable-selection/epsilon-optimality conditions. |
| F009 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Pure stop/continue classes do not partition a universe that admits randomized mixtures; for expected loss mixtures cannot improve below the smaller class infimum. |
| F010 | MINOR | `AMBIGUOUS` | Standard-Borel conditions should identify the conditioned hypothesis space and observation space, not just say 'common setting'. |
| F011 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | R_e may be −∞ under an extended-real loss convention, so EVSI may be +∞ rather than a finite difference. |
| F012 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | The comparison is root-level; sequential implementation needs Bellman and measurable-selection conditions, and degenerate empty/infinite cases need scope. |
| F013 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | A positive minimum cost plus finite budget ensures finite termination only with a hard pathwise budget and suitable deterministic/almost-sure cost bound. |
| F014 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | The sequence decreases to 1/3 without attaining it at finite n; non-attainment depends on finite termination and the allowed experiment sequence. |
| F015 | MINOR | `AMBIGUOUS` | The example gives ex-ante versus conditionally re-optimized value discrepancy for pure actions, not a plan reversal or stop/continue counterexample. |
| F016 | MINOR | `AMBIGUOUS` | For an exact union of pure policy classes inf F equals the minimum of class infima; mixture-admissible robust classes can do better due to convexity. |
| F017 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Kernel-equality condition needs induction by history length, positive-probability reachability for counterexamples, and non-anticipating consistency. |
| F018 | MINOR | `VALID_UNDER_ADDITIONAL_ASSUMPTIONS` | Equal history laws imply LR=1 almost surely; posterior-odds equality additionally requires positive prior masses and predictive support. |
| F019 | MINOR | `AMBIGUOUS` | Robust invariance over a set of priors is not defined by a single-prior mass move; a vague 'relevant' sentence is not a theorem. |
| F020 | MINOR | `VALID_AS_WRITTEN` | Single-experiment equivalence plus loss equivalence does not preserve EVSI under repeated performance; reported values are 1/2 and 1/4. |
| F021 | EDITORIAL | `AMBIGUOUS` | Notation overload (π prior/protocol), Proposition 1b numbering, and redundant cost condition create avoidable ambiguity. |

## Numerical checks reported

1. **Repeated runs:** Under h, d₂=d₁ with d₁~Bernoulli(1/2); under h′, d₁ and d₂ are independent Bernoulli(1/2). Therefore P(d₁=d₂)=1 versus 1/2.
2. **Prior mass move, one observation:** The reported EVSI values are 1/2 under μ_A and 0 under μ_B.
3. **Prior mass move, repeated observations:** The reported EVSI values are 1/2 under μ_A and 1/4 under μ_B.
4. **Complementary experiments:** Each experiment alone has EVSI 0; together they have EVSI 1/2. With cost c per experiment, the two-step net value is 1/2−2c, positive when 0<c<1/4.
5. **Non-attainment:** Vₙ=2⁻ⁿ+(1−4⁻ⁿ)/3 decreases to 1/3 without attaining that value at any finite n. The conclusion depends on requiring finite termination and restricting the example to sequential prefix queries.
6. **Robust example:** The ex-ante deterministic minimax value is 1/2; conditionally re-optimized pure-action worst-case value is 1. A fair randomized guess restores value 1/2. This is a value-recursion discrepancy for the stated class, not a demonstrated plan reversal or stopping-rule counterexample.

## Patch disposition in proposed v3.2

- **F005:** Added explicit Markov-kernel measurability and posterior-existence conditions.
- **F006–F008:** Connected policies to Π, narrowed the same-likelihood statement, and made measurable decision-rule/selection assumptions explicit.
- **F009, F012–F013:** Distinguished pure stopping/continuation classes from the global class, clarified root-level scope, and tightened budget/cost assumptions.
- **F010–F011:** Specified standard-Borel/posterior conditions and finite versus extended-real EVSI conventions.
- **F014:** Added a concrete sequential binary-digit realization and the finite-termination/prefix-query restrictions.
- **F015–F016:** Reframed the robust example as a value-recursion discrepancy and corrected the union-versus-mixture explanation.
- **F017–F018:** Added kernel/induction and positive-prior-mass scope clarifications to the relevant claims.
- **F001–F004, F019–F021:** Baseline defects remain documented; the proposal does not rewrite historical records. Robust prior-set language and notation should remain narrowly scoped.

## Limitations and governance

The review states that it used no external sources, code or tools and relied on hand calculations. Standard measure-theoretic theorems were not reproved. No files were changed by the reviewer. The resulting v3.2 is still a proposal and has not received a second independent review.

- Frozen Core: unchanged.
- CE-V promotion: not claimed.
- RL registration: not claimed.
- Canonical acceptance: not claimed.
- Physical/empirical validity: not established.
