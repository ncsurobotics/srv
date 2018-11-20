cmake_minimum_required(VERSION 3.1)
PROJECT(srv)

add_executable(srv
  main.cpp
  server.cpp
  "${HEADERS_DIR}/server.hpp"
  "${HEADERS_DIR}/source.hpp")
target_link_libraries(srv ${CONAN_LIBS})

add_executable(cvtest cvtest.cpp)
target_link_libraries(cvtest ${CONAN_LIBS})
