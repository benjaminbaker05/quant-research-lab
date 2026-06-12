#include "order_book.hpp"

#include <chrono>
#include <iostream>

int main() {
    quant::OrderBook book;

    constexpr int n_orders = 100000;

    const auto start = std::chrono::high_resolution_clock::now();

    for (int i = 0; i < n_orders; ++i) {
        const double price = 100.0 - static_cast<double>(i % 100) * 0.01;

        book.add_limit_order(
            quant::Order{
                .id = i + 1,
                .side = quant::Side::Buy,
                .price = price,
                .quantity = 10
            }
        );
    }

    for (int i = 0; i < n_orders / 2; ++i) {
        book.add_market_order(
            n_orders + i + 1,
            quant::Side::Sell,
            5
        );
    }

    const auto end = std::chrono::high_resolution_clock::now();

    const auto elapsed = std::chrono::duration<double>(end - start).count();

    const int total_operations = n_orders + n_orders / 2;
    const double operations_per_second =
        static_cast<double>(total_operations) / elapsed;

    std::cout << "Total operations: " << total_operations << "\n";
    std::cout << "Elapsed seconds: " << elapsed << "\n";
    std::cout << "Operations per second: " << operations_per_second << "\n";
    std::cout << "Remaining live orders: " << book.live_order_count() << "\n";

    return 0;
}