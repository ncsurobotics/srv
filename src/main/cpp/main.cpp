/*
 * Copyright NCSU Robotics 2018
 */

#include <ctime>
#include <iostream>
#include <string>
#include <boost/array.hpp>
#include <boost/asio.hpp>

/**
 * @file main.cpp
 * @brief File at which the program starts.
 * This file should contain nothing more than a short
 * main method for handling the initialization of the server.
 * @author Jacob Salzberg
 */

/**
 * @mainpage SRV -- The Seawolf Router for video
 * By running ./srv, one will start the main(int, char**) function.
 */

using boost::asio::ip::udp;


/**
 * The port to which this program sends data
 */
const int PORT = 5005;

/**
 * The main function of the program.
 * @return Always returns zero
 */
auto main(int, char**) -> int {
  std::cout << "Starting srv" << std::endl;
  try {
    // The io_service serves as the io context for the udp socket.
    boost::asio::io_service io_service;
    auto endpoint = udp::endpoint(udp::v4(), PORT);
    udp::socket socket(io_service, endpoint);

    while (true) {
      boost::array<char, 100> recv_buf;
      udp::endpoint remote_endpoint;
      boost::system::error_code error;
      socket.receive_from(boost::asio::buffer(recv_buf),
                          remote_endpoint,
                          0,
                          error);
      std::cout << recv_buf.data() << std::endl;
      std::string message = "hey";
      boost::system::error_code ignored_error;
      auto bmessage = boost::asio::buffer(message);
      socket.send_to(bmessage, remote_endpoint, 0, ignored_error);
    }
  } catch (std::exception &e) {
      std::cerr << e.what() << std::endl;
    }
    const auto x = 0;
    return x;
}
