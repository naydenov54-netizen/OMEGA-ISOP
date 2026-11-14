#ifndef OMEGA_ISOP_TENSOR_STORAGE_HPP
#define OMEGA_ISOP_TENSOR_STORAGE_HPP

#include <array>
#include <cstddef>
#include <type_traits>

namespace omega_isop {

inline constexpr std::size_t kDimension = 4;

enum class Coordinate : std::size_t {
    T = 0,
    X = 1,
    Theta = 2,
    Phi = 3
};

constexpr std::size_t index(Coordinate coordinate) noexcept {
    return static_cast<std::size_t>(coordinate);
}

template <typename Scalar>
using Vector4 = std::array<Scalar, kDimension>;

template <typename Scalar>
class Matrix4 {
public:
    using Storage = std::array<std::array<Scalar, kDimension>, kDimension>;

    constexpr Scalar& operator()(std::size_t mu, std::size_t nu) {
        return values_.at(mu).at(nu);
    }

    constexpr const Scalar& operator()(std::size_t mu, std::size_t nu) const {
        return values_.at(mu).at(nu);
    }

    constexpr Scalar& operator()(Coordinate mu, Coordinate nu) {
        return (*this)(index(mu), index(nu));
    }

    constexpr const Scalar& operator()(Coordinate mu, Coordinate nu) const {
        return (*this)(index(mu), index(nu));
    }

    constexpr Storage& storage() noexcept { return values_; }
    constexpr const Storage& storage() const noexcept { return values_; }

private:
    Storage values_{};
};

template <typename Scalar>
class Tensor3_4 {
public:
    using Storage = std::array<Matrix4<Scalar>, kDimension>;

    // Contract: value(a, mu, nu) = partial_a(g_mu_nu).
    constexpr Scalar& operator()(std::size_t a, std::size_t mu, std::size_t nu) {
        return values_.at(a)(mu, nu);
    }

    constexpr const Scalar& operator()(std::size_t a, std::size_t mu, std::size_t nu) const {
        return values_.at(a)(mu, nu);
    }

    constexpr Scalar& operator()(Coordinate a, Coordinate mu, Coordinate nu) {
        return (*this)(index(a), index(mu), index(nu));
    }

    constexpr const Scalar& operator()(Coordinate a, Coordinate mu, Coordinate nu) const {
        return (*this)(index(a), index(mu), index(nu));
    }

    constexpr Storage& storage() noexcept { return values_; }
    constexpr const Storage& storage() const noexcept { return values_; }

private:
    Storage values_{};
};

template <typename Scalar>
class Tensor4_4 {
public:
    using Storage = std::array<Tensor3_4<Scalar>, kDimension>;

    // Contract: value(a, b, mu, nu) = partial_a(partial_b(g_mu_nu)).
    constexpr Scalar& operator()(std::size_t a, std::size_t b,
                                 std::size_t mu, std::size_t nu) {
        return values_.at(a)(b, mu, nu);
    }

    constexpr const Scalar& operator()(std::size_t a, std::size_t b,
                                       std::size_t mu, std::size_t nu) const {
        return values_.at(a)(b, mu, nu);
    }

    constexpr Scalar& operator()(Coordinate a, Coordinate b,
                                 Coordinate mu, Coordinate nu) {
        return (*this)(index(a), index(b), index(mu), index(nu));
    }

    constexpr const Scalar& operator()(Coordinate a, Coordinate b,
                                       Coordinate mu, Coordinate nu) const {
        return (*this)(index(a), index(b), index(mu), index(nu));
    }

    constexpr Storage& storage() noexcept { return values_; }
    constexpr const Storage& storage() const noexcept { return values_; }

private:
    Storage values_{};
};

template <typename Scalar>
struct MetricJet {
    static_assert(std::is_default_constructible<Scalar>::value,
                  "MetricJet scalar must be default constructible");

    Matrix4<Scalar> g{};
    Tensor3_4<Scalar> dg{};
    Tensor4_4<Scalar> ddg{};
};

using DiagnosticScalar = double;
using DiagnosticMetricJet = MetricJet<DiagnosticScalar>;

static_assert(kDimension == 4, "OMEGA-ISOP coordinate dimension is fixed at four");
static_assert(index(Coordinate::T) == 0, "T index contract changed");
static_assert(index(Coordinate::X) == 1, "x index contract changed");
static_assert(index(Coordinate::Theta) == 2, "theta index contract changed");
static_assert(index(Coordinate::Phi) == 3, "phi index contract changed");

} // namespace omega_isop

#endif // OMEGA_ISOP_TENSOR_STORAGE_HPP
