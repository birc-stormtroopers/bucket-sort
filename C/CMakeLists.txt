cmake_minimum_required(VERSION 3.21)
project(bsort)
enable_testing()

add_library(bsort bsort.c)

add_executable(bsort_test bsort_test.c)
target_link_libraries(bsort_test bsort)
add_test(bsort_test bsort_test)
