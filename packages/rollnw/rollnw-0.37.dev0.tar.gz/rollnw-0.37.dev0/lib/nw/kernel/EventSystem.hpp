#pragma once

#include "../objects/ObjectBase.hpp"
#include "Kernel.hpp"

#include <queue>
#include <tuple>

namespace nw::kernel {

enum struct EventType {
    apply_effect,
    remove_effect,
};

struct EventHandle {
    int day = 0;
    int time = 0;
    EventType type;
    ObjectBase* object = nullptr;
    void* data = nullptr;

    bool operator<(const EventHandle& rhs) const
    {
        return std::tie(day, time) < std::tie(rhs.day, rhs.time);
    }

    bool operator>(const EventHandle& rhs) const
    {
        return !(*this < rhs) && *this != rhs;
    }

    bool operator==(const EventHandle& rhs) const
    {
        return std::tie(day, time) == std::tie(rhs.day, rhs.time);
    }
};

struct EventSystem : public Service {
    template <typename T>
    using storage = std::priority_queue<T, std::vector<T>, std::greater<T>>;

    void add(EventType type, ObjectBase* object, void* data = nullptr);
    void clear() override;
    int process();
    storage<EventHandle> queue_;
};

inline EventSystem& events()
{
    auto res = services().get_mut<EventSystem>();
    if (!res) {
        throw std::runtime_error("kernel: unable to event service");
    }
    return *res;
}

} // namespace nw::kernel
