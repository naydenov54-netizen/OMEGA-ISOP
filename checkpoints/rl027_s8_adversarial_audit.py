"""OMEGA-ISOP RL-027 S8 adversarial audit.
Colab dependencies: numpy, scipy.
Checks MIN with an epigraph QP formulation and MAX by exact
rational vertex enumeration for small dimensions.
"""

from fractions import Fraction as F
from itertools import combinations
import random
import numpy as np
from scipy.optimize import minimize, LinearConstraint, Bounds


def min_formula(p, r, eta):
    p = np.array(sorted(p, reverse=True), dtype=float)
    d = len(p)
    t = 1.0 - p[:r].sum()
    if eta < t - 1e-12:
        return None

    eps = eta - t
    u = 1.0 / r
    eps_uniform = np.maximum(p[:r] - u, 0.0).sum()

    if eps >= eps_uniform - 1e-12:
        return np.r_[np.full(r, u), np.zeros(d-r)]

    if eps <= 1e-14:
        alpha = np.inf
    else:
        lo, hi = 0.0, p[0]
        for _ in range(100):
            mid = (lo + hi) / 2
            if np.maximum(p[:r] - mid, 0.0).sum() > eps:
                lo = mid
            else:
                hi = mid
        alpha = (lo + hi) / 2

    target = t + eps
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if np.maximum(mid - p[:r], 0.0).sum() < target:
            lo = mid
        else:
            hi = mid
    beta = (lo + hi) / 2

    return np.r_[np.clip(p[:r], beta, alpha), np.zeros(d-r)]


def min_epigraph_qp(p, r, eta):
    p = np.array(sorted(p, reverse=True), dtype=float)
    t = 1.0 - p[:r].sum()
    eps = eta - t
    if eps < -1e-10:
        return None, None

    # x=(q_1,...,q_r,s_1,...,s_r)
    # s_i >= p_i-q_i; s_i>=0; sum(s_i)<=eps.
    n = 2*r
    Aeq = np.zeros((1, n))
    Aeq[0, :r] = 1.0

    A = np.zeros((r+1, n))
    for i in range(r):
        A[i, i] = 1.0
        A[i, r+i] = 1.0
    A[r, r:] = 1.0

    lower = np.r_[p[:r], -np.inf]
    upper = np.r_[np.full(r, np.inf), eps]

    constraints = [
        LinearConstraint(Aeq, [1.0], [1.0]),
        LinearConstraint(A, lower, upper)
    ]

    x0 = np.r_[np.full(r, 1.0/r), np.maximum(p[:r]-1.0/r, 0.0)]

    result = minimize(
        lambda x: np.dot(x[:r], x[:r]),
        x0,
        jac=lambda x: np.r_[2.0*x[:r], np.zeros(r)],
        method="SLSQP",
        bounds=Bounds(np.zeros(n), np.full(n, np.inf)),
        constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 2000}
    )

    if not result.success:
        return result, None
    return result, result.x[:r]


def solve_fractional(A, b):
    n = len(b)
    M = [
        [F(x) for x in row] + [F(rhs)]
        for row, rhs in zip(A, b)
    ]

    for col in range(n):
        pivot = next(
            (i for i in range(col, n) if M[i][col] != 0),
            None
        )
        if pivot is None:
            return None

        M[col], M[pivot] = M[pivot], M[col]
        scale = M[col][col]
        M[col] = [x/scale for x in M[col]]

        for i in range(n):
            if i == col:
                continue
            factor = M[i][col]
            if factor:
                M[i] = [
                    M[i][j] - factor*M[col][j]
                    for j in range(n+1)
                ]

    return [M[i][-1] for i in range(n)]


def exact_max_formula(p, r, eta):
    p = list(map(F, p))
    d = len(p)
    t = F(1) - sum(p[:r])
    eta = F(eta)

    if eta < t:
        return None
    if eta >= 1-p[0]:
        return [F(1)] + [F(0)]*(d-1)

    eps = eta-t
    q = [F(0)]*d
    q[0] = p[0]+eta
    remaining = eps

    for i in range(r-1, 0, -1):
        take = min(p[i], remaining)
        q[i] = p[i]-take
        remaining -= take

    assert remaining == 0
    return q


def exact_vertex_max(p, r, eta):
    p = list(map(F, p))
    t = F(1)-sum(p[:r])
    eps = F(eta)-t

    if eps < 0:
        return None, 0

    # Polytope inequalities:
    # q_i>=0 and sum_{i in S}(p_i-q_i)<=eps for every S.
    rows, rhs = [], []

    for i in range(r):
        a = [F(0)]*r
        a[i] = F(-1)
        rows.append(a)
        rhs.append(F(0))

    for mask in range(1 << r):
        a = [F(0)]*r
        ps = F(0)
        for i in range(r):
            if mask >> i & 1:
                a[i] = F(-1)
                ps += p[i]
        rows.append(a)
        rhs.append(eps-ps)

    best_value = None
    best_q = None
    vertex_count = 0

    for active in combinations(range(len(rows)), r-1):
        A = [[F(1)]*r] + [rows[j] for j in active]
        b = [F(1)] + [rhs[j] for j in active]
        q = solve_fractional(A, b)

        if q is None:
            continue

        feasible = True
        for row, bound in zip(rows, rhs):
            if sum(row[i]*q[i] for i in range(r)) > bound:
                feasible = False
                break

        if not feasible or any(x < 0 for x in q):
            continue

        vertex_count += 1
        value = sum(x*x for x in q)

        if best_value is None or value > best_value:
            best_value = value
            best_q = q

    return best_q, vertex_count


def boundary_tests():
    cases = [
        ([F(3,10),F(1,4),F(1,5),F(3,20),F(1,10)], 2, F(9,20)),
        ([F(3,5),F(3,10),F(1,10)], 2, F(1,10)),
        ([F(7,10),F(1,10),F(1,10),F(1,10)], 2, F(1,5)),
        ([F(2,5),F(2,5),F(1,10),F(1,10)], 2, F(1,5)),
        ([F(1,4)]*4, 4, F(0)),
        ([F(1,2),F(1,2)], 2, F(0)),
        ([F(1,3)]*3, 1, F(2,3)),
    ]

    for p, r, eta in cases:
        p = sorted(p, reverse=True)
        qlo = min_formula(p, r, float(eta))
        qhi = exact_max_formula(p, r, eta)

        assert qlo is not None and qhi is not None
        assert abs(sum(qlo)-1.0) < 1e-12
        assert all(x >= -1e-12 for x in qlo)
        assert sum(qhi) == 1
        assert all(x >= 0 for x in qhi)

    return len(cases)


def main():
    rng = np.random.default_rng(20261126)

    # Independent MIN comparison using linear epigraph constraints.
    min_cases = 2000
    min_success = 0
    min_max_error = 0.0

    for _ in range(min_cases):
        d = int(rng.integers(2, 9))
        r = int(rng.integers(1, d+1))
        p = np.sort(rng.dirichlet(np.ones(d)*0.7))[::-1]
        t = 1.0-p[:r].sum()
        eta = t+(1.0-t)*float(rng.random())

        q_formula = min_formula(p, r, eta)
        result, q_qp = min_epigraph_qp(p, r, eta)

        if q_qp is None:
            raise AssertionError(
                "MIN epigraph solver failed: "+str(result.message)
            )

        min_success += 1
        error = abs(
            np.dot(q_formula[:r], q_formula[:r])
            - np.dot(q_qp, q_qp)
        )
        min_max_error = max(min_max_error, error)

    # Exact MAX vertex enumeration for small dimensions.
    random.seed(20261126)
    max_cases = 0
    vertices_checked = 0

    for d in range(2, 6):
        for r in range(1, d+1):
            for _ in range(10):
                weights = [random.randint(1, 12) for _ in range(d)]
                total = sum(weights)
                p = sorted(
                    [F(w, total) for w in weights],
                    reverse=True
                )
                t = F(1)-sum(p[:r])
                eta = t+(1-p[0]-t)*F(
                    random.randint(0, 10), 10
                )

                q_formula = exact_max_formula(p, r, eta)
                q_vertex, count = exact_vertex_max(p, r, eta)

                assert q_vertex is not None
                assert sum(x*x for x in q_formula[:r]) == sum(
                    x*x for x in q_vertex
                )

                max_cases += 1
                vertices_checked += count

    boundaries = boundary_tests()

    print("S8 ADVERSARIAL AUDIT")
    print("seed=20261126")
    print("MIN_epigraph_QP_cases=", min_cases)
    print("MIN_epigraph_QP_successes=", min_success)
    print("MIN_max_abs_purity_error=", format(min_max_error, ".3e"))
    print("MAX_exact_vertex_cases=", max_cases)
    print("MAX_exact_vertices_checked=", vertices_checked)
    print("boundary_and_degeneracy_cases=", boundaries)
    print("RESULT=ALL_ASSERTIONS_PASSED")
    print("NOTE=finite computational audit; analytical proofs remain primary")


if __name__ == "__main__":
    main()
