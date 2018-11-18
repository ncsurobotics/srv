/*
 * Copyright 2018 NCSU Robotics
 */

/**
 * @file server.cpp
 * Defines the methods for the server.
 * This class defines the servers constructor.
 * @author Jacob Salzberg
 */

#include <string>
#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include "server.hpp"

using std::string;
using std::cout;
using std::endl;


using boost::asio::ip::udp;
using boost::asio::io_service;
using boost::system::error_code;
using boost::asio::buffer;

/**
 * Construct the server.
 * @param argc the amount of arguments. Should be passed down from the main function.
 * @param argv a pointer to the beginning of the argument array
 */
Server::Server(int argc, char** argv) noexcept {
}

/**
 * Add a source to the server
 * @param source the source
 */
auto Server::add_source(string source) -> void {
}

/**
 * Remove a source from the server.
 * @param source the source to remove
 * @return whether a source was removed
 */
auto Server::remove_source(string source) -> bool {
  return false;
}

/**
 * Clear the server's list of sources
 */
auto Server::clear_source() -> void {
}

/**
 * Get a source from the server
 * @param name the source to get
 */
auto Server::get_source(string name) -> string {
  return NULL;
}

/**
 * Swap the source's cameras
 */
auto Server::swapcams() -> void {
}

/**
 * Start the source's cameras
 */
auto Server::start_cams() -> void {
}

/**
 * Get and compress the frames of one of the sources' images
 * @param source the source to compress
 * @return the compressed image
 */
auto Server::compressFrame(string source) -> Mat {
  // TODO fix this, this is not an actual value
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
