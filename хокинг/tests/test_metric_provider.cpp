#include "omega/metric_provider.hpp"

#include <cmath>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {
int tests = 0;
int failures = 0;

void check(bool ok, const std::string& name) {
    ++tests;
    if (ok) std::cout << "PASS: " << name << '\n';
    else {
        ++failures;
        std::cout << "FAIL: " << name << '\n';
    }
}

bool close(double a, double b) {
    const double scale = (std::abs(a) > std::abs(b)) ? std::abs(a) : std::abs(b);
    return std::abs(a - b) <= 1.0e-12 + 1.0e-11 * scale;
}

double expected_g(const omega_isop::MetricProviderParameters& p,
                  std::size_t mu, std::size_t nu) {
    if (mu != nu) return 0.0;
    const double x2 = p.x * p.x;
    const double D = x2 - 2.0 * p.q * p.x + p.q;
    const double B = D / x2;
    const double Rm2 = p.Rm * p.Rm;
    if (mu == 0) return -B * p.c * p.c;
    if (mu == 1) return Rm2 / B;
    if (mu == 2) return Rm2 * x2;
    return Rm2 * x2 * std::sin(p.theta) * std::sin(p.theta);
}

double expected_dg(const omega_isop::MetricProviderParameters& p,
                   std::size_t a, std::size_t mu, std::size_t nu) {
    if (mu != nu) return 0.0;
    const double x = p.x;
    const double x2 = x * x;
    const double x3 = x2 * x;
    const double D = x2 - 2.0 * p.q * x + p.q;
    const double B = D / x2;
    const double Bx = 2.0 * p.q * (x - 1.0) / x3;
    const double Rm2 = p.Rm * p.Rm;
    const double s = std::sin(p.theta);
    const double co = std::cos(p.theta);

    if (a == 1 && mu == 0) return -p.c * p.c * Bx;
    if (a == 1 && mu == 1) return -Rm2 * Bx / (B * B);
    if (a == 1 && mu == 2) return 2.0 * Rm2 * x;
    if (a == 1 && mu == 3) return 2.0 * Rm2 * x * s * s;
    if (a == 2 && mu == 3) return 2.0 * Rm2 * x2 * s * co;
    return 0.0;
}

double expected_ddg(const omega_isop::MetricProviderParameters& p,
                    std::size_t a, std::size_t b,
                    std::size_t mu, std::size_t nu) {
    if (mu != nu) return 0.0;
    const double x = p.x;
    const double x2 = x * x;
    const double x3 = x2 * x;
    const double x4 = x2 * x2;
    const double D = x2 - 2.0 * p.q * x + p.q;
    const double B = D / x2;
    const double Bx = 2.0 * p.q * (x - 1.0) / x3;
    const double Bxx = -4.0 * p.q / x3 + 6.0 * p.q / x4;
    const double Rm2 = p.Rm * p.Rm;
    const double s = std::sin(p.theta);
    const double co = std::cos(p.theta);
    const bool xx = (a == 1 && b == 1);
    const bool theta_theta = (a == 2 && b == 2);
    const bool mixed = ((a == 1 && b == 2) || (a == 2 && b == 1));

    if (xx && mu == 0) return -p.c * p.c * Bxx;
    if (xx && mu == 1)
        return Rm2 * (2.0 * Bx * Bx / (B * B * B) - Bxx / (B * B));
    if (xx && mu == 2) return 2.0 * Rm2;
    if (xx && mu == 3) return 2.0 * Rm2 * s * s;
    if (theta_theta && mu == 3)
        return 2.0 * Rm2 * x2 * (co * co - s * s);
    if (mixed && mu == 3) return 4.0 * Rm2 * x * s * co;
    return 0.0;
}

bool throws_domain(const omega_isop::MetricProviderParameters& p) {
    try {
        (void)omega_isop::MetricProvider::evaluate(p);
    } catch (const std::domain_error&) {
        return true;
    } catch (const std::invalid_argument&) {
        return true;
    }
    return false;
}
}

int main() {
    using namespace omega_isop;
    const MetricProviderParameters p{0.4, 2.0, 3.0, 2.0, 0.7};
    const auto jet = MetricProvider::evaluate(p);

    bool metric_ok = true;
    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = 0; nu < kDimension; ++nu)
            metric_ok = close(jet.g(mu, nu), expected_g(p, mu, nu)) && metric_ok;
    check(metric_ok, "all 16 metric components match the analytic component formulas");

    bool first_ok = true;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t mu = 0; mu < kDimension; ++mu)
            for (std::size_t nu = 0; nu < kDimension; ++nu)
                first_ok = close(jet.dg(a, mu, nu),
                                 expected_dg(p, a, mu, nu)) && first_ok;
    check(first_ok, "all 64 first-derivative entries match the analytic formulas");

    bool second_ok = true;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t b = 0; b < kDimension; ++b)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = 0; nu < kDimension; ++nu)
                    second_ok = close(jet.ddg(a, b, mu, nu),
                        expected_ddg(p, a, b, mu, nu)) && second_ok;
    check(second_ok, "all 256 second-derivative entries match the analytic formulas");

    bool symmetry_ok = true;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t b = 0; b < kDimension; ++b)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = 0; nu < kDimension; ++nu) {
                    symmetry_ok = close(jet.ddg(a, b, mu, nu),
                                        jet.ddg(b, a, mu, nu)) && symmetry_ok;
                    symmetry_ok = close(jet.ddg(a, b, mu, nu),
                                        jet.ddg(a, b, nu, mu)) && symmetry_ok;
                }
    check(symmetry_ok, "second-derivative index symmetries hold");

    bool zero_coordinate_derivatives = true;
    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = 0; nu < kDimension; ++nu) {
            zero_coordinate_derivatives =
                close(jet.dg(0, mu, nu), 0.0) &&
                close(jet.dg(3, mu, nu), 0.0) &&
                zero_coordinate_derivatives;
            for (std::size_t b = 0; b < kDimension; ++b) {
                zero_coordinate_derivatives =
                    close(jet.ddg(0, b, mu, nu), 0.0) &&
                    close(jet.ddg(3, b, mu, nu), 0.0) &&
                    close(jet.ddg(b, 0, mu, nu), 0.0) &&
                    close(jet.ddg(b, 3, mu, nu), 0.0) &&
                    zero_coordinate_derivatives;
            }
        }
    check(zero_coordinate_derivatives, "T and phi derivative directions vanish");

    const auto lower_boundary = MetricProvider::evaluate(
        MetricProviderParameters{0.1, 1.5, 2.0, 1.0, 1.1});
    const auto upper_boundary = MetricProvider::evaluate(
        MetricProviderParameters{0.9, 1.5, 2.0, 1.0, 1.1});
    check(std::isfinite(lower_boundary.g(0, 0)) &&
          std::isfinite(upper_boundary.g(0, 0)),
          "q endpoints and x=1 are accepted in the declared domain");

    check(throws_domain(MetricProviderParameters{0.099, 2.0, 3.0, 2.0, 0.7}),
          "q below the declared interval is rejected");
    check(throws_domain(MetricProviderParameters{0.4, 2.0, 3.0, 0.99, 0.7}),
          "x below one is rejected");
    check(throws_domain(MetricProviderParameters{0.4, 2.0, 3.0, 2.0, 0.0}),
          "theta coordinate pole is rejected");
    check(throws_domain(MetricProviderParameters{0.4, 0.0, 3.0, 2.0, 0.7}),
          "non-positive Rm is rejected");

    std::cout << "SUMMARY: " << (tests - failures) << "/" << tests
              << " checks passed; failures=" << failures << '\n';
    return failures == 0 ? 0 : 1;
}
