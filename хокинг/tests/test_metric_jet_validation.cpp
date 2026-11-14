#include "omega/metric_jet_validation.hpp"

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
bool close(double a, double b) { return std::abs(a - b) <= 1.0e-12; }

omega_isop::MetricJet<double> make_symmetric_jet() {
    omega_isop::MetricJet<double> jet;
    for (std::size_t mu = 0; mu < 4; ++mu)
        for (std::size_t nu = 0; nu < 4; ++nu) {
            jet.g(mu, nu) = static_cast<double>(mu + nu + 1);
            for (std::size_t a = 0; a < 4; ++a) {
                jet.dg(a, mu, nu) = static_cast<double>(a + mu + nu + 1);
                for (std::size_t b = 0; b < 4; ++b)
                    jet.ddg(a, b, mu, nu) =
                        static_cast<double>(a + b + mu + nu + 1);
            }
        }
    return jet;
}
}

int main() {
    using namespace omega_isop;
    auto jet = make_symmetric_jet();
    auto symmetry = validate_metric_jet_symmetry(jet, close);
    check(symmetry.checks.size() == 4, "L1 emits four independent symmetry checks");
    check(symmetry.all_passed(), "L1 accepts a fully symmetric MetricJet");
    check(symmetry.checks[0].comparisons == 6, "L1 g symmetry checks 6 pairs");
    check(symmetry.checks[1].comparisons == 24, "L1 dg symmetry checks 24 pairs");
    check(symmetry.checks[2].comparisons == 96, "L1 ddg derivative symmetry checks 96 pairs");
    check(symmetry.checks[3].comparisons == 96, "L1 ddg metric symmetry checks 96 pairs");

    jet.g(0, 1) += 1.0;
    check(validate_metric_jet_symmetry(jet, close).has_failures(),
          "L1 detects broken g symmetry");
    jet = make_symmetric_jet();
    jet.dg(2, 0, 3) += 1.0;
    check(validate_metric_jet_symmetry(jet, close).checks[1].status == ValidationStatus::fail,
          "L1 detects broken dg metric symmetry");
    jet = make_symmetric_jet();
    jet.ddg(0, 1, 2, 3) += 1.0;
    check(validate_metric_jet_symmetry(jet, close).checks[2].status == ValidationStatus::fail,
          "L1 detects broken ddg derivative-order symmetry");
    jet = make_symmetric_jet();
    jet.ddg(0, 0, 1, 2) += 1.0;
    check(validate_metric_jet_symmetry(jet, close).checks[3].status == ValidationStatus::fail,
          "L1 detects broken ddg metric-index symmetry");

    jet = make_symmetric_jet();
    MetricDerivativeReference<double> reference;
    for (std::size_t a = 0; a < 4; ++a)
        for (std::size_t mu = 0; mu < 4; ++mu)
            for (std::size_t nu = 0; nu < 4; ++nu) {
                reference.dg(a, mu, nu) = jet.dg(a, mu, nu);
                for (std::size_t b = 0; b < 4; ++b)
                    reference.ddg(a, b, mu, nu) = jet.ddg(a, b, mu, nu);
            }
    auto derivative_ok = validate_metric_jet_derivatives(jet, reference, close);
    check(derivative_ok.all_passed(), "L2 accepts matching derivative reference");
    check(derivative_ok.checks[0].comparisons == 64, "L2 checks all 64 dg entries");
    check(derivative_ok.checks[1].comparisons == 256, "L2 checks all 256 ddg entries");
    reference.dg(1, 2, 3) += 1.0;
    check(validate_metric_jet_derivatives(jet, reference, close).checks[0].status
              == ValidationStatus::fail,
          "L2 detects disagreement in dg reference");
    reference.dg(1, 2, 3) -= 1.0;
    reference.ddg(3, 2, 1, 0) += 1.0;
    check(validate_metric_jet_derivatives(jet, reference, close).checks[1].status
              == ValidationStatus::fail,
          "L2 detects disagreement in ddg reference");

    std::cout << "SUMMARY: " << (tests - failures) << "/" << tests
              << " checks passed; failures=" << failures << '\n';
    return failures == 0 ? 0 : 1;
}
