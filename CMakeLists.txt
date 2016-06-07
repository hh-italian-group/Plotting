project(hh-plotting)
cmake_minimum_required(VERSION 2.6)

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake/modules")

find_package(ROOT REQUIRED COMPONENTS Core Hist RIO Tree Physics Graf Gpad Matrix)
find_package(BoostEx REQUIRED COMPONENTS program_options filesystem regex system)
include_directories(SYSTEM ${Boost_INCLUDE_DIRS} ${ROOT_INCLUDE_DIR})
set(ALL_LIBS ${Boost_LIBRARIES} ${ROOT_LIBRARIES})

SET(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
SET(CMAKE_INSTALL_RPATH "${Boost_LIBRARY_DIRS};${ROOT_LIBRARY_DIR}")

set(CMAKE_CXX_COMPILER g++)
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -O3")

file(GLOB_RECURSE HEADER_LIST "*.h")
add_custom_target(headers SOURCES ${HEADER_LIST})

file(GLOB_RECURSE SOURCE_LIST "*.cpp")
add_custom_target(sources SOURCES ${SOURCE_LIST})

file(GLOB_RECURSE CONFIG_LIST "*.cfg" "*.xml")
add_custom_target(configs SOURCES ${CONFIG_LIST})

add_executable(hh-common-plot "bin/CommonPlot.cpp")
target_link_libraries(hh-common-plot ${ALL_LIBS})
