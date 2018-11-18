/*
 * Copyright 2018 NCSU Robotics
 */

#ifndef INCLUDE_MAIN_CPP_SERVER_HPP_
#define INCLUDE_MAIN_CPP_SERVER_HPP_
#include <string>
#include <unordered_map>
#include <tuple>
#include <opencv2/core/core.hpp>

using std::tuple;
using std::string;

using cv::Mat;

class Server {
 public:
  static const int PORT = 5005;

 private:
  std::unordered_map<string, string> sources;
 public:
  Server(int argc, char** argv) noexcept;
  auto add_source(string source) -> void;
  auto remove_source(string source) -> bool;
  auto clear_source() -> void;
  auto get_source(string name) -> string;
  auto swapcams() -> void;
  auto start_cams() -> void;
  auto compressFrame(string source) -> Mat;
  auto run() -> int;
};

#endif  // INCLUDE_MAIN_CPP_SERVER_HPP_
