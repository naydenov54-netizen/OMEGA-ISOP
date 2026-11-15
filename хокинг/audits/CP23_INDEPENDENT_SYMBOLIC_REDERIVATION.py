#!/usr/bin/env python3
"""Independent exact-symbolic Ricci reconstruction for OMEGA-ISOP CP-23.

This script is a separate audit calculation. It does not import the
production C++ MetricProvider, the reconstruction engine, or any external
symbolic oracle. It constructs the metric from the locked line element,
computes the inverse, Christoffel symbols, Riemann tensor and Ricci
contraction using the stated convention, then checks the exact fixture.
"""
import sympy as sp

T, x, theta, phi, q, Rm, c = sp.symbols(
    "T x theta phi q Rm c", positive=True, real=True
)
coordinates = [T, x, theta, phi]
D = x**2 - 2*q*x + q
B = D / x**2

metric = sp.diag(
    -B*c**2,
    Rm**2/B,
    Rm**2*x**2,
    Rm**2*x**2*sp.sin(theta)**2,
)
inverse_metric = sp.simplify(metric.inv())
dimension = 4

christoffel = [
    [[sp.Integer(0) for _ in range(dimension)]
     for _ in range(dimension)]
    for _ in range(dimension)
]
for rho in range(dimension):
    for mu in range(dimension):
        for nu in range(dimension):
            christoffel[rho][mu][nu] = sp.simplify(
                sum(
                    inverse_metric[rho, sigma] * (
                        sp.diff(metric[sigma, nu], coordinates[mu])
                        + sp.diff(metric[sigma, mu], coordinates[nu])
                        - sp.diff(metric[mu, nu], coordinates[sigma])
                    )
                    for sigma in range(dimension)
                ) / 2
            )

# R^rho_(sigma mu nu) =
# d_mu Gamma^rho_(nu sigma) - d_nu Gamma^rho_(mu sigma)
# + Gamma^rho_(mu lambda) Gamma^lambda_(nu sigma)
# - Gamma^rho_(nu lambda) Gamma^lambda_(mu sigma)
riemann = [
    [[[sp.Integer(0) for _ in range(dimension)]
       for _ in range(dimension)]
      for _ in range(dimension)]
    for _ in range(dimension)
]
for rho in range(dimension):
    for sigma in range(dimension):
        for mu in range(dimension):
            for nu in range(dimension):
                value = (
                    sp.diff(christoffel[rho][nu][sigma], coordinates[mu])
                    - sp.diff(christoffel[rho][mu][sigma], coordinates[nu])
                )
                value += sum(
                    christoffel[rho][mu][lam]
                    * christoffel[lam][nu][sigma]
                    - christoffel[rho][nu][lam]
                    * christoffel[lam][mu][sigma]
                    for lam in range(dimension)
                )
                riemann[rho][sigma][mu][nu] = sp.simplify(value)

ricci = sp.Matrix(
    dimension,
    dimension,
    lambda sigma, nu: sp.simplify(
        sum(riemann[rho][sigma][rho][nu] for rho in range(dimension))
    ),
)
ricci_scalar = sp.simplify(
    sum(
        inverse_metric[mu, nu] * ricci[mu, nu]
        for mu in range(dimension)
        for nu in range(dimension)
    )
)

expected = sp.diag(
    c**2*q*D/(Rm**2*x**6),
    -q/(x**2*D),
    q/x**2,
    q*sp.sin(theta)**2/x**2,
)
difference = ricci - expected
assert all(sp.simplify(difference[i, j]) == 0
           for i in range(dimension) for j in range(dimension))
assert ricci_scalar == 0

fixture = {
    q: sp.Rational(2, 5),
    Rm: sp.Integer(2),
    c: sp.Integer(3),
    x: sp.Integer(2),
    theta: sp.pi/3,
}
fixture_values = [sp.simplify(ricci[i, i].subs(fixture))
                  for i in range(dimension)]
assert fixture_values == [
    sp.Rational(63, 1600),
    -sp.Rational(1, 28),
    sp.Rational(1, 10),
    sp.Rational(3, 40),
]
assert sp.simplify(ricci_scalar.subs(fixture)) == 0

print("OMEGA-ISOP CP-23 INDEPENDENT SYMBOLIC RE-DERIVATION")
print("SymPy:", sp.__version__)
print("Riemann convention: locked CP-20 convention")
print("Ricci diagonal:")
for name, value in zip(("R_TT", "R_xx", "R_thetatheta", "R_phiphi"),
                       (ricci[i, i] for i in range(dimension))):
    print(f"{name} = {sp.factor(value)}")
print("Off-diagonal Ricci components: all exactly zero")
print("Ricci scalar:", ricci_scalar)
print("Exact fixture:", fixture_values)
print("Fixture Ricci scalar:", sp.simplify(ricci_scalar.subs(fixture)))
print("RESULT: PASS")
