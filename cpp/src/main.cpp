#include "order_book.hpp"

#include <iostream>

int main() {
    quant::OrderBook book;

    book.add_limit_order(
        quant::Order{
            .id = 1,
            .side = quant::Side::Buy,
            .price = 100.0,
            .quantity = 10
        }
    );

    book.add_limit_order(
        quant::Order{
            .id = 2,
            .side = quant::Side::Sell,
            .price = 101.0,
            .quantity = 5
        }
    );

    std::cout << "Best bid: " << book.best_bid_price().value() << "\n";
    std::cout << "Best ask: " << book.best_ask_price().value() << "\n";

    const auto trades = book.add_market_order(
        3,
        quant::Side::Buy,
        3
    );

    std::cout << "Trades executed: " << trades.size() << "\n";

    for (const auto& trade : trades) {
        std::cout
            << "Resting order: " << trade.resting_order_id
            << ", incoming order: " << trade.incoming_order_id
            << ", price: " << trade.price
            << ", quantity: " << trade.quantity
            << "\n";
    }

    std::cout << "Remaining ask quantity: "
              << book.total_ask_quantity()
              << "\n";

    return 0;
}