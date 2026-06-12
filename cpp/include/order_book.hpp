#pragma once

#include <cstdint>
#include <deque>
#include <functional>
#include <map>
#include <optional>
#include <unordered_set>
#include <vector>

namespace quant {

enum class Side {
    Buy,
    Sell
};

struct Order {
    std::int64_t id;
    Side side;
    double price;
    int quantity;
};

struct Trade {
    std::int64_t resting_order_id;
    std::int64_t incoming_order_id;
    double price;
    int quantity;
};

class OrderBook {
public:
    std::vector<Trade> add_limit_order(const Order& order);

    std::vector<Trade> add_market_order(
        std::int64_t order_id,
        Side side,
        int quantity
    );

    bool cancel_order(std::int64_t order_id);

    std::optional<double> best_bid_price() const;
    std::optional<double> best_ask_price() const;

    int total_bid_quantity() const;
    int total_ask_quantity() const;
    int live_order_count() const;

private:
    using BidBook = std::map<double, std::deque<Order>, std::greater<double>>;
    using AskBook = std::map<double, std::deque<Order>, std::less<double>>;

    BidBook bids_;
    AskBook asks_;
    std::unordered_set<std::int64_t> live_order_ids_;

    std::vector<Trade> match_buy_order(
        Order& incoming,
        std::optional<double> limit_price
    );

    std::vector<Trade> match_sell_order(
        Order& incoming,
        std::optional<double> limit_price
    );

    void add_resting_order(const Order& order);
};

}  // namespace quant