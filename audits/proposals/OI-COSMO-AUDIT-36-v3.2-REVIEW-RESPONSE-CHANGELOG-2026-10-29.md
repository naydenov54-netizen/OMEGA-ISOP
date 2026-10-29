# Audit #36 — v3.2 review-response change log

**Purpose:** Record how the proposed revision responds to the received independent mathematical review. This is a proposal-only patch, not a canonical change.

## Changes made

1. **Kernel measurability (F005):** Section 1 now defines each observation law as a Markov kernel and states measurability of the full-history law for each fixed protocol.
2. **Posterior existence (F010):** Section 1 and A3 identify standard-Borel conditions for hypothesis and observation/history spaces, or require equivalent conditions guaranteeing regular conditional distributions.
3. **Policy/protocol compatibility (F006):** Proposition 1b now requires each admissible policy to induce a protocol in Π and its terminal action to be a measurable function of history and h-independent randomization.
4. **Conditional invariance (F007):** Equal likelihood of a past history is no longer treated as sufficient for future-value invariance. Conditional invariance requires equal conditional laws under all admissible future protocols, plus matching feasibility, loss and cost assumptions.
5. **Measurable rules (F008):** A4 now requires measurable ε-optimal rules or an equivalent condition connecting pointwise posterior infima with infima over measurable decision rules.
6. **Extended-real EVSI (F011):** A6 distinguishes finite EVSI from an explicitly permitted +∞ value.
7. **Stop/continue mixtures (F009):** D_stop and D_cont are defined as pure classes; the global class Δ and expected-loss mixture convention are stated without falsely calling the pure classes a partition when mixtures are admissible.
8. **Cost/budget scope (F013):** The finite-termination implication now requires a hard pathwise budget and a deterministic or almost-sure positive lower bound on each selected cost, or an explicit termination condition.
9. **Non-attainment realization (F014):** Section 6.8 gives θ∼Uniform[0,1), loss 4|a−θ|, sequential binary-digit revelation, prefix-query restriction, and finite-termination requirement.
10. **Robust recursion (F015–F016):** Section 6.10 now calls the result a value-recursion discrepancy for the specified pure-action class, explicitly disclaims a demonstrated plan reversal/stopping counterexample, and separates the exact-union identity from the possible benefit of robust mixtures.
11. **Scope language:** The document continues to distinguish root-level comparisons from sequential optimality and keeps physical/empirical validity and canonical status explicitly unclaimed.

## Preserved records

- The baseline audit remains historical and unchanged.
- The v3.1 proposal remains a historical version and is not silently overwritten.
- The received review record is stored in `audits/external-review/`.
- v3.2 is proposal-only pending review and explicit governance acceptance.
