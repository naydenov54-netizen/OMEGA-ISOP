#ifndef OMEGA_ISOP_METRIC_JET_VALIDATION_HPP
#define OMEGA_ISOP_METRIC_JET_VALIDATION_HPP

#include "omega/tensor_storage.hpp"

#include <cstddef>
#include <string>
#include <vector>

namespace omega_isop {

enum class ValidationStatus { pass, fail, not_evaluated };

struct ValidationCheck {
    std::string id;
    ValidationStatus status;
    std::size_t comparisons;
    std::string detail;
};

struct ValidationReport {
    std::vector<ValidationCheck> checks;

    bool has_failures() const {
        for (const auto& check : checks)
            if (check.status == ValidationStatus::fail) return true;
        return false;
    }

    bool complete() const {
        for (const auto& check : checks)
            if (check.status == ValidationStatus::not_evaluated) return false;
        return true;
    }

    bool all_passed() const {
        return !checks.empty() && complete() && !has_failures();
    }
};

// L1 checks only the declared algebraic symmetries.
// The caller supplies the scalar equality policy (exact or tolerance-based).
template <typename Scalar, typename Equal>
ValidationReport validate_metric_jet_symmetry(const MetricJet<Scalar>& jet,
                                               Equal equal) {
    ValidationReport report;
    bool metric_ok = true;
    std::size_t metric_count = 0;
    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = mu + 1; nu < kDimension; ++nu) {
            ++metric_count;
            metric_ok = equal(jet.g(mu, nu), jet.g(nu, mu)) && metric_ok;
        }
    report.checks.push_back({"L1-G-SYMMETRY",
        metric_ok ? ValidationStatus::pass : ValidationStatus::fail,
        metric_count, "g(mu,nu) = g(nu,mu)"});

    bool first_ok = true;
    std::size_t first_count = 0;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t mu = 0; mu < kDimension; ++mu)
            for (std::size_t nu = mu + 1; nu < kDimension; ++nu) {
                ++first_count;
                first_ok = equal(jet.dg(a, mu, nu), jet.dg(a, nu, mu)) && first_ok;
            }
    report.checks.push_back({"L1-DG-METRIC-SYMMETRY",
        first_ok ? ValidationStatus::pass : ValidationStatus::fail,
        first_count, "dg(a,mu,nu) = dg(a,nu,mu)"});

    bool second_derivative_ok = true;
    std::size_t second_derivative_count = 0;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t b = a + 1; b < kDimension; ++b)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = 0; nu < kDimension; ++nu) {
                    ++second_derivative_count;
                    second_derivative_ok =
                        equal(jet.ddg(a, b, mu, nu), jet.ddg(b, a, mu, nu))
                        && second_derivative_ok;
                }
    report.checks.push_back({"L1-DDG-DERIVATIVE-SYMMETRY",
        second_derivative_ok ? ValidationStatus::pass : ValidationStatus::fail,
        second_derivative_count, "ddg(a,b,mu,nu) = ddg(b,a,mu,nu)"});

    bool second_metric_ok = true;
    std::size_t second_metric_count = 0;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t b = 0; b < kDimension; ++b)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = mu + 1; nu < kDimension; ++nu) {
                    ++second_metric_count;
                    second_metric_ok =
                        equal(jet.ddg(a, b, mu, nu), jet.ddg(a, b, nu, mu))
                        && second_metric_ok;
                }
    report.checks.push_back({"L1-DDG-METRIC-SYMMETRY",
        second_metric_ok ? ValidationStatus::pass : ValidationStatus::fail,
        second_metric_count, "ddg(a,b,mu,nu) = ddg(a,b,nu,mu)"});
    return report;
}

// L2 compares stored derivatives with a separately constructed reference.
// Agreement does not certify the reference's derivation or provenance.
template <typename Scalar>
struct MetricDerivativeReference {
    Tensor3_4<Scalar> dg{};
    Tensor4_4<Scalar> ddg{};
};

template <typename Scalar, typename Equal>
ValidationReport validate_metric_jet_derivatives(
    const MetricJet<Scalar>& jet,
    const MetricDerivativeReference<Scalar>& reference,
    Equal equal) {
    ValidationReport report;
    bool first_ok = true;
    std::size_t first_count = 0;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t mu = 0; mu < kDimension; ++mu)
            for (std::size_t nu = 0; nu < kDimension; ++nu) {
                ++first_count;
                first_ok = equal(jet.dg(a, mu, nu), reference.dg(a, mu, nu))
                           && first_ok;
            }
    report.checks.push_back({"L2-FIRST-DERIVATIVE-REFERENCE",
        first_ok ? ValidationStatus::pass : ValidationStatus::fail,
        first_count, "dg agrees with supplied independent derivative reference"});

    bool second_ok = true;
    std::size_t second_count = 0;
    for (std::size_t a = 0; a < kDimension; ++a)
        for (std::size_t b = 0; b < kDimension; ++b)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = 0; nu < kDimension; ++nu) {
                    ++second_count;
                    second_ok = equal(jet.ddg(a, b, mu, nu),
                                      reference.ddg(a, b, mu, nu)) && second_ok;
                }
    report.checks.push_back({"L2-SECOND-DERIVATIVE-REFERENCE",
        second_ok ? ValidationStatus::pass : ValidationStatus::fail,
        second_count, "ddg agrees with supplied independent derivative reference"});
    return report;
}

} // namespace omega_isop

#endif // OMEGA_ISOP_METRIC_JET_VALIDATION_HPP
