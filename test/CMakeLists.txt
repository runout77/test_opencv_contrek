cmake_minimum_required(VERSION 3.10)
project(BenchmarkContour C CXX)

set(CMAKE_CXX_STANDARD 17)

# Flag globali (si applicano AUTOMATICAMENTE a tutti i target)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pthread -march=native -DNDEBUG -Ofast -flto -O3")

include_directories(/usr/local/include)
link_directories(/usr/local/lib)

add_subdirectory(contrek_core ContrekCore_build)

find_package(OpenCV REQUIRED)
if(OpenCV_FOUND)
    message(STATUS "OpenCV found: ${OpenCV_VERSION}")
else()
    message(FATAL_ERROR "OpenCV not found")
endif()

# --- GESTIONE DIPENDENZE COMUNI ---
# Creiamo una lista di librerie a cui collegare entrambi gli eseguibili
set(COMMON_LIBS ContrekLib ${OpenCV_LIBS} pthread)

find_library(TCMALLOC_LIB tcmalloc)
if(TCMALLOC_LIB)
    message(STATUS "tcmalloc found")
    list(APPEND COMMON_LIBS ${TCMALLOC_LIB})
endif()

find_library(ZLIB_NG_LIB z-ng)
if(ZLIB_NG_LIB)
    message(STATUS "zlib-ng found: ${ZLIB_NG_LIB}")
    list(APPEND COMMON_LIBS ${ZLIB_NG_LIB})
else()
    find_package(ZLIB REQUIRED)
    list(APPEND COMMON_LIBS ZLIB::ZLIB)
endif()

# =================================================================
# DEFINIZIONE DEI TARGET (Ora bastano pochissime righe!)
# =================================================================

# 1. Target Benchmark Originale
add_executable(contrek_opencv_benchmark test.cpp)
target_include_directories(contrek_opencv_benchmark PRIVATE ${OpenCV_INCLUDE_DIRS})
target_link_libraries(contrek_opencv_benchmark PRIVATE ${COMMON_LIBS})

# 2. Target Streaming
add_executable(streaming_benchmark streaming.cpp)
target_include_directories(streaming_benchmark PRIVATE 
    ${OpenCV_INCLUDE_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/contrek_core
)
target_link_libraries(streaming_benchmark PRIVATE ${COMMON_LIBS})