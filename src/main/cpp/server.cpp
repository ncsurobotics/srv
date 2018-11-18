/*
 * Copyright 2018 NCSU Robotics
 */

/**
 * @file server.cpp
 * Defines the methods for the server.
 * This class defines the servers constructor.
 * @author Jacob Salzberg
 */

// #include <optional>
#include <iostream>
#include <string>
#include <utility>
#include "boost/array.hpp"
#include "boost/asio.hpp"
#include "boost/optional.hpp"
#include "server.hpp"
#include "source.hpp"

using std::string;
using std::cout;
using std::endl;
// using std::optional;

using std::unordered_map;
using std::pair;

using boost::asio::ip::udp;
using boost::asio::io_service;
using boost::system::error_code;
using boost::asio::buffer;

/**
 * Construct the server.
 * @param argc the amount of arguments. Should be passed down from the main function.
 * @param argv a pointer to the beginning of the argument array
 */
Server::Server(int argc, string* argv) noexcept {
  sources = { };
}

/**
 * Add a source to the server
 * @param source the source
 */
auto Server::add_source(Source source) -> void {
  sources.insert({source.name, source});
}

/**
 * Remove a source from the server.
 * @param source the source to remove
 * @return whether a source was removed
 */
auto Server::remove_source(string name) -> void {
  sources.erase(name);
}

/**
 * Clear the server's list of sources
 */
auto Server::clear_source() -> void {
  sources.clear();
}

/**
 * Get a source from the server
 * @param name the source to get
 */
auto Server::get_source(string name) -> optional<Source> {
  auto found = sources.find(name);
  if (found == sources.end()) {
    return { };
  }
  return found->second;
}

/**
 * Swap the source's cameras.
 * @return whether the source's cameras were really swapped
 */
auto Server::swapcams() -> bool {
  if (!this->get_source("down").has_value()) {
    return false;
  }
  if (!this->get_source("forward").has_value()) {
    return false;
  }
  auto oldDown = this->get_source("down").value();
  sources["down"] = sources["foward"];
  sources["down"].name = "down";
  sources["forward"] = oldDown;
  sources["forward"].name = "forward";
  return true;
}

/**
 * Start the source's cameras
 */
auto Server::start_cams() -> void {

  auto sourceToAdd = Source("down");
  add_source(sourceToAdd);

  // Make this configurable, and and foward source as well.
  cout << "Started cams" << endl;
}

/**
 * Get and compress the frames of one of the sources' images
 * @param source the source to compress
 * @return the compressed image
 */
auto Server::compressFrame(string source) -> Mat {
  // TODO(jssalzbe): fix this, this is not an actual value
  for (auto keyval : sources) {
    auto source = keyval.second;
    Mat img;
    source.capture >> img;

  }
  return Mat();
}

/**
 * Run the program
 * @return whether this program exited successfully or not
 */
auto Server::run() -> int {
  cout << "Starting srv on port: " << Server::PORT << endl;
  // The io_service serves as the io context for the udp socket.
  io_service ioService;
  auto endpoint = udp::endpoint(udp::v4(), Server::PORT);
  udp::socket socket(ioService, endpoint);

  while (true) {
    boost::array<char, 100> recvBuf;
    udp::endpoint remote_endpoint;
    error_code error;
    socket.receive_from(buffer(recvBuf), remote_endpoint, 0, error);
    cout << recvBuf.data() << endl;
    string message = "hey";
    error_code ignored_error;
    auto msg = buffer(message);
    socket.send_to(msg, remote_endpoint, 0, ignored_error);
  }

  return 0;
}
