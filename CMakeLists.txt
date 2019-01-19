cmake_minimum_required(VERSION 2.8.3)
project(rpi_object_tracking)

add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  roslib
  cv_bridge
  image_transport
)


catkin_package(

)

find_package(raspicam REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(tracking_calibration src/cpp/tracking_calibration.cpp)

target_link_libraries(tracking_calibration
  ${catkin_LIBRARIES}
  ${OpenCV_LIBRARIES}
  yaml-cpp
)
