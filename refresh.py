import yaml
import toml
import os
import Levenshtein as le


def get_modlist():
    modlist = {modname.replace(".pw.toml","") for modname in os.listdir("./mods")}
    return modlist

def update_flavors(modlist):
    flavor_groups,flavors = open("pack-config/flavorgroups.toml", "r"), open("pack-config/flavors.yaml")
    _=yaml.safe_load(flavors); fl= _ if _ is not None else {} # type: ignore

    modflavors = {modname: "srv_on" for modname in modlist} | fl  # type: ignore
    data = toml.load(flavor_groups) | {"metafile": {k: {"flavors": v} for k, v in fl.items()}} # type: ignore

    newly_added={(mm if mm not in fl.keys() else ...)for mm in modlist}; newly_added.remove(...) # type: ignore
    outdated={(mod if mod not in modlist else ...)for mod in modflavors.keys()}; outdated.remove(...)

    if len(outdated)>0:print("These mods are being removed!!");[print("- ",mod) for mod in outdated]
    if len(newly_added)>0:print("These mods are being added!!");[print("- ",mod) for mod in newly_added]

    _={(
        print(mod, "might be related to", m) if le.ratio(mod, m) > 0.85 else None, # type: ignore
        print('%s: %s' % (mod, modflavors.get(mod)))
        ) for mod in outdated for m in modlist}
    _={modflavors.pop(mod)for mod in outdated}

    with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml","w") as fl:
        yaml.dump(modflavors, fl)
        toml.dump(data, f)

update_flavors(get_modlist())
os.system("packwiz refresh")
