#include "order_book.hpp"

#include <cassert>
#include <iostream>

void test_add_limit_order_creates_best_bid() {
    quant::OrderBook book;

    book.add_limit_order(
        quant::Order{
            .id = 1,
            .side = quant::Side::Buy,
            .price = 100.0,
            .quantity = 10
        }
    );

    assert(book.best_bid_price().has_value());
    assert(book.best_bid_price().value() == 100.0);
    assert(book.total_bid_quantity() == 10);
    assert(book.live_order_count() == 1);
}

void test_crossing_sell_order_matches_bid() {
    quant::OrderBook book;

    book.add_limit_order(
        quant::Order{
            .id = 1,
            .side = quant::Side::Buy,
            .price = 100.0,
            .quantity = 10
        }
    );

    const auto trades = book.add_limit_order(
        quant::Order{
            .id = 2,
            .side = quant::Side::Sell,
            .price = 99.0,
            .quantity = 4
        }
    );

    assert(trades.size() == 1);
    assert(trades[0].resting_order_id == 1);
    assert(trades[0].incoming_order_id == 2);
    assert(trades[0].price == 100.0);
    assert(trades[0].quantity == 4);
    assert(book.total_bid_quantity() == 6);
}

void test_market_order_respects_fifo() {
    quant::OrderBook book;

    book.add_limit_order(
        quant::Order{
            .id = 1,
            .side = quant::Side::Sell,
            .price = 101.0,
            .quantity = 5
        }
    );

    book.add_limit_order(
        quant::Order{
            .id = 2,
            .side = quant::Side::Sell,
            .price = 101.0,
            .quantity = 7
        }
    );

    const auto trades = book.add_market_order(
        3,
        quant::Side::Buy,
        8
    );

    assert(trades.size() == 2);

    assert(trades[0].resting_order_id == 1);
    assert(trades[0].quantity == 5);

    assert(trades[1].resting_order_id == 2);
    assert(trades[1].quantity == 3);

    assert(book.total_ask_quantity() == 4);
}

void test_cancel_order() {
    quant::OrderBook book;

    book.add_limit_order(
        quant::Order{
            .id = 10,
            .side = quant::Side::Buy,
            .price = 99.5,
            .quantity = 20
        }
    );

    const bool cancelled = book.cancel_order(10);

    assert(cancelled);
    assert(!book.best_bid_price().has_value());
    assert(book.live_order_count() == 0);
}

void test_non_crossing_orders_do_not_match() {
    quant::OrderBook book;

    const auto buy_trades = book.add_limit_order(
        quant::Order{
            .id = 1,
            .side = quant::Side::Buy,
            .price = 99.0,
            .quantity = 10
        }
    );

    const auto sell_trades = book.add_limit_order(
        quant::Order{
            .id = 2,
            .side = quant::Side::Sell,
            .price = 101.0,
            .quantity = 10
        }
    );

    assert(buy_trades.empty());
    assert(sell_trades.empty());

    assert(book.best_bid_price().value() == 99.0);
    assert(book.best_ask_price().value() == 101.0);
}

int main() {
    test_add_limit_order_creates_best_bid();
    test_crossing_sell_order_matches_bid();
    test_market_order_respects_fifo();
    test_cancel_order();
    test_non_crossing_orders_do_not_match();

    std::cout << "All order book tests passed\n";

    return 0;
}