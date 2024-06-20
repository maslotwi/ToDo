cmake_minimum_required(VERSION 3.5)
PROJECT(days)


set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

execute_process(COMMAND bash -c "python3-config --ldflags | tr ' ' ';'"
                OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE OPCJE)

add_link_options(${OPCJE})
add_link_options(-lpython3)

ADD_LIBRARY(days SHARED days.cpp)

TARGET_LINK_LIBRARIES(days PUBLIC)