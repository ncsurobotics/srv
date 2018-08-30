cmake_minimum_required(VERSION 3.1.0)

find_package(Boost
             1.40.0
             REQUIRED
             COMPONENTS system thread)

find_package(Threads REQUIRED)

add_executable(server main.cpp)
target_link_libraries(server ${Boost_LIBRARIES} Threads::Threads)
