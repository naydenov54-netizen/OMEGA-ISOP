#ifndef OMEGA_ISOP_METRIC_PROVIDER_HPP
#define OMEGA_ISOP_METRIC_PROVIDER_HPP

#include "omega/tensor_storage.hpp"

#include <cmath>
#include <stdexcept>

namespace omega_isop {

// Diagnostic double-precision provider for the locked diagonal metric.
// This is an analytic implementation, not an interval certificate.
struct MetricProviderParameters {
    double q{};
    double Rm{};
    double c{};
    double x{};
    double theta{};
};

class MetricProvider final {
public:
    static DiagnosticMetricJet evaluate(const MetricProviderParameters& p) {
        validate_domain(p);

        const double x2 = p.x * p.x;
        const double x3 = x2 * p.x;
        const double x4 = x2 * x2;
        const double sin_theta = std::sin(p.theta);
        const double cos_theta = std::cos(p.theta);
        const double sin2 = sin_theta * sin_theta;
        const double Rm2 = p.Rm * p.Rm;
        const double c2 = p.c * p.c;

        if (!std::isfinite(Rm2) || !std::isfinite(c2) ||
            !std::isfinite(sin2) || Rm2 <= 0.0 || c2 <= 0.0 || sin2 <= 0.0) {
            throw std::overflow_error(
                "MetricProvider: scale square is non-finite or underflowed to zero");
        }

        const double D = x2 - 2.0 * p.q * p.x + p.q;
        const double B = D / x2;
        const double B_x = 2.0 * p.q * (p.x - 1.0) / x3;
        const double B_xx = -4.0 * p.q / x3 + 6.0 * p.q / x4;

        if (!std::isfinite(B) || !std::isfinite(B_x) ||
            !std::isfinite(B_xx) || B <= 0.0) {
            throw std::overflow_error("MetricProvider: invalid or non-finite B(x)");
        }

        DiagnosticMetricJet jet{};

        // Metric components.
        jet.g(Coordinate::T, Coordinate::T) = -B * c2;
        jet.g(Coordinate::X, Coordinate::X) = Rm2 / B;
        jet.g(Coordinate::Theta, Coordinate::Theta) = Rm2 * x2;
        jet.g(Coordinate::Phi, Coordinate::Phi) = Rm2 * x2 * sin2;

        // First derivatives: dg(a,mu,nu) = partial_a(g_mu_nu).
        jet.dg(Coordinate::X, Coordinate::T, Coordinate::T) =
            -c2 * B_x;

        jet.dg(Coordinate::X, Coordinate::X, Coordinate::X) =
            -Rm2 * B_x / (B * B);

        jet.dg(Coordinate::X, Coordinate::Theta, Coordinate::Theta) =
            2.0 * Rm2 * p.x;

        jet.dg(Coordinate::X, Coordinate::Phi, Coordinate::Phi) =
            2.0 * Rm2 * p.x * sin2;

        jet.dg(Coordinate::Theta, Coordinate::Phi, Coordinate::Phi) =
            2.0 * Rm2 * x2 * sin_theta * cos_theta;

        // Second derivatives: ddg(a,b,mu,nu) = partial_a(partial_b(g_mu_nu)).
        jet.ddg(Coordinate::X, Coordinate::X,
                Coordinate::T, Coordinate::T) = -c2 * B_xx;

        jet.ddg(Coordinate::X, Coordinate::X,
                Coordinate::X, Coordinate::X) =
            Rm2 * (2.0 * B_x * B_x / (B * B * B) -
                  B_xx / (B * B));

        jet.ddg(Coordinate::X, Coordinate::X,
                Coordinate::Theta, Coordinate::Theta) = 2.0 * Rm2;

        jet.ddg(Coordinate::X, Coordinate::X,
                Coordinate::Phi, Coordinate::Phi) =
            2.0 * Rm2 * sin2;

        jet.ddg(Coordinate::Theta, Coordinate::Theta,
                Coordinate::Phi, Coordinate::Phi) =
            2.0 * Rm2 * x2 * (cos_theta * cos_theta - sin2);

        const double mixed_x_theta =
            4.0 * Rm2 * p.x * sin_theta * cos_theta;
        jet.ddg(Coordinate::X, Coordinate::Theta,
                Coordinate::Phi, Coordinate::Phi) = mixed_x_theta;
        jet.ddg(Coordinate::Theta, Coordinate::X,
                Coordinate::Phi, Coordinate::Phi) = mixed_x_theta;

        require_finite(jet);
        return jet;
    }

private:
    static void validate_domain(const MetricProviderParameters& p) {
        if (!std::isfinite(p.q) || !std::isfinite(p.Rm) ||
            !std::isfinite(p.c) || !std::isfinite(p.x) ||
            !std::isfinite(p.theta)) {
            throw std::invalid_argument(
                "MetricProvider: all parameters must be finite");
        }
        if (p.q < 0.1 || p.q > 0.9) {
            throw std::domain_error("MetricProvider: q must be in [0.1, 0.9]");
        }
        if (p.x < 1.0) {
            throw std::domain_error("MetricProvider: x must be >= 1");
        }
        if (p.Rm <= 0.0 || p.c <= 0.0) {
            throw std::domain_error("MetricProvider: Rm and c must be positive");
        }
        if (p.theta <= 0.0 || p.theta >= 3.14159265358979323846) {
            throw std::domain_error("MetricProvider: theta must be in (0, pi)");
        }
    }

    static void require_finite(const DiagnosticMetricJet& jet) {
        for (std::size_t mu = 0; mu < kDimension; ++mu) {
            for (std::size_t nu = 0; nu < kDimension; ++nu) {
                if (!std::isfinite(jet.g(mu, nu))) {
                    throw std::overflow_error("MetricProvider: non-finite metric component");
                }
                for (std::size_t a = 0; a < kDimension; ++a) {
                    if (!std::isfinite(jet.dg(a, mu, nu))) {
                        throw std::overflow_error("MetricProvider: non-finite first derivative");
                    }
                    for (std::size_t b = 0; b < kDimension; ++b) {
                        if (!std::isfinite(jet.ddg(a, b, mu, nu))) {
                            throw std::overflow_error("MetricProvider: non-finite second derivative");
                        }
                    }
                }
            }
        }
    }
};

} // namespace omega_isop

#endif // OMEGA_ISOP_METRIC_PROVIDER_HPP
