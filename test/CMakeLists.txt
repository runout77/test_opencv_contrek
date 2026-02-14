cmake_minimum_required(VERSION 3.10)

project(BenchmarkContour C CXX)

set(CMAKE_CXX_STANDARD 17)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pthread -march=native -DNDEBUG -Ofast -flto")

include_directories(/usr/local/include)
link_directories(/usr/local/lib)

add_subdirectory(contrek_core ContrekCore_build)

find_package(OpenCV REQUIRED)

if(OpenCV_FOUND)
    message(STATUS "OpenCV found: ${OpenCV_VERSION}")
else()
    message(FATAL_ERROR "OpenCV not found")
endif()

add_executable(contrek_opencv_benchmark
    test.cpp
)

target_include_directories(contrek_opencv_benchmark PRIVATE
    ${OpenCV_INCLUDE_DIRS}
)

find_library(TCMALLOC_LIB tcmalloc)
find_library(ZLIB_NG_LIB z-ng)

if(TCMALLOC_LIB)
    message(STATUS "tcmalloc found")
    target_link_libraries(contrek_opencv_benchmark PRIVATE ${TCMALLOC_LIB})
endif()

if(ZLIB_NG_LIB)
    message(STATUS "zlib-ng found: ${ZLIB_NG_LIB}")
    target_link_libraries(contrek_opencv_benchmark PRIVATE ${ZLIB_NG_LIB})
else()
    find_package(ZLIB REQUIRED)
    target_link_libraries(contrek_opencv_benchmark PRIVATE ZLIB::ZLIB)
endif()

target_link_libraries(contrek_opencv_benchmark PRIVATE
    ContrekLib
    ${OpenCV_LIBS}
    pthread
)

target_compile_options(contrek_opencv_benchmark PRIVATE
    -O3
    -march=native
    -flto
)
