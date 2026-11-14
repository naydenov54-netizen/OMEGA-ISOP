#include "omega/tensor_storage.hpp"

#include <cmath>
#include <cstddef>
#include <exception>
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>

namespace {

int failures = 0;
int tests = 0;

void check(bool condition, const std::string& name) {
    ++tests;
    if (condition) {
        std::cout << "PASS: " << name << '\n';
    } else {
        ++failures;
        std::cout << "FAIL: " << name << '\n';
    }
}

bool close(double a, double b) {
    return std::abs(a - b) <= 1.0e-12;
}

void test_coordinate_contract() {
    using omega_isop::Coordinate;
    check(omega_isop::kDimension == 4, "N equals 4");
    check(omega_isop::index(Coordinate::T) == 0, "coordinate T maps to index 0");
    check(omega_isop::index(Coordinate::X) == 1, "coordinate x maps to index 1");
    check(omega_isop::index(Coordinate::Theta) == 2, "coordinate theta maps to index 2");
    check(omega_isop::index(Coordinate::Phi) == 3, "coordinate phi maps to index 3");
}

void test_metric_matrix_storage() {
    omega_isop::Matrix4<double> matrix;
    std::size_t count = 0;
    for (std::size_t mu = 0; mu < 4; ++mu) {
        for (std::size_t nu = 0; nu < 4; ++nu) {
            const double value = static_cast<double>(100 * mu + nu) + 0.25;
            matrix(mu, nu) = value;
            ++count;
        }
    }
    bool all_ok = (count == 16);
    for (std::size_t mu = 0; mu < 4; ++mu) {
        for (std::size_t nu = 0; nu < 4; ++nu) {
            all_ok = all_ok && close(matrix(mu, nu),
                static_cast<double>(100 * mu + nu) + 0.25);
        }
    }
    check(all_ok, "Matrix4 stores and retrieves all 16 ordered entries");

    matrix(omega_isop::Coordinate::T, omega_isop::Coordinate::Phi) = 42.5;
    check(close(matrix(0, 3), 42.5), "semantic Matrix4 access matches numeric indices");
}

void test_rank3_storage() {
    omega_isop::Tensor3_4<double> tensor;
    std::size_t count = 0;
    for (std::size_t a = 0; a < 4; ++a) {
        for (std::size_t mu = 0; mu < 4; ++mu) {
            for (std::size_t nu = 0; nu < 4; ++nu) {
                tensor(a, mu, nu) = static_cast<double>(100 * a + 10 * mu + nu);
                ++count;
            }
        }
    }
    bool all_ok = (count == 64);
    for (std::size_t a = 0; a < 4; ++a) {
        for (std::size_t mu = 0; mu < 4; ++mu) {
            for (std::size_t nu = 0; nu < 4; ++nu) {
                all_ok = all_ok && close(tensor(a, mu, nu),
                    static_cast<double>(100 * a + 10 * mu + nu));
            }
        }
    }
    check(all_ok, "Tensor3_4 stores and retrieves all 64 [a][mu][nu] entries");
    tensor(omega_isop::Coordinate::Phi, omega_isop::Coordinate::X,
           omega_isop::Coordinate::Theta) = 321.0;
    check(close(tensor(3, 1, 2), 321.0), "semantic Tensor3_4 access preserves index order");
}

void test_rank4_storage() {
    omega_isop::Tensor4_4<double> tensor;
    std::size_t count = 0;
    for (std::size_t a = 0; a < 4; ++a) {
        for (std::size_t b = 0; b < 4; ++b) {
            for (std::size_t mu = 0; mu < 4; ++mu) {
                for (std::size_t nu = 0; nu < 4; ++nu) {
                    tensor(a, b, mu, nu) = static_cast<double>(1000 * a + 100 * b + 10 * mu + nu);
                    ++count;
                }
            }
        }
    }
    bool all_ok = (count == 256);
    for (std::size_t a = 0; a < 4; ++a) {
        for (std::size_t b = 0; b < 4; ++b) {
            for (std::size_t mu = 0; mu < 4; ++mu) {
                for (std::size_t nu = 0; nu < 4; ++nu) {
                    all_ok = all_ok && close(tensor(a, b, mu, nu),
                        static_cast<double>(1000 * a + 100 * b + 10 * mu + nu));
                }
            }
        }
    }
    check(all_ok, "Tensor4_4 stores and retrieves all 256 [a][b][mu][nu] entries");
    tensor(omega_isop::Coordinate::Phi, omega_isop::Coordinate::Theta,
           omega_isop::Coordinate::X, omega_isop::Coordinate::T) = 3210.0;
    check(close(tensor(3, 2, 1, 0), 3210.0), "semantic Tensor4_4 access preserves index order");
}

void test_metric_jet_and_scalar_genericity() {
    static_assert(std::is_same<omega_isop::DiagnosticScalar, double>::value,
                  "diagnostic backend scalar must be double");
    omega_isop::MetricJet<double> jet;
    jet.g(1, 2) = 12.0;
    jet.dg(3, 1, 2) = 312.0;
    jet.ddg(2, 3, 1, 2) = 2312.0;
    check(close(jet.g(1, 2), 12.0), "MetricJet exposes g[mu][nu]");
    check(close(jet.dg(3, 1, 2), 312.0), "MetricJet exposes dg[a][mu][nu]");
    check(close(jet.ddg(2, 3, 1, 2), 2312.0), "MetricJet exposes ddg[a][b][mu][nu]");

    omega_isop::MetricJet<long double> long_double_jet;
    long_double_jet.g(0, 0) = 1.25L;
    check(long_double_jet.g(0, 0) == 1.25L,
          "MetricJet is scalar-generic and has no double-only storage dependency");
}

void test_bounds_and_copy_semantics() {
    omega_isop::Matrix4<double> matrix;
    bool throws = false;
    try {
        (void)matrix(4, 0);
    } catch (const std::out_of_range&) {
        throws = true;
    }
    check(throws, "Matrix4 rejects out-of-range indices with std::out_of_range");

    omega_isop::MetricJet<double> original;
    original.g(0, 0) = 7.0;
    auto copied = original;
    copied.g(0, 0) = 9.0;
    check(close(original.g(0, 0), 7.0) && close(copied.g(0, 0), 9.0),
          "MetricJet copy owns independent fixed-size storage");
}

} // namespace

int main() {
    std::cout << "OMEGA-ISOP PHASE III-B.4.5.2 — Tensor Storage Tests\n";
    test_coordinate_contract();
    test_metric_matrix_storage();
    test_rank3_storage();
    test_rank4_storage();
    test_metric_jet_and_scalar_genericity();
    test_bounds_and_copy_semantics();
    std::cout << "SUMMARY: " << (tests - failures) << "/" << tests
              << " checks passed; failures=" << failures << '\n';
    return failures == 0 ? 0 : 1;
}
