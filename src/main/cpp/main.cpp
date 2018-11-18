/*
 * Copyright NCSU Robotics 2018
 */

#include <ctime>
#include <iostream>
#include <string>
#include <boost/array.hpp>
#include <boost/asio.hpp>
#include "server.hpp"

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
auto main(int argc, char** argv) -> int {
  auto server = Server(argc, argv);

  try {
    return server.run();

  } catch (std::exception &e) {
    std::cerr << e.what() << std::endl;
  }
}
