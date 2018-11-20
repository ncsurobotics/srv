/*
 * Copyright NCSU Robotics 2018
 */

#ifndef INCLUDE_MAIN_CPP_SOURCE_HPP_
#define INCLUDE_MAIN_CPP_SOURCE_HPP_
#include <iterator>
#include <string>
#include "opencv2/opencv.hpp"

using cv::VideoCapture;

using std::string;

class Source {
 public:
  // Constructor
  Source(string name, VideoCapture capture);
  // Also constructor
  explicit Source(string name);
  // Copy Constructor
  Source(const Source &other);
  // Copy Assignment Constructor
  Source& operator=(const Source& source);
  // Destructor
  ~Source();
  string name;
  VideoCapture capture;
};


// typedef istream_iterator<Mat> Source;

#endif  // INCLUDE_MAIN_CPP_SOURCE_HPP_
