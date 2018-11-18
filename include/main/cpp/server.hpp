/*
 * Copyright 2018 NCSU Robotics
 */

#ifndef INCLUDE_MAIN_CPP_SERVER_HPP_
#define INCLUDE_MAIN_CPP_SERVER_HPP_
#include <string>
#include <unordered_map>
#include "opencv2/opencv.hpp"
#include "boost/optional.hpp"
#include "source.hpp"

using std::string;
using std::unordered_map;
using boost::optional;

using cv::Mat;

class Server {
 public:
  static const int PORT = 5005;

 private:
  unordered_map<string, Source> sources;
 public:
  Server(int argc, string* argv) noexcept;
  auto add_source(Source source) -> void;
  auto remove_source(string name) -> void;
  auto clear_source() -> void;
  auto get_source(string name) -> optional<Source>;
  auto swapcams() -> bool;
  auto start_cams() -> void;
  auto compressFrame(string source) -> Mat;
  auto run() -> int;
};

#endif  // INCLUDE_MAIN_CPP_SERVER_HPP_
