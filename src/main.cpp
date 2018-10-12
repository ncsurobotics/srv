#include <iostream>
#include <boost/array.hpp>
#include <boost/asio.hpp>

using boost::asio::ip::udp;

int main() {
  try {
    boost::asio::io_service io_service;
    udp::socket socket(io_service, udp::endpoint(udp::v4(), 13));

    while (true) {
      boost::array<char, 1> recv_buf;
      udp::endpoint remote_endpoint;
      boost::system::error_code error;
      socket.receive_from(boost::asio::buffer(recv_buf),
                          remote_endpoint, 0, error);
      if (error && error != boost::asio::error::message_size) {
        throw boost::system::system_error(error);
      }

      std::string message = "daytime";
      
    }

  } catch (std::exception &e) {
    std::cerr << e.what() << std::endl;
  }
  std::cout << "Hi" << std::endl;
  return 0;
}