#ifndef OMEGA_ISOP_CURVATURE_ENGINE_HPP
#define OMEGA_ISOP_CURVATURE_ENGINE_HPP

#include "omega/tensor_storage.hpp"

#include <algorithm>
#include <array>
#include <cmath>
#include <limits>
#include <stdexcept>

namespace omega_isop {

struct CurvatureResult {
    Matrix4<double> inverse_metric{};
    Tensor3_4<double> christoffel{}; // Gamma^rho_(mu nu)
    Tensor4_4<double> riemann{};      // R^rho_(sigma mu nu)
    Matrix4<double> ricci{};          // R_(sigma nu)
    double ricci_scalar{};
    Matrix4<double> einstein{};       // G_(mu nu)
    Matrix4<double> einstein_mixed{}; // G^mu_nu
};

inline Matrix4<double> invert_metric(const Matrix4<double>& metric) {
    std::array<std::array<double, 2 * kDimension>, kDimension> a{};
    double scale = 0.0;
    for (std::size_t i = 0; i < kDimension; ++i) {
        for (std::size_t j = 0; j < kDimension; ++j) {
            const double value = metric(i, j);
            if (!std::isfinite(value))
                throw std::invalid_argument("CurvatureEngine: non-finite metric");
            a[i][j] = value;
            scale = std::max(scale, std::abs(value));
        }
        a[i][kDimension + i] = 1.0;
    }
    if (scale == 0.0)
        throw std::domain_error("CurvatureEngine: singular zero metric");

    for (std::size_t col = 0; col < kDimension; ++col) {
        std::size_t pivot = col;
        for (std::size_t row = col + 1; row < kDimension; ++row)
            if (std::abs(a[row][col]) > std::abs(a[pivot][col])) pivot = row;
        if (std::abs(a[pivot][col]) <=
            64.0 * std::numeric_limits<double>::epsilon() * scale)
            throw std::domain_error("CurvatureEngine: metric is singular or ill-conditioned");
        if (pivot != col) std::swap(a[pivot], a[col]);

        const double divisor = a[col][col];
        for (std::size_t j = 0; j < 2 * kDimension; ++j)
            a[col][j] /= divisor;

        for (std::size_t row = 0; row < kDimension; ++row) {
            if (row == col) continue;
            const double factor = a[row][col];
            for (std::size_t j = 0; j < 2 * kDimension; ++j)
                a[row][j] -= factor * a[col][j];
        }
    }

    Matrix4<double> inverse{};
    for (std::size_t i = 0; i < kDimension; ++i)
        for (std::size_t j = 0; j < kDimension; ++j) {
            inverse(i, j) = a[i][kDimension + j];
            if (!std::isfinite(inverse(i, j)))
                throw std::overflow_error("CurvatureEngine: non-finite inverse metric");
        }
    return inverse;
}

inline CurvatureResult reconstruct_curvature(const MetricJet<double>& jet) {
    CurvatureResult out{};
    out.inverse_metric = invert_metric(jet.g);

    for (std::size_t rho = 0; rho < kDimension; ++rho)
        for (std::size_t mu = 0; mu < kDimension; ++mu)
            for (std::size_t nu = 0; nu < kDimension; ++nu) {
                double value = 0.0;
                for (std::size_t sigma = 0; sigma < kDimension; ++sigma)
                    value += 0.5 * out.inverse_metric(rho, sigma) *
                        (jet.dg(mu, sigma, nu) + jet.dg(nu, sigma, mu)
                         - jet.dg(sigma, mu, nu));
                out.christoffel(rho, mu, nu) = value;
            }

    // dGamma(lambda,rho,mu,nu) is computed from dg, ddg and
    // d(g^-1) = -g^-1 * (dg) * g^-1. No curvature target is used here.
    const auto dgamma = [&](std::size_t lambda, std::size_t rho,
                            std::size_t mu, std::size_t nu) {
        double value = 0.0;
        for (std::size_t sigma = 0; sigma < kDimension; ++sigma) {
            double dinverse = 0.0;
            for (std::size_t a = 0; a < kDimension; ++a)
                for (std::size_t b = 0; b < kDimension; ++b)
                    dinverse -= out.inverse_metric(rho, a)
                        * jet.dg(lambda, a, b)
                        * out.inverse_metric(b, sigma);

            const double first =
                jet.dg(mu, sigma, nu) + jet.dg(nu, sigma, mu)
                - jet.dg(sigma, mu, nu);
            const double second =
                jet.ddg(lambda, mu, sigma, nu)
                + jet.ddg(lambda, nu, sigma, mu)
                - jet.ddg(lambda, sigma, mu, nu);
            value += 0.5 * (dinverse * first
                            + out.inverse_metric(rho, sigma) * second);
        }
        return value;
    };

    for (std::size_t rho = 0; rho < kDimension; ++rho)
        for (std::size_t sigma = 0; sigma < kDimension; ++sigma)
            for (std::size_t mu = 0; mu < kDimension; ++mu)
                for (std::size_t nu = 0; nu < kDimension; ++nu) {
                    double value = dgamma(mu, rho, nu, sigma)
                                   - dgamma(nu, rho, mu, sigma);
                    for (std::size_t lambda = 0; lambda < kDimension; ++lambda)
                        value += out.christoffel(rho, mu, lambda)
                                     * out.christoffel(lambda, nu, sigma)
                                 - out.christoffel(rho, nu, lambda)
                                     * out.christoffel(lambda, mu, sigma);
                    out.riemann(rho, sigma, mu, nu) = value;
                }

    for (std::size_t sigma = 0; sigma < kDimension; ++sigma)
        for (std::size_t nu = 0; nu < kDimension; ++nu)
            for (std::size_t rho = 0; rho < kDimension; ++rho)
                out.ricci(sigma, nu) += out.riemann(rho, sigma, rho, nu);

    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = 0; nu < kDimension; ++nu)
            out.ricci_scalar += out.inverse_metric(mu, nu) * out.ricci(mu, nu);

    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = 0; nu < kDimension; ++nu)
            out.einstein(mu, nu) =
                out.ricci(mu, nu) - 0.5 * jet.g(mu, nu) * out.ricci_scalar;

    for (std::size_t mu = 0; mu < kDimension; ++mu)
        for (std::size_t nu = 0; nu < kDimension; ++nu)
            for (std::size_t sigma = 0; sigma < kDimension; ++sigma)
                out.einstein_mixed(mu, nu) +=
                    out.inverse_metric(mu, sigma) * out.einstein(sigma, nu);

    return out;
}

} // namespace omega_isop

#endif // OMEGA_ISOP_CURVATURE_ENGINE_HPP
