cmake_minimum_required(VERSION 3.16)
project(omega_isop_tensor_validation LANGUAGES CXX)

add_library(omega_isop_tensor_storage INTERFACE)
target_include_directories(omega_isop_tensor_storage INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_features(omega_isop_tensor_storage INTERFACE cxx_std_17)

add_executable(test_tensor_storage tests/test_tensor_storage.cpp)
target_link_libraries(test_tensor_storage PRIVATE omega_isop_tensor_storage)

add_executable(test_metric_jet_validation tests/test_metric_jet_validation.cpp)
target_link_libraries(test_metric_jet_validation PRIVATE omega_isop_tensor_storage)

add_executable(test_metric_provider tests/test_metric_provider.cpp)
target_link_libraries(test_metric_provider PRIVATE omega_isop_tensor_storage)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    foreach(target test_tensor_storage test_metric_jet_validation test_metric_provider)
        target_compile_options(${target} PRIVATE
            -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror)
    endforeach()
endif()

enable_testing()
add_test(NAME tensor_storage_tests COMMAND test_tensor_storage)
add_test(NAME metric_jet_validation_tests COMMAND test_metric_jet_validation)
add_test(NAME metric_provider_tests COMMAND test_metric_provider)
