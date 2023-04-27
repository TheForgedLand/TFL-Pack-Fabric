import os
modlist = [modname.replace(".pw.toml", "") for modname in os.listdir("./mods")]

import toml
import yaml
with open("pack-config/flavorgroups.toml", "r") as f, open("pack-config/flavors.yaml") as fl:
    modflavors = {modname: "misc_on" for modname in modlist}|yaml.safe_load(fl)
    yaml.dump(modflavors,fl)
    data = toml.load(f) | {"metafile": {k: {"flavors": v.split(",")} for k, v in yaml.safe_load(fl).items()}} # type: ignore
with open("unsup.toml", "w") as f: toml.dump(data, f)
os.system("packwiz refresh")
