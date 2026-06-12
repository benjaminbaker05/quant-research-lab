#include "order_book.hpp"

#include <algorithm>
#include <stdexcept>

namespace quant {

std::vector<Trade> OrderBook::add_limit_order(const Order& order) {
    if (order.quantity <= 0) {
        throw std::invalid_argument("Order quantity must be positive");
    }

    if (live_order_ids_.contains(order.id)) {
        throw std::invalid_argument("Duplicate live order id");
    }

    Order incoming = order;
    std::vector<Trade> trades;

    if (incoming.side == Side::Buy) {
        trades = match_buy_order(incoming, incoming.price);
    } else {
        trades = match_sell_order(incoming, incoming.price);
    }

    if (incoming.quantity > 0) {
        add_resting_order(incoming);
    }

    return trades;
}

std::vector<Trade> OrderBook::add_market_order(
    std::int64_t order_id,
    Side side,
    int quantity
) {
    if (quantity <= 0) {
        throw std::invalid_argument("Order quantity must be positive");
    }

    if (live_order_ids_.contains(order_id)) {
        throw std::invalid_argument("Duplicate live order id");
    }

    Order incoming{
        .id = order_id,
        .side = side,
        .price = 0.0,
        .quantity = quantity
    };

    if (side == Side::Buy) {
        return match_buy_order(incoming, std::nullopt);
    }

    return match_sell_order(incoming, std::nullopt);
}

std::vector<Trade> OrderBook::match_buy_order(
    Order& incoming,
    std::optional<double> limit_price
) {
    std::vector<Trade> trades;

    while (incoming.quantity > 0 && !asks_.empty()) {
        auto best_ask = asks_.begin();
        const double ask_price = best_ask->first;

        if (limit_price.has_value() && ask_price > limit_price.value()) {
            break;
        }

        auto& queue = best_ask->second;

        while (incoming.quantity > 0 && !queue.empty()) {
            Order& resting = queue.front();

            const int trade_quantity = std::min(
                incoming.quantity,
                resting.quantity
            );

            trades.push_back(
                Trade{
                    .resting_order_id = resting.id,
                    .incoming_order_id = incoming.id,
                    .price = ask_price,
                    .quantity = trade_quantity
                }
            );

            incoming.quantity -= trade_quantity;
            resting.quantity -= trade_quantity;

            if (resting.quantity == 0) {
                live_order_ids_.erase(resting.id);
                queue.pop_front();
            }
        }

        if (queue.empty()) {
            asks_.erase(best_ask);
        }
    }

    return trades;
}

std::vector<Trade> OrderBook::match_sell_order(
    Order& incoming,
    std::optional<double> limit_price
) {
    std::vector<Trade> trades;

    while (incoming.quantity > 0 && !bids_.empty()) {
        auto best_bid = bids_.begin();
        const double bid_price = best_bid->first;

        if (limit_price.has_value() && bid_price < limit_price.value()) {
            break;
        }

        auto& queue = best_bid->second;

        while (incoming.quantity > 0 && !queue.empty()) {
            Order& resting = queue.front();

            const int trade_quantity = std::min(
                incoming.quantity,
                resting.quantity
            );

            trades.push_back(
                Trade{
                    .resting_order_id = resting.id,
                    .incoming_order_id = incoming.id,
                    .price = bid_price,
                    .quantity = trade_quantity
                }
            );

            incoming.quantity -= trade_quantity;
            resting.quantity -= trade_quantity;

            if (resting.quantity == 0) {
                live_order_ids_.erase(resting.id);
                queue.pop_front();
            }
        }

        if (queue.empty()) {
            bids_.erase(best_bid);
        }
    }

    return trades;
}

void OrderBook::add_resting_order(const Order& order) {
    if (order.side == Side::Buy) {
        bids_[order.price].push_back(order);
    } else {
        asks_[order.price].push_back(order);
    }

    live_order_ids_.insert(order.id);
}

bool OrderBook::cancel_order(std::int64_t order_id) {
    for (auto level = bids_.begin(); level != bids_.end(); ++level) {
        auto& queue = level->second;

        auto order = std::find_if(
            queue.begin(),
            queue.end(),
            [order_id](const Order& resting_order) {
                return resting_order.id == order_id;
            }
        );

        if (order != queue.end()) {
            queue.erase(order);
            live_order_ids_.erase(order_id);

            if (queue.empty()) {
                bids_.erase(level);
            }

            return true;
        }
    }

    for (auto level = asks_.begin(); level != asks_.end(); ++level) {
        auto& queue = level->second;

        auto order = std::find_if(
            queue.begin(),
            queue.end(),
            [order_id](const Order& resting_order) {
                return resting_order.id == order_id;
            }
        );

        if (order != queue.end()) {
            queue.erase(order);
            live_order_ids_.erase(order_id);

            if (queue.empty()) {
                asks_.erase(level);
            }

            return true;
        }
    }

    return false;
}

std::optional<double> OrderBook::best_bid_price() const {
    if (bids_.empty()) {
        return std::nullopt;
    }

    return bids_.begin()->first;
}

std::optional<double> OrderBook::best_ask_price() const {
    if (asks_.empty()) {
        return std::nullopt;
    }

    return asks_.begin()->first;
}

int OrderBook::total_bid_quantity() const {
    int total = 0;

    for (const auto& [price, queue] : bids_) {
        for (const auto& order : queue) {
            total += order.quantity;
        }
    }

    return total;
}

int OrderBook::total_ask_quantity() const {
    int total = 0;

    for (const auto& [price, queue] : asks_) {
        for (const auto& order : queue) {
            total += order.quantity;
        }
    }

    return total;
}

int OrderBook::live_order_count() const {
    return static_cast<int>(live_order_ids_.size());
}

}  // namespace quant