cmake_minimum_required(VERSION 3.16)
project(omega_isop_tensor_storage LANGUAGES CXX)

add_library(omega_isop_tensor_storage INTERFACE)
target_include_directories(omega_isop_tensor_storage INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_features(omega_isop_tensor_storage INTERFACE cxx_std_17)

add_executable(test_tensor_storage tests/test_tensor_storage.cpp)
target_link_libraries(test_tensor_storage PRIVATE omega_isop_tensor_storage)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(test_tensor_storage PRIVATE
        -Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion -Werror)
endif()

enable_testing()
add_test(NAME tensor_storage_tests COMMAND test_tensor_storage)
