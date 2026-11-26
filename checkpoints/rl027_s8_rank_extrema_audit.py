"""OMEGA-ISOP RL-027 S8.5-S8.6 exact rational audit.
Run: python rl027_s8_rank_extrema_audit.py
Uses only Python standard library.
"""
from fractions import Fraction as F
import random

def solve_min(p, r, eta):
    d = len(p)
    t = F(1) - sum(p[:r])
    if eta < t:
        return None
    eps = eta - t
    u = F(1, r)
    eps_uniform = sum((x-u for x in p[:r] if x > u), F(0))
    if eps >= eps_uniform:
        return [u]*r + [F(0)]*(d-r)

    if eps == 0:
        alpha = max(p[:r])
    else:
        alpha = None
        for k in range(1, r+1):
            a = (sum(p[:k])-eps)/k
            if a <= p[k-1] and (k == r or a >= p[k]):
                alpha = a
                break
        if alpha is None:
            raise AssertionError("alpha active-set search failed")

    target = t + eps
    if target == 0:
        beta = min(p[:r])
    else:
        beta = None
        for ell in range(1, r+1):
            b = (sum(p[r-ell:r])+target)/ell
            if b >= p[r-ell] and (r-ell == 0 or b <= p[r-ell-1]):
                beta = b
                break
        if beta is None:
            raise AssertionError("beta active-set search failed")

    return [min(max(x,beta),alpha) for x in p[:r]] + [F(0)]*(d-r)

def solve_max(p, r, eta):
    d = len(p)
    t = F(1)-sum(p[:r])
    if eta < t:
        return None
    if eta >= 1-p[0]:
        return [F(1)]+[F(0)]*(d-1)
    eps = eta-t
    q = [F(0)]*d
    q[0] = p[0]+eta
    remaining = eps
    for i in range(r-1,0,-1):
        take = min(p[i],remaining)
        q[i] = p[i]-take
        remaining -= take
    assert remaining == 0
    return q

def tv(p,q):
    return sum(abs(a-b) for a,b in zip(p,q))/2

def purity(q):
    return sum(x*x for x in q)

def check_case(p,r,eta):
    p=sorted(p,reverse=True)
    assert sum(p)==1 and all(x>=0 for x in p)
    t=F(1)-sum(p[:r])
    qlo=solve_min(p,r,eta)
    qhi=solve_max(p,r,eta)
    if eta<t:
        assert qlo is None and qhi is None
        return 0
    assert qlo is not None and qhi is not None
    for q in (qlo,qhi):
        assert all(x>=0 for x in q)
        assert sum(q)==1
        assert all(x==0 for x in q[r:])
        assert tv(p,q)<=eta

    # Exact MIN threshold identities, except the uniform branch.
    eps=eta-t
    u=F(1,r)
    eps_u=sum((x-u for x in p[:r] if x>u),F(0))
    if eps>=eps_u:
        assert qlo[:r]==[u]*r
    else:
        assert sum((p[i]-qlo[i] for i in range(r) if p[i]>qlo[i]),F(0))==eps
        assert sum((qlo[i]-p[i] for i in range(r) if qlo[i]>p[i]),F(0))==t+eps

    # Exact MAX majorization certificate.
    partial=F(0)
    for k in range(1,r+1):
        partial += qhi[k-1]
        assert partial == min(F(1),sum(p[:k])+eta)

    # The MIN cannot exceed any feasible test point; the MAX cannot be
    # exceeded by any feasible test point. Random points are checks, not proof.
    samples=0
    for _ in range(8):
        weights=[random.randint(0,30) for _ in range(r)]
        if sum(weights)==0:
            weights[0]=1
        z0=[F(w,sum(weights)) for w in weights]+[F(0)]*(len(p)-r)
        if tv(p,z0)<=eta:
            assert purity(qlo)<=purity(z0)
            assert purity(z0)<=purity(qhi)
            samples+=1
    return samples

def main():
    random.seed(20261126)
    N=20000
    feasible_samples=0
    for _ in range(N):
        d=random.randint(1,10)
        r=random.randint(1,d)
        weights=[random.randint(0,100) for _ in range(d)]
        if sum(weights)==0:
            weights[0]=1
        total=sum(weights)
        p=[F(w,total) for w in weights]
        p.sort(reverse=True)
        # Include random eta and the exact rank-feasibility boundary.
        eta_options=[F(random.randint(0,1200),1000),
                     F(1)-sum(p[:r]),
                     max(F(0),F(1)-sum(p[:r])-F(1,1000))]
        for eta in eta_options:
            feasible_samples += check_case(p,r,eta)
    print("S8.5-S8.6 EXACT RATIONAL AUDIT")
    print("seed=20261126")
    print("base_cases=",N)
    print("eta_cases=",3*N)
    print("random_feasible_comparisons=",feasible_samples)
    print("RESULT=ALL_ASSERTIONS_PASSED")
    print("NOTE=finite tests; not a substitute for the analytical proofs")

if __name__=="__main__":
    main()
