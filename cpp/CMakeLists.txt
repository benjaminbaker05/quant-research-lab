cmake_minimum_required(VERSION 3.20)

project(QuantOrderBook LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(orderbook
    src/order_book.cpp
)

target_include_directories(orderbook
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

add_executable(orderbook_demo
    src/main.cpp
)

target_link_libraries(orderbook_demo
    PRIVATE orderbook
)

add_executable(orderbook_tests
    tests/test_order_book.cpp
)

target_link_libraries(orderbook_tests
    PRIVATE orderbook
)

add_executable(orderbook_benchmark
    benchmarks/benchmark_order_book.cpp
)

target_link_libraries(orderbook_benchmark
    PRIVATE orderbook
)

enable_testing()

add_test(
    NAME orderbook_tests
    COMMAND orderbook_tests
)