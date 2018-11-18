cmake_minimum_required(VERSION 3.1)
PROJECT(srv)

add_executable(srv main.cpp)
target_link_libraries(srv ${CONAN_LIBS})

add_executable(cvtest cvtest.cpp)
target_link_libraries(cvtest ${CONAN_LIBS})
