/*
 * Copyright NCSU Robotics 2018
 */

#include "source.hpp"

using cv::VideoCapture;
using cv::String;

using std::string;

/**
 * Construct a source.
 * This exists because default constructors
 * are used by templates sometimes.
 */
Source::Source() {
}

/**
 * Construct a source.
 * @param name the name of the source
 * @param capture the video with which to capture it
 */
Source::Source(string name, VideoCapture capture) {
  this->name = name;
  this->capture = capture;
}

/**
 * Construct a source
 * @param name the name of the source, and the name of the camera
 */
Source::Source(string name) {
  this->name = name;
  this->capture = VideoCapture(name.c_str());
}

/**
 * Copy another source
 * @param other the other source
 */
Source::Source(const Source &other) {
  this->name = other.name;
  this->capture = other.capture;
}

/**
 * Set a source equal to something
 * @param source the other source
 */
Source& Source::operator=(const Source& source) {
  this->name = source.name;
  this->capture = source.capture;
  return *this;
}

/**
 * Destroy this source.
 */
Source::~Source() {
}
