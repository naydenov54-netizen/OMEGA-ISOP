"""OMEGA-ISOP RL-027 S8.9-A assertion-completeness audit.

Supplemental checks only. The original S8.9 script is imported unchanged.
Colab: run from repository root with:
    python checkpoints/rl027_s8_adversarial_assertion_completeness.py

Dependencies: numpy, scipy (same as original S8.9 audit).
"""

from fractions import Fraction as F
import random
import numpy as np

import rl027_s8_adversarial_audit as original

# Explicit tolerances for floating-point MIN/QP and boundary checks.
MIN_PURITY_ATOL = 1e-10
FEASIBILITY_ATOL = 1e-10
NORMALIZATION_ATOL = 1e-12
ORDER_ATOL = 1e-10
NEGATIVITY_ATOL = 1e-12


def purity(q):
    return float(np.dot(np.asarray(q, dtype=float), np.asarray(q, dtype=float)))


def tv_distance(p, q):
    """Classical trace distance: 1/2 * L1 distance."""
    return 0.5 * float(np.sum(np.abs(
        np.asarray(p, dtype=float) - np.asarray(q, dtype=float)
    )))


def assert_float_spectrum(p, q, r, eta, label):
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    d = len(p)
    assert len(q) == d, f"{label}: wrong output dimension"
    assert abs(float(np.sum(q)) - 1.0) <= NORMALIZATION_ATOL, (
        f"{label}: normalization failure"
    )
    assert float(np.min(q)) >= -NEGATIVITY_ATOL, (
        f"{label}: negative component"
    )
    assert not np.any(np.abs(q[r:]) > NEGATIVITY_ATOL), (
        f"{label}: support exceeds rank r"
    )
    assert np.all(q[:r] >= -NEGATIVITY_ATOL), (
        f"{label}: negative supported component"
    )
    assert np.all(q[:r][:-1] + ORDER_ATOL >= q[:r][1:]), (
        f"{label}: supported spectrum is not non-increasing"
    )
    distance = tv_distance(p, q)
    assert distance <= float(eta) + FEASIBILITY_ATOL, (
        f"{label}: trace-distance infeasible: {distance} > {eta}"
    )
    return distance


def assert_exact_spectrum(p, q, r, eta, label):
    p = list(map(F, p))
    q = list(map(F, q))
    assert len(q) == len(p), f"{label}: wrong output dimension"
    assert sum(q) == 1, f"{label}: exact normalization failure"
    assert all(x >= 0 for x in q), f"{label}: negative component"
    assert all(x == 0 for x in q[r:]), f"{label}: support exceeds rank r"
    assert all(q[i] >= q[i+1] for i in range(r-1)), (
        f"{label}: supported spectrum is not non-increasing"
    )
    distance = sum(abs(p[i]-q[i]) for i in range(len(p))) / 2
    assert distance <= F(eta), (
        f"{label}: exact trace-distance infeasible: {distance} > {eta}"
    )
    return distance


def run_min_qp_supplement():
    rng = np.random.default_rng(20261126)
    cases = 2000
    max_abs_purity_error = 0.0
    max_formula_minus_qp = 0.0

    for case in range(cases):
        d = int(rng.integers(2, 9))
        r = int(rng.integers(1, d+1))
        p = np.sort(rng.dirichlet(np.ones(d)*0.7))[::-1]
        t = 1.0 - p[:r].sum()
        eta = t + (1.0-t)*float(rng.random())

        q_formula = original.min_formula(p, r, eta)
        result, q_qp = original.min_epigraph_qp(p, r, eta)

        assert q_formula is not None, f"MIN case {case}: formula infeasible"
        assert q_qp is not None, (
            f"MIN case {case}: QP failed: {getattr(result, 'message', None)}"
        )

        assert_float_spectrum(
            p, q_formula, r, eta, f"MIN formula case {case}"
        )
        # QP returns the r supported coordinates; pad with exact zeros.
        q_qp_full = np.r_[np.asarray(q_qp, dtype=float), np.zeros(d-r)]
        assert_float_spectrum(
            p, q_qp_full, r, eta, f"MIN QP case {case}"
        )

        formula_purity = purity(q_formula)
        qp_purity = purity(q_qp)
        error = abs(formula_purity-qp_purity)
        max_abs_purity_error = max(max_abs_purity_error, error)
        max_formula_minus_qp = max(
            max_formula_minus_qp, formula_purity-qp_purity
        )

        assert error <= MIN_PURITY_ATOL, (
            f"MIN case {case}: purity mismatch {error} exceeds "
            f"{MIN_PURITY_ATOL}"
        )
        # The formula must not be worse than the independently optimized QP
        # beyond the declared floating-point tolerance.
        assert formula_purity <= qp_purity + MIN_PURITY_ATOL, (
            f"MIN case {case}: formula purity exceeds QP objective"
        )

    return cases, max_abs_purity_error, max_formula_minus_qp


def run_max_exact_supplement():
    random.seed(20261126)
    cases = 0
    active_set_solutions = 0

    for d in range(2, 6):
        for r in range(1, d+1):
            for case in range(10):
                weights = [random.randint(1, 12) for _ in range(d)]
                total = sum(weights)
                p = sorted([F(w, total) for w in weights], reverse=True)
                t = F(1)-sum(p[:r])
                eta = t + (1-p[0]-t)*F(random.randint(0, 10), 10)

                q_formula = original.exact_max_formula(p, r, eta)
                q_vertex, count = original.exact_vertex_max(p, r, eta)

                assert q_formula is not None, "MAX formula unexpectedly infeasible"
                assert q_vertex is not None, "MAX vertex enumeration found no point"

                assert_exact_spectrum(
                    p, q_formula, r, eta, f"MAX formula d={d},r={r},case={case}"
                )
                assert_exact_spectrum(
                    p, q_vertex, r, eta, f"MAX vertex d={d},r={r},case={case}"
                )

                formula_value = sum(x*x for x in q_formula)
                vertex_value = sum(x*x for x in q_vertex)
                assert formula_value == vertex_value, (
                    f"MAX exact objective mismatch d={d},r={r},case={case}"
                )

                cases += 1
                active_set_solutions += count

    return cases, active_set_solutions


def run_boundary_supplement():
    cases = [
        ([F(3,10),F(1,4),F(1,5),F(3,20),F(1,10)], 2, F(9,20)),
        ([F(3,5),F(3,10),F(1,10)], 2, F(1,10)),
        ([F(7,10),F(1,10),F(1,10),F(1,10)], 2, F(1,5)),
        ([F(2,5),F(2,5),F(1,10),F(1,10)], 2, F(1,5)),
        ([F(1,4)]*4, 4, F(0)),
        ([F(1,2),F(1,2)], 2, F(0)),
        ([F(1,3)]*3, 1, F(2,3)),
    ]

    for index, (p, r, eta) in enumerate(cases):
        p = sorted(p, reverse=True)
        q_min = original.min_formula(p, r, float(eta))
        q_max = original.exact_max_formula(p, r, eta)

        assert q_min is not None, f"Boundary {index}: MIN infeasible"
        assert q_max is not None, f"Boundary {index}: MAX infeasible"

        assert_float_spectrum(
            p, q_min, r, eta, f"Boundary MIN {index}"
        )
        assert_exact_spectrum(
            p, q_max, r, eta, f"Boundary MAX {index}"
        )

        min_value = purity(q_min)
        max_value = sum(x*x for x in q_max)
        assert min_value <= float(max_value) + MIN_PURITY_ATOL, (
            f"Boundary {index}: MIN purity exceeds MAX purity"
        )

        # Independently verify exact trace distance for MAX and the
        # floating-point trace distance for MIN are both within eta.
        assert sum(abs(F(p[i])-q_max[i]) for i in range(len(p)))/2 <= eta

    return len(cases)


def main():
    min_cases, min_error, min_signed_gap = run_min_qp_supplement()
    max_cases, max_active = run_max_exact_supplement()
    boundary_cases = run_boundary_supplement()

    print("S8.9-A ASSERTION COMPLETENESS AUDIT")
    print("seed=20261126")
    print("MIN_cases=", min_cases)
    print("MIN_purity_atol=", MIN_PURITY_ATOL)
    print("MIN_max_abs_purity_error=", format(min_error, ".3e"))
    print("MIN_max_formula_minus_QP=", format(min_signed_gap, ".3e"))
    print("MAX_exact_cases=", max_cases)
    print("MAX_feasible_active_set_solutions=", max_active)
    print("boundary_cases=", boundary_cases)
    print("ASSERTED=normalization, nonnegativity, rank support, ordering,")
    print("         trace-distance feasibility, MIN/MAX purity ordering,")
    print("         MIN-QP objective agreement, exact MAX objective agreement")
    print("RESULT=ALL_SUPPLEMENTAL_ASSERTIONS_PASSED")
    print("NOTE=finite audit only; analytical proofs remain primary")


if __name__ == "__main__":
    main()
