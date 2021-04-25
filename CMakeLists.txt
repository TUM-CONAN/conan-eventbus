
PROJECT(conaneventbus)
cmake_minimum_required(VERSION 3.18)
include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()
include_directories(${CMAKE_SOURCE_DIR}/sources)
add_subdirectory("${CMAKE_SOURCE_DIR}/sources")