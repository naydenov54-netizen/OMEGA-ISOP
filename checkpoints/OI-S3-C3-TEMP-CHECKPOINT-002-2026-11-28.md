# OMEGA-ISOP S3-C3 — TEMPORARY RESEARCH CHECKPOINT

**Record ID:** OI-S3-C3-TEMP-CHECKPOINT-002  
**Date:** 2026-11-28  
**Workstream:** S3-C3 / Constraint Amalgamation Classification  
**Status:** TEMPORARY RESEARCH RECORD  
**Canonical status:** No Frozen Core change; no theorem registration  
**Coverage:** Source reconciliation addendum 2026-11-27 and experiments II-1 through II-4

---

## 1. Purpose

This checkpoint preserves the current S3-C3 research state and distinguishes established source assumptions, conditional construction results, exploratory tests, and unresolved questions.

It is not a modification of the Frozen Core and does not promote any research result to theorem-registry status.

## 2. Protected framework

The apartness structure is:

```text
A = (U0, #)
# : U0 x U0 -> {TRUE, FALSE}
```

The frozen apartness axioms are:

```text
A1: NOT(x # x)

A2: x # y IFF y # x

A3: x # y -> (x # z OR z # y), for every z
```

Under the complete Boolean apartness realization and classical Boolean logic:

```text
x ~ y IFF NOT(x # y)
```

A1-A3 imply that `~` is an equivalence relation. Its quotient is:

```text
DS = U0 / ~
```

**Logic boundary:** No intuitionistic or non-Boolean generalization is made.

Apartness embeddings must preserve and reflect apartness:

```text
x #1 y IFF f(x) #2 f(y)
```

Preservation alone is insufficient.

## 3. Recovered amalgamation architecture

### 3.1 P2.3 quotient-based strong apartness amalgam

The source construction forms:

```text
Q_A = S_A / ~_A
Q_B = S_B / ~_B
Q_C = S_C / ~_C
```

It takes the pushout `Q` of `Q_A` and `Q_B` over `Q_C`, and the pushout `S_P` of the underlying sets over `S_C`.

The quotient map on the amalgam is defined from the component quotient maps. Apartness is then:

```text
x #_P y IFF pi_P(x) != pi_P(y)
```

The source records A1-A3 and strong apartness embeddings under its stated assumptions. This is a strong amalgam, not a claim that the construction is a categorical pushout in every category of apartness structures.

**Audit status:** Source-reported proof; independent proof audit remains required before formal registration.

### 3.2 P2.4.1 free relational amalgam

For a pure relational signature without extra axioms coupling relations to apartness, the free relational amalgam interprets each relation as the union of the two component relations. Mixed tuples are false.

This result assumes agreement on the common substructure.

It does not establish amalgamation for arbitrary relational constraints coupled to apartness.

### 3.3 Quotient descent

For an n-ary relation `R`, coordinatewise `~`-invariance is:

```text
(x1~y1 AND ... AND xn~yn)
->
(R(x1,...,xn) IFF R(y1,...,yn))
```

This is necessary and sufficient for `R` to descend to a well-defined relation on `S/~`.

It is not, by itself, a compatibility criterion for arbitrary constraint theories.

## 4. Classification framework under investigation

Let `K` be a specified class of structures, `Γ` a specified set of constraints, and:

```text
A <- C -> B
```

an admissible embedding span.

An amalgam is a structure `P` with embeddings of `A` and `B` into `P` that agree on `C`.

A strong amalgam additionally requires:

```text
image(A) INTERSECTION image(B) = image(C)
```

The three proposed research classes are:

### Class I — Canonical-amalgam preserving

For every admissible span, the specified canonical construction `P_can` satisfies `Γ`.

```text
FOR ALL admissible spans:
P_can(A,B,C) satisfies Γ
```

### Class II — Alternative-amalgam admitting

The canonical construction fails for at least one admissible span, but an alternative admissible amalgam exists for every span in the class under consideration.

```text
Some P_can fails Γ
AND
FOR ALL admissible spans, SOME P_alt satisfies Γ
```

A failure of the canonical construction is not evidence of Class III.

### Class III — Amalgamation obstructed

There is at least one admissible span for which no amalgam in the specified class satisfies the constraints.

```text
EXISTS admissible span:
NO P in K is a Γ-amalgam of A and B over C
```

To establish Class III, impossibility must be proved for every possible amalgam, not merely for P_can or one alternative construction.

**Important:** The three classes are meaningful only after fixing `K`, the signature, the constraint semantics, the embedding notion, and whether ordinary or strong amalgamation is required.

## 5. Experiments recorded

### Experiment II-1 — Transitivity of R

Constraint:

```text
T_R:
R(x,y) AND R(y,z) -> R(x,z)
```

Span:

```text
A = {a,b}, R_A = {(a,b)}
B = {b,c}, R_B = {(b,c)}
C = {b},   R_C = {}
```

The free relational amalgam contains `R(a,b)` and `R(b,c)` but not `R(a,c)`, so it fails transitivity.

Adding `R(a,c)` gives a transitive relation in this finite example.

**Result:** The free construction fails. This example alone does not establish a global Class II result.

### Experiment II-2 — Transitivity plus quotient invariance

Additional constraint:

```text
I_R:
x~x' AND y~y'
->
(R(x,y) IFF R(x',y'))
```

Under `I_R`, `R` descends to the quotient. A candidate alternative construction is:

```text
E = R_QA UNION R_QB
R_Q = TC(E)

R_P(x,y) IFF R_Q(pi_P(x), pi_P(y))
```

where `TC` is transitive closure.

A proposed lemma states that, when both component relations are transitive and the common substructure is induced for `R`, transitive closure does not add new relation pairs inside either component.

Proof idea: any path that leaves one component must pass through the common substructure; inducedness and transitivity allow each outside segment between common-substructure points to be replaced by an edge already present in the component.

**Status:** Conditional construction result, requiring a careful formal audit of the quotient pushout, inducedness, and preservation/reflection conditions. Do not register as a theorem yet.

If the lemma's hypotheses hold, this construction gives a strong amalgam for transitive quotient relations in the specified setting.

### Experiment II-3 — Transitivity plus negative apartness coupling

Constraint:

```text
C_R:
R(x,y) -> NOT(x#y)
```

Equivalently:

```text
R(x,y) -> x~y
```

The proposed quotient construction places every initial `R` edge within one quotient class. A path of such edges remains within that same quotient class, so transitive closure does not create an edge between distinct quotient classes.

For the minimal path:

```text
R(a,b)
R(b,c)
```

transitivity adds:

```text
R(a,c)
```

and all three elements are indistinguishable under the stated assumptions.

**Result:** No obstruction appears in this minimal test. The construction is a candidate alternative amalgam, subject to the same inducedness and embedding audit as II-2.

### Experiment II-4 — Transitivity plus positive apartness coupling

Constraint:

```text
C_R*:
R(x,y) -> x#y
```

For the minimal span:

```text
R(a,b)
R(b,c)
```

the coupling gives:

```text
a#b
b#c
```

Transitivity adds:

```text
R(a,c)
```

and the coupling then requires:

```text
a#c
```

This finite configuration is consistent with A1-A3. In particular, A3 does not force `a#c` from `a#b` and `b#c`, but it also does not prohibit `a#c`.

**Result:** The minimal test does not produce a contradiction and does not establish Class III.

A general amalgamation claim for `{T_R, C_R*}` has **not** been proved. A larger-span obstruction search and a construction audit remain necessary.

## 6. Corrections and methodological safeguards

1. The configuration `a~b, b~c, a#c` is inadmissible under frozen A1-A3 and classical Boolean logic. Do not use it as an S3-C3 counterexample.
2. Do not confuse failure of the free relational amalgam with failure of amalgamation.
3. Do not classify a constraint as Class II from one successful finite alternative construction. Class II requires a universal existence result over the specified admissible spans.
4. Do not classify a constraint as Class III without proving that every possible amalgam fails for at least one admissible span.
5. Coordinatewise `~`-invariance characterizes quotient descent, not arbitrary compatibility with all constraints.
6. Transitive closure must be checked against every other relation constraint and against embedding reflection.
7. Strong amalgamation and ordinary amalgamation must be tracked separately.
8. No unspecified S3-C3 coupling constraint may be silently assumed to belong to the frozen source.

## 7. Current status

### Source-recovered

- A1-A3 apartness framework.
- Equivalence of `~` under classical Boolean logic.
- Preserve-and-reflect requirement for apartness embeddings.
- P2.3 quotient-based strong apartness amalgam, under stated assumptions.
- Restricted P2.4.1 free relational amalgamation.
- Quotient-descent criterion for coordinatewise invariant relations.

### Conditional / requires proof audit

- Transitive-closure alternative amalgam for transitive quotient relations over induced common substructures.
- Its compatibility with the complete S3-C3 relational signature.
- Its preservation of all required embedding and strong-intersection properties.

### Open

- Exact S3-C3 relational signature and coupling constraints from primary sources.
- Formal decomposition/indecomposability definition for the exact S3-C3 task.
- Necessary-and-sufficient structural connectedness criterion.
- Minimal forbidden configurations for the actual constrained class.
- Any genuine Class III obstruction.
- Whether a proposed hypergraph criterion matches the original decomposition semantics.

## 8. Next justified actions

1. Recover the exact S3-C3 relation signature and all coupling constraints from the primary frozen sources.
2. Formalize the transitive-closure lemma with explicit hypotheses and a complete proof.
3. Test the positive-apartness case `{T_R, C_R*}` on larger spans, including paths that alternate between the two sides through the common substructure.
4. Check ordinary amalgamation and strong amalgamation separately.
5. Only then search for a minimal Class III obstruction.
6. Record missing source definitions explicitly rather than filling gaps by assumption.

## 9. Governance

```text
FROZEN CORE: UNCHANGED
NEW AXIOMS: NONE
VOLUME II / III / V: UNCHANGED
THEOREM REGISTRY: UNCHANGED
RL / CE / CE-V STATUS: UNCHANGED
S3-C3: RESEARCH IN PROGRESS
```

**End of temporary checkpoint.**