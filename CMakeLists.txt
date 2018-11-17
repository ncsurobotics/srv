cmake_minimum_required(VERSION 3.1)
PROJECT(srv)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

enable_testing()

add_subdirectory(src/main/cpp)
add_subdirectory(src/test/cpp)
