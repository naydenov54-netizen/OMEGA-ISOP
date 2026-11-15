#!/usr/bin/env python3
"""OMEGA-ISOP CP-22 independent symbolic reconstruction.

Sole mathematical source: хокинг/00_ARCHIVE_2026-11-14.txt, section III-B.3.
No imports from CP-23, legacy oracle files, production C++, or MetricProvider.
Uses exact SymPy expressions and the archive's fixed Riemann convention.
"""
import sympy as sp

T, x, theta, phi, q, Rm, c = sp.symbols(
    "T x theta phi q Rm c", positive=True, real=True
)
coordinates = (T, x, theta, phi)
n = 4
D = x**2 - 2*q*x + q
B = D/x**2

# CP22-03: reconstruct the metric directly from the archived line element.
g = sp.diag(
    -B*c**2,
    Rm**2/B,
    Rm**2*x**2,
    Rm**2*x**2*sp.sin(theta)**2,
)
g_inv = sp.simplify(g.inv())
identity = sp.simplify(g*g_inv - sp.eye(n))
assert identity == sp.zeros(n)

# CP22-05: general Christoffel definition, all ordered components.
Gamma = [[[
    sp.factor(sum(
        g_inv[rho, sig] * (
            sp.diff(g[sig, nu], coordinates[mu])
            + sp.diff(g[sig, mu], coordinates[nu])
            - sp.diff(g[mu, nu], coordinates[sig])
        )
        for sig in range(n)
    ) / 2)
    for nu in range(n)] for mu in range(n)] for rho in range(n)]
nonzero_gamma = [
    (r, m, v) for r in range(n) for m in range(n) for v in range(n)
    if Gamma[r][m][v] != 0
]
assert all(sp.simplify(Gamma[r][m][v] - Gamma[r][v][m]) == 0
           for r in range(n) for m in range(n) for v in range(n))
independent_gamma = {
    (r, min(m, v), max(m, v)) for r, m, v in nonzero_gamma
}
expected_gamma = {
    (0, 0, 1): q*(x-1)/(x*D),
    (1, 0, 0): c**2*q*(x-1)*D/(Rm**2*x**5),
    (1, 1, 1): -q*(x-1)/(x*D),
    (1, 2, 2): -D/x,
    (1, 3, 3): -D*sp.sin(theta)**2/x,
    (2, 1, 2): 1/x,
    (3, 1, 3): 1/x,
    (2, 3, 3): -sp.sin(theta)*sp.cos(theta),
    (3, 2, 3): sp.cos(theta)/sp.sin(theta),
}
assert len(independent_gamma) == len(expected_gamma) == 9
for (rho, mu, nu), expected in expected_gamma.items():
    assert sp.simplify(Gamma[rho][mu][nu] - expected) == 0
assert all(
    Gamma[rho][mu][nu] == 0
    for rho in range(n) for mu in range(n) for nu in range(n)
    if (rho, min(mu, nu), max(mu, nu)) not in expected_gamma
)

# CP22-06: fixed archive convention, R^rho_(sigma mu nu).
Riemann = [[[[sp.Integer(0) for _ in range(n)] for _ in range(n)]
            for _ in range(n)] for _ in range(n)]
for rho in range(n):
    for sigma in range(n):
        for mu in range(n):
            for nu in range(n):
                value = (
                    sp.diff(Gamma[rho][nu][sigma], coordinates[mu])
                    - sp.diff(Gamma[rho][mu][sigma], coordinates[nu])
                )
                value += sum(
                    Gamma[rho][mu][lam] * Gamma[lam][nu][sigma]
                    - Gamma[rho][nu][lam] * Gamma[lam][mu][sigma]
                    for lam in range(n)
                )
                Riemann[rho][sigma][mu][nu] = sp.factor(value)

nonzero_riemann = sum(
    Riemann[r][s][m][v] != 0
    for r in range(n) for s in range(n)
    for m in range(n) for v in range(n)
)
assert all(
    sp.simplify(Riemann[r][s][m][v] + Riemann[r][s][v][m]) == 0
    for r in range(n) for s in range(n)
    for m in range(n) for v in range(n)
)

# CP22-06/10: algebraic first Bianchi identity, all 256 index tuples.
algebraic_bianchi_checks = 0
for rho in range(n):
    for sigma in range(n):
        for mu in range(n):
            for nu in range(n):
                value = sp.simplify(
                    Riemann[rho][sigma][mu][nu]
                    + Riemann[rho][mu][nu][sigma]
                    + Riemann[rho][nu][sigma][mu]
                )
                assert value == 0, (rho, sigma, mu, nu, value)
                algebraic_bianchi_checks += 1

# CP22-07: Ricci contraction R_sigma_nu = R^rho_(sigma rho nu).
Ricci = sp.Matrix(n, n, lambda sigma, nu: sp.factor(sum(
    Riemann[rho][sigma][rho][nu] for rho in range(n)
)))
expected_ricci = sp.diag(
    c**2*q*D/(Rm**2*x**6),
    -q/(x**2*D),
    q/x**2,
    q*sp.sin(theta)**2/x**2,
)
assert all(sp.simplify(Ricci[i, j] - expected_ricci[i, j]) == 0
           for i in range(n) for j in range(n))

# CP22-08: Ricci scalar.
Ricci_scalar = sp.factor(sum(
    g_inv[mu, nu] * Ricci[mu, nu]
    for mu in range(n) for nu in range(n)
))
assert sp.simplify(Ricci_scalar) == 0

# CP22-09: Einstein tensor and mixed components.
Einstein = sp.simplify(Ricci - sp.Rational(1, 2)*g*Ricci_scalar)
assert all(sp.simplify(Einstein[i, j] - Ricci[i, j]) == 0
           for i in range(n) for j in range(n))
Einstein_mixed = sp.simplify(g_inv*Einstein)
expected_mixed = sp.diag(
    -q/(Rm**2*x**4), -q/(Rm**2*x**4),
    q/(Rm**2*x**4), q/(Rm**2*x**4)
)
assert all(sp.simplify(Einstein_mixed[i, j] - expected_mixed[i, j]) == 0
           for i in range(n) for j in range(n))

# CP22-10: differential Bianchi identity.
# For a (1,3) tensor:
# nabla_l R^r_(s m n) = partial_l R + Gamma^r_lk R^k
# - Gamma^k_ls R^r_k - Gamma^k_lm R^r_(s k n)
# - Gamma^k_ln R^r_(s m k).
def covariant_derivative_riemann(lam, rho, sigma, mu, nu):
    value = sp.diff(Riemann[rho][sigma][mu][nu], coordinates[lam])
    value += sum(Gamma[rho][lam][k] * Riemann[k][sigma][mu][nu]
                 for k in range(n))
    value -= sum(Gamma[k][lam][sigma] * Riemann[rho][k][mu][nu]
                 for k in range(n))
    value -= sum(Gamma[k][lam][mu] * Riemann[rho][sigma][k][nu]
                 for k in range(n))
    value -= sum(Gamma[k][lam][nu] * Riemann[rho][sigma][mu][k]
                 for k in range(n))
    return sp.factor(value)

differential_bianchi_checks = 0
for rho in range(n):
    for sigma in range(n):
        for lam in range(n):
            for mu in range(n):
                for nu in range(n):
                    value = sp.simplify(
                        covariant_derivative_riemann(
                            lam, rho, sigma, mu, nu
                        )
                        + covariant_derivative_riemann(
                            mu, rho, sigma, nu, lam
                        )
                        + covariant_derivative_riemann(
                            nu, rho, sigma, lam, mu
                        )
                    )
                    assert value == 0, (rho, sigma, lam, mu, nu, value)
                    differential_bianchi_checks += 1

# CP22-11: dimensional audit. Exponents are ordered (L, T, M).
# [x]=[theta]=[phi]=[q]=1, [Rm]=L, [c]=L/T, [G_N]=L^3 M^-1 T^-2.
L = (1, 0, 0)
TIME = (0, 1, 0)
DIMENSIONLESS = (0, 0, 0)
def add(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(3))
def scale(k, vector):
    return tuple(k*v for v in vector)
c_dim = add(L, scale(-1, TIME))
rm_dim = L
gn_dim = (3, -2, -1)  # ordered (L,T,M)
rho_dim = (-1, -2, 1) # pressure / energy density
assert add(scale(4, c_dim), scale(-1, gn_dim), scale(-2, rm_dim)) == rho_dim
assert add(scale(4, c_dim), scale(2, rm_dim), scale(-1, gn_dim)) == (3, -2, 1)
assert add(scale(-2, rm_dim)) == (-2, 0, 0)  # [R] and mixed curvature
assert add(scale(2, c_dim)) == (2, -2, 0)  # [g_TT] = L^2/T^2
assert scale(2, rm_dim) == (2, 0, 0)       # spatial/angular metric entries
assert add(scale(2, c_dim), scale(-2, rm_dim)) == (0, -2, 0)

# Exact diagnostic fixture from the archive.
fixture = {
    q: sp.Rational(2, 5), Rm: sp.Integer(2), c: sp.Integer(3),
    x: sp.Integer(2), theta: sp.pi/3,
}
fixture_ricci = [sp.simplify(Ricci[i, i].subs(fixture)) for i in range(n)]
assert fixture_ricci == [
    sp.Rational(63, 1600), -sp.Rational(1, 28),
    sp.Rational(1, 10), sp.Rational(3, 40)
]

print("OMEGA-ISOP CP-22 INDEPENDENT SYMBOLIC RECONSTRUCTION")
print("SOURCE: хокинг/00_ARCHIVE_2026-11-14.txt, III-B.3 only")
print("SymPy:", sp.__version__)
print("Metric inverse identity: PASS (16 component equations)")
print("Christoffel nonzero ordered components:", len(nonzero_gamma))
print("Christoffel independent under lower-index symmetry:",
      len(independent_gamma), "(exact 9-component archive match PASS)")
print("Riemann nonzero ordered components:", nonzero_riemann)
print("Riemann last-index antisymmetry: 256 / 256 PASS")
print("Algebraic Bianchi identity:", algebraic_bianchi_checks, "/ 256 PASS")
print("Ricci tensor: exact component identity PASS")
print("Ricci scalar:", Ricci_scalar)
print("Einstein tensor and mixed components: exact identity PASS")
print("Differential Bianchi identity:",
      differential_bianchi_checks, "/ 1024 PASS")
print("Dimensional audit: PASS")
print("  [g_TT]=L^2/T^2; [g_xx]=[g_theta_theta]=[g_phi_phi]=L^2")
print("  [R]=[G^mu_nu]=L^-2; [R_TT]=T^-2; spatial Ricci covariant components dimensionless")
print("  [rho]=[p_r]=[p_t]=M/(L*T^2)")
print("  [c^4/(G_N*Rm^2)]=M/(L*T^2)")
print("  [C*r0^2] required by rho formula = M*L^3/T^2")
print("Exact fixture:", fixture_ricci)
print("ENERGY NORMALIZATION C*r0^2: NOT CLOSED; primary definitions absent")
print("RESULT: PASS FOR CP22-03 THROUGH CP22-11 SYMBOLIC/DIMENSIONAL SCOPE")
