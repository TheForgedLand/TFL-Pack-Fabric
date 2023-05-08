import yaml
import toml
import os
import Levenshtein

f,fl = open("pack-config/flavorgroups.toml", "r"), yaml.safe_load(open("pack-config/flavors.yaml"))
modlist = [modname.replace(".pw.toml", "") for modname in os.listdir("./mods")]
modflavors = {modname: "misc_on" for modname in modlist} | fl  # type: ignore

data = toml.load(f) | {"metafile": {k: {"flavors": v} for k, v in fl.items()}} # type: ignore
outdated = []
for mod in modflavors.keys():
    if mod not in modlist:
        outdated.append(mod)
print("These mods are being removed!!\n",outdated)
for mod in outdated:
    modflavors.pop(mod)
    for m in modlist:
        if Levenshtein.ratio(mod,m)>=0.85: print(mod,"is probably related to",m)


with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml","w") as fl:
    yaml.dump(modflavors, fl)
    toml.dump(data, f)
os.system("packwiz refresh")
