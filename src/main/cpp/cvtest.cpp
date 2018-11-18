/*
 * Copyright NCSU Robotics 2018 
 */

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

auto main(int argc, char** argv) -> int {
  if (argc != 2) {
    std::cout << "Usage: display_image ImageToLoadAndDisplay" << std::endl;
    return -1;
  }

  cv::Mat image;
  image = imread(argv[1], cv::IMREAD_COLOR);

  if (image.empty()) {
    std::cout << "Empty image :(" << std::endl;
    return -1;
  }

  namedWindow("Display window", cv::WINDOW_AUTOSIZE);

  imshow("Display window", image);

  cv::waitKey(0);

  return 0;
}
