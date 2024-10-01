#include "Kernel.hpp"

#include "EffectSystem.hpp"
#include "EventSystem.hpp"
#include "FactionSystem.hpp"
#include "ModelCache.hpp"
#include "Objects.hpp"
#include "Resources.hpp"
#include "Rules.hpp"
#include "Strings.hpp"
#include "TilesetRegistry.hpp"
#include "TwoDACache.hpp"

#include "../profiles/nwn1/Profile.hpp"

namespace nw::kernel {

Services::Services()
{
    // The ordering here is important.  Pretty much everything depends on strings and resman
    add<Strings>();
    add<Resources>();
    add<TwoDACache>();
    add<Rules>();
    add<EffectSystem>();
    add<ObjectSystem>();
    add<EventSystem>();
    add<ModelCache>();
    add<TilesetRegistry>();
    add<FactionSystem>();
}

void Services::start()
{
    if (config().version() == GameVersion::vEE
        || config().version() == GameVersion::v1_69) {
        profile_ = std::make_unique<nwn1::Profile>();
    } else {
        std::runtime_error("currently selected game version is unsupported");
    }

    for (auto& s : services_) {
        s.service->initialize(ServiceInitTime::kernel_start);
    }
}

GameProfile* Services::profile() const
{
    return profile_.get();
}

void Services::shutdown()
{
    for (auto& s : reverse(services_)) {
        s.service->clear();
    }

    profile_.reset();
}

Config& config()
{
    static Config s_config;
    return s_config;
}

Services& services()
{
    static Services s_services;
    return s_services;
}

Module* load_module(const std::filesystem::path& path, bool instantiate)
{
    // Always unload, just in case.
    unload_module();

    for (auto& s : services().services_) {
        s.service->initialize(ServiceInitTime::module_pre_load);
    }

    resman().load_module(path, "");

    Module* mod = objects().make_module();
    if (mod->haks.size()) {
        nw::kernel::resman().load_module_haks(mod->haks);
    }

    if (mod->tlk.size()) {
        auto path = nw::kernel::config().user_path() / "tlk";
        nw::kernel::strings().load_custom_tlk(path / (mod->tlk + ".tlk"));
    }

    for (auto& s : services().services_) {
        s.service->initialize(ServiceInitTime::module_post_load);
    }

    if (instantiate) {
        if (mod) {
            mod->instantiate();
        }

        for (auto& s : services().services_) {
            s.service->initialize(ServiceInitTime::module_post_instantiation);
        }
    }

    return mod;
}

void unload_module()
{
    for (auto& s : reverse(services().services_)) {
        s.service->clear();
    }

    resman().unload_module();
    strings().unload_custom_tlk();
}

} // namespace nw::kernel
