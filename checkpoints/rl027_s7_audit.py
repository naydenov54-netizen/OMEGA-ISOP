r"""
OMEGA-ISOP RL-027 S7 — НЕЗАВИСИМ МАТЕМАТИЧЕСКИ И ЧИСЛЕН ОДИТ (2026-11-26)
Файл: rl027_s7_audit.py
"""

import itertools, math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize

def check_input(p, eta):
    p = np.asarray(p, dtype=float)
    if p.ndim != 1 or p.size == 0 or not np.all(np.isfinite(p)):
        raise ValueError("p: непразен краен вектор")
    if p.min() < 0 or abs(math.fsum(p) - 1) > 1e-9:
        raise ValueError("p не е вероятностен вектор")
    if not (math.isfinite(eta) and eta >= 0):
        raise ValueError("eta >= 0")
    return p

def tv(p, q):
    return 0.5 * math.fsum(abs(a - b) for a, b in zip(p, q))

def purity(q):
    return math.fsum(x * x for x in q)

def solve_min(p, eta, one):
    n = len(p); u = one / n
    if sum((x - u for x in p if x > u), 0 * one) <= eta:
        return [u] * n
    if eta == 0:
        return list(p)
    d = sorted(p, reverse=True); s = 0 * one
    for k in range(1, n):
        s += d[k-1]; alpha = (s - eta) / k
        if alpha >= d[k]:
            break
    a = d[::-1]; s = 0 * one
    for k in range(1, n):
        s += a[k-1]; beta = (s + eta) / k
        if beta <= a[k]:
            break
    return [min(max(x, beta), alpha) for x in p]

def solve_max(p, eta, one):
    n = len(p); q = list(p)
    top = max(range(n), key=lambda i: p[i])
    delta = min(eta, one - p[top])
    q[top] += delta
    rest = delta
    for i in sorted((i for i in range(n) if i != top), key=lambda i: p[i]):
        take = min(q[i], rest)
        q[i] -= take; rest -= take
        if rest <= 0:
            break
    return q

def min_purity(p, eta):
    p = check_input(p, eta)
    return np.array(solve_min([float(x) for x in p], float(eta), 1.0))

def max_purity(p, eta):
    p = check_input(p, eta)
    return np.array(solve_max([float(x) for x in p], float(eta), 1.0))

def audit(p, eta, qmin, qmax, tol=1e-12):
    p = list(p)
    return {
      "A1_nonneg": min(min(qmin), min(qmax)) >= -tol,
      "A2_norm": max(abs(math.fsum(qmin)-1), abs(math.fsum(qmax)-1)) <= tol,
      "A3_tv_min": tv(p, qmin) <= eta + tol,
      "A4_tv_max": tv(p, qmax) <= eta + tol,
      "A5_order": purity(qmin) <= purity(p)+tol and purity(p) <= purity(qmax)+tol,
    }

def eta_cert(p, e, q):
    u = F(1, len(p))
    if all(x == u for x in q):
        return sum(abs(a-u) for a in p) <= 2*e
    inner = sum(b*(a-b) for a, b in zip(p, q))
    return inner == e * (max(q)-min(q))

def exact_case(w, e):
    S = sum(w); p = [F(x, S) for x in w]; n = len(p)
    lo = solve_min(p, e, F(1)); hi = solve_max(p, e, F(1))
    for q in (lo, hi):
        assert sum(q) == 1 and min(q) >= 0
        assert sum(abs(a-b) for a, b in zip(p, q)) <= 2*e
    assert eta_cert(p, e, lo)
    P = F(0); Q = F(0)
    for a, b in zip(sorted(p, reverse=True), sorted(hi, reverse=True)):
        P += a; Q += b
        assert Q == min(P + e, F(1))

def oracle_min(p, eta):
    n = len(p)
    f = lambda z: np.sum((p + z[:n] - z[n:])**2)
    g = lambda z: np.r_[2*(p + z[:n] - z[n:]), -2*(p + z[:n] - z[n:])]
    cons = [
      {"type":"eq","fun":lambda z: z[:n].sum()-z[n:].sum(), "jac":lambda z: np.r_[np.ones(n),-np.ones(n)]},
      {"type":"ineq","fun":lambda z: 2*eta - z.sum(), "jac":lambda z: -np.ones(2*n)},
      {"type":"ineq","fun":lambda z: p + z[:n] - z[n:], "jac":lambda z: np.c_[np.eye(n),-np.eye(n)]}]
    return minimize(f, np.zeros(2*n), jac=g, bounds=[(0,1)]*(2*n), constraints=cons,
                    method="SLSQP", options={"ftol":1e-15,"maxiter":1000})

def vertex_systems(n):
    signs = np.array(list(itertools.product((-1,1), repeat=n)), float)
    A = np.vstack([-np.eye(n), signs])
    idx = np.array(list(itertools.combinations(range(len(A)), n-1)))
    M = np.concatenate([np.ones((len(idx),1,n)), A[idx]], axis=1)
    good = np.abs(np.linalg.det(M)) > 0.5
    return signs, A, idx[good], np.linalg.inv(M[good])

def oracle_vertices(p, eta, sys_):
    signs, A, idx, inv = sys_
    b = np.r_[np.zeros(len(p)), 2*eta + signs @ p]
    rhs = np.concatenate([np.ones((len(idx),1)), b[idx]], axis=1)
    V = np.einsum("kij,kj->ki", inv, rhs)
    V = V[np.all(V @ A.T <= b + 1e-10, axis=1)]
    pur = (V**2).sum(1)
    return pur.min(), pur.max()

def random_p(rng, n):
    kind = rng.integers(6)
    p = rng.dirichlet(np.ones(n) * rng.choice([0.1,0.5,1,5]))
    if kind == 1: p = np.ones(n)
    if kind == 2: p = np.eye(n)[rng.integers(n)]
    if kind == 3: p = rng.integers(1,4,n).astype(float)
    if kind == 4 and n > 1: p[rng.choice(n, n//2, replace=False)] = 0
    s = p.sum()
    p = p/s if s > 0 else np.eye(n)[0]
    return rng.permutation(p)

def random_eta(rng, p):
    u = tv(p, np.ones(len(p))/len(p))
    return float(rng.choice([0.0, rng.uniform(0,0.2), rng.uniform(0,1.2), u,
                             max(u-1e-9,0), u+1e-9, 1-p.max()]))

def main():
    rng = np.random.default_rng(20261126)
    p = np.array([0.61370612,0.12481632,0.11683150,0.08137840,0.06239827,0.00086939])
    eta = 0.09344593349461805
    uni = np.ones(6)/6
    lo, hi = min_purity(p,eta), max_purity(p,eta)
    np.set_printoptions(precision=12, suppress=True, linewidth=100)
    print("sum p =", repr(math.fsum(p)))
    print("TV(p,uniform) =", repr(tv(p,uni)), "excess =", repr(tv(p,uni)-eta))
    print("q_min =", lo.tolist()); print("q_max =", hi.tolist())
    print("TV min/max =", tv(p,lo), tv(p,hi))
    print("purity min/p/max =", purity(lo), purity(p), purity(hi), "uniform", purity(uni))
    print("audit new     :", audit(p,eta,lo,hi))
    print("audit reported:", audit(p,eta,uni,hi))

    edges = [([1.0],0),([1.0],0.7),([0.25]*4,0),([0.25]*4,0.1),([0.25]*4,2),
             ([1,0,0],0),([1,0,0],0.2),([1,0,0],2/3),([1,0,0],1),([.4,.4,.1,.1],0.1),
             ([.5,.5,0,0],0.2),([.7,.3,0],0.3),(p,0),(p,tv(p,uni)),(p,1)]
    bad = 0
    for pp, e in edges:
        pp = np.array(pp,float); a, b = min_purity(pp,e), max_purity(pp,e)
        r = audit(pp,e,a,b); bad += not all(r.values())
        print("edge p=",np.round(pp,6).tolist(),"eta=",round(float(e),6),"min=",np.round(a,6).tolist(),
              "max=",np.round(b,6).tolist(),"OK" if all(r.values()) else r)
    print("edge FAIL =", bad, "/", len(edges))

    N=100000; fails={}; worst=0.0
    for _ in range(N):
        n = int(rng.integers(1,31)); pp = random_p(rng,n); e = random_eta(rng,pp)
        a,b = min_purity(pp,e), max_purity(pp,e)
        for k,v in audit(pp,e,a,b).items():
            if not v: fails[k]=fails.get(k,0)+1
        worst = max(worst, tv(pp,a)-e, tv(pp,b)-e)
    print("T1", N, "fails:", fails, "max TV excess:", worst)

    N=20000
    for _ in range(N):
        n = int(rng.integers(1,13))
        w = [int(x) for x in rng.integers(0, int(rng.choice([2,4,1000])), n)]
        if sum(w)==0: w[0]=1
        exact_case(w, F(int(rng.integers(0,1201)),1000))
    print("T2", N, "exact: all assertions passed")

    N=3000; err_max=0.0; below=0.0
    cache={n:vertex_systems(n) for n in range(2,6)}
    for _ in range(N):
        n=int(rng.integers(2,6)); pp=random_p(rng,n); e=float(rng.uniform(0.001,1.0))
        vmin,vmax = oracle_vertices(pp,e,cache[n])
        err_max=max(err_max, abs(vmax-purity(max_purity(pp,e))))
        below=max(below, purity(min_purity(pp,e))-vmin)
    print("T3", N, "max |oracle_max - ours| =", err_max, " ours_min - min_vertex <=", below)

    N=3000; gap=0.0; better=0.0; nofail=0
    for _ in range(N):
        n=int(rng.integers(2,11)); pp=random_p(rng,n); e=float(rng.uniform(0.001,0.8))
        r=oracle_min(pp,e)
        if not r.success: nofail+=1; continue
        ours=purity(min_purity(pp,e))
        gap=max(gap, abs(r.fun-ours)); better=max(better, ours-r.fun)
    print("T4", N, "solver non-converged:", nofail, "max |diff| =", gap, "max (ours - solver) =", better)

    N=20000; viol=0.0; kept=0
    for _ in range(N):
        n=int(rng.integers(2,7)); pp=random_p(rng,n)
        G=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n))
        tau=G@G.conj().T; tau/=np.trace(tau).real
        t=rng.uniform()**2
        sig=(1-t)*np.diag(pp)+t*tau
        e=0.5*np.abs(np.linalg.eigvalsh(sig-np.diag(pp))).sum()
        pur=np.trace(sig@sig).real; kept+=1
        viol=max(viol, purity(min_purity(pp,e))-pur, pur-purity(max_purity(pp,e)))
    print("T5", kept, "max bound violation =", viol)

if __name__=="__main__":
    main()
