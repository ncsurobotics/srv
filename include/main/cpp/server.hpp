/*
 * Copyright 2018 NCSU Robotics
 */

#ifndef INCLUDE_MAIN_CPP_SERVER_HPP_
#define INCLUDE_MAIN_CPP_SERVER_HPP_
#include <string>
#include <unordered_map>
#include <tuple>

using std::tuple;
using std::string;

class Server {
 private:
  Server(int argc, string *argv) noexcept;
  std::unordered_map<string, string> sources;
 public:
  auto addSource(tuple<string, string> source) -> void;
  auto removeSource(string source) -> bool;
  auto clearSource() -> void;
  auto getSource(string name) -> void;
  auto swapcams() -> void;
  auto startCams() -> void;
  auto compressFrame(string source) -> void;
  auto run() -> int;
};

#endif  // INCLUDE_MAIN_CPP_SERVER_HPP_
