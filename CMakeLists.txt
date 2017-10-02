cmake_minimum_required(VERSION 2.8.3)
project(path_maker)

find_package(catkin REQUIRED)

catkin_package()

catkin_install_python(PROGRAMS
    path_maker.py
    DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
