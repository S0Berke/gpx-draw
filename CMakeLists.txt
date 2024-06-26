project(gpx-graph)
cmake_minimum_required(VERSION 3.0)

include_directories(
    external
    external/rapidxml
)

add_subdirectory(src)
