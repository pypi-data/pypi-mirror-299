#pragma once

#include "../serialization/Serialization.hpp"
#include "ObjectBase.hpp"

#include <cstdint>
#include <variant>
#include <vector>

namespace nw {

struct Item;

struct InventoryItem {
    bool infinite = false;
    uint16_t pos_x;
    uint16_t pos_y;
    std::variant<Resref, Item*> item;
};

struct Inventory {
    Inventory() = default;
    explicit Inventory(ObjectBase* owner_)
        : owner{owner_}
    {
    }
    Inventory(const Inventory&) = delete;
    Inventory(Inventory&&) = default;
    Inventory& operator=(const Inventory&) = delete;
    Inventory& operator=(Inventory&&) = default;
    ~Inventory() = default;

    bool instantiate();

    bool from_json(const nlohmann::json& archive, SerializationProfile profile);
    nlohmann::json to_json(SerializationProfile profile) const;

    ObjectBase* owner;
    std::vector<InventoryItem> items;
};

bool deserialize(Inventory& self, const GffStruct& archive, SerializationProfile profile);
bool serialize(const Inventory& self, GffBuilderStruct& archive, SerializationProfile profile);

} // namespace nw
