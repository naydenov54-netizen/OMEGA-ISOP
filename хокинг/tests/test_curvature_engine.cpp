#include "omega/curvature_engine.hpp"
#include "omega/metric_provider.hpp"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

namespace {
int tests = 0;
int failures = 0;
void check(bool ok, const std::string& name) {
    ++tests;
    if (ok) std::cout << "PASS: " << name << '\n';
    else { ++failures; std::cout << "FAIL: " << name << '\n'; }
}
bool close(double a, double b) {
    return std::abs(a-b) <= 2.0e-10 + 2.0e-9*std::max(std::abs(a),std::abs(b));
}
}

int main() {
    using namespace omega_isop;
    const MetricProviderParameters p{0.4, 2.0, 3.0, 2.0, 0.7};
    const auto jet = MetricProvider::evaluate(p);
    const auto result = reconstruct_curvature(jet);

    bool inverse_ok = true;
    for (std::size_t i=0;i<4;++i)
        for (std::size_t j=0;j<4;++j) {
            double v=0.0;
            for (std::size_t k=0;k<4;++k) v += jet.g(i,k)*result.inverse_metric(k,j);
            inverse_ok = close(v, i==j ? 1.0 : 0.0) && inverse_ok;
        }
    check(inverse_ok, "inverse metric satisfies g*g_inverse = I");

    bool gamma_symmetry = true;
    for (std::size_t r=0;r<4;++r)
        for (std::size_t m=0;m<4;++m)
            for (std::size_t n=0;n<4;++n)
                gamma_symmetry = close(result.christoffel(r,m,n),
                                       result.christoffel(r,n,m)) && gamma_symmetry;
    check(gamma_symmetry, "Christoffel lower-index symmetry");

    const double D=p.x*p.x-2.0*p.q*p.x+p.q;
    const double s=std::sin(p.theta);
    const double expected_ricci[4] = {
        p.c*p.c*p.q*D/(p.Rm*p.Rm*std::pow(p.x,6)),
        -p.q/(p.x*p.x*D),
        p.q/(p.x*p.x),
        p.q*s*s/(p.x*p.x)
    };
    bool ricci_ok=true;
    for(std::size_t i=0;i<4;++i)
        for(std::size_t j=0;j<4;++j)
            ricci_ok=close(result.ricci(i,j),i==j?expected_ricci[i]:0.0)&&ricci_ok;
    check(ricci_ok, "all 16 Ricci components match the independent III-B.3 target");

    check(close(result.ricci_scalar,0.0), "Ricci scalar is zero");

    bool einstein_covariant_ok=true;
    for(std::size_t i=0;i<4;++i)
        for(std::size_t j=0;j<4;++j)
            einstein_covariant_ok=close(result.einstein(i,j),result.ricci(i,j))
                                  &&einstein_covariant_ok;
    check(einstein_covariant_ok, "Einstein covariant tensor equals Ricci for R=0");

    const double expected_mixed[4]={-p.q/(p.Rm*p.Rm*std::pow(p.x,4)),
                                    -p.q/(p.Rm*p.Rm*std::pow(p.x,4)),
                                     p.q/(p.Rm*p.Rm*std::pow(p.x,4)),
                                     p.q/(p.Rm*p.Rm*std::pow(p.x,4))};
    bool mixed_ok=true;
    for(std::size_t i=0;i<4;++i)
        for(std::size_t j=0;j<4;++j)
            mixed_ok=close(result.einstein_mixed(i,j),i==j?expected_mixed[i]:0.0)
                     &&mixed_ok;
    check(mixed_ok, "all 16 mixed Einstein components match the III-B.3 target");

    std::size_t riemann_nonzero=0;
    bool antisymmetry=true;
    for(std::size_t r=0;r<4;++r)
        for(std::size_t sig=0;sig<4;++sig)
            for(std::size_t m=0;m<4;++m)
                for(std::size_t n=0;n<4;++n) {
                    if(std::abs(result.riemann(r,sig,m,n))>1.0e-12) ++riemann_nonzero;
                    antisymmetry=close(result.riemann(r,sig,m,n),
                                       -result.riemann(r,sig,n,m))&&antisymmetry;
                }
    check(antisymmetry, "Riemann last-index antisymmetry");
    check(riemann_nonzero==24, "Riemann has 24 nonzero ordered components at the fixture");

    std::size_t bianchi_count=0;
    bool bianchi_ok=true;
    for(std::size_t r=0;r<4;++r)
        for(std::size_t sig=0;sig<4;++sig)
            for(std::size_t m=0;m<4;++m)
                for(std::size_t n=0;n<4;++n) {
                    const double v=result.riemann(r,sig,m,n)
                        +result.riemann(r,m,n,sig)
                        +result.riemann(r,n,sig,m);
                    bianchi_ok=close(v,0.0)&&bianchi_ok;
                    ++bianchi_count;
                }
    check(bianchi_ok && bianchi_count==256,
          "algebraic first Bianchi identity, 256/256 combinations");

    // Physical c and geometric Rm can differ by many orders of magnitude.
    // Scaled pivoting must not mistake this dimensional scale separation
    // for a singular metric.
    const MetricProviderParameters physical_scale{0.4, 1.0, 299792458.0, 2.0, 0.7};
    const auto physical_jet = MetricProvider::evaluate(physical_scale);
    const auto physical_result = reconstruct_curvature(physical_jet);
    bool physical_inverse_ok = true;
    for (std::size_t i=0; i<4; ++i)
        for (std::size_t j=0; j<4; ++j) {
            double value = 0.0;
            for (std::size_t k=0; k<4; ++k)
                value += physical_jet.g(i,k)*physical_result.inverse_metric(k,j);
            physical_inverse_ok = close(value, i==j ? 1.0 : 0.0)
                                  && physical_inverse_ok;
        }
    check(physical_inverse_ok,
          "scaled pivoting handles physical c/Rm magnitude separation");

    std::cout << "SUMMARY: " << (tests-failures) << "/" << tests
              << " checks passed; failures=" << failures << '\n';
    return failures==0?0:1;
}
