import yaml
import toml
import os
import Levenshtein

f,fl = open("pack-config/flavorgroups.toml", "r"), yaml.safe_load(open("pack-config/flavors.yaml"));
if fl is None: fl = {}
modlist = [modname.replace(".pw.toml", "") for modname in os.listdir("./mods")]
modflavors = {modname: "srv_on" for modname in modlist} | fl  # type: ignore
data = toml.load(f) | {"metafile": {k: {"flavors": v} for k, v in fl.items()}} # type: ignore
newly_added=[]
for mm in modlist:
    if mm not in fl.keys(): newly_added.append(mm) # type: ignore #
outdated = []
for mod in modflavors.keys():
    if mod not in modlist: outdated.append(mod)

if outdated.__len__()>0:print("These mods are being removed!!");[print("- ",mod) for mod in outdated];print("\n")
if newly_added.__len__()>0:print("These mods are being added!!");[print("- ",mod) for mod in newly_added];print("\n")

for mod in outdated:
    for m in modlist:
        if Levenshtein.ratio(mod,m)>=0.85: print(mod,"might be related to",m); print('%s: %s' % (mod, modflavors.get(mod)))
    modflavors.pop(mod)

with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml","w") as fl:
    yaml.dump(modflavors, fl)
    toml.dump(data, f)
os.system("packwiz refresh")
