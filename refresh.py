import yaml
import toml
import os
import tempfile
for x in os.listdir("./mods"):
    x.replace(".pw.toml", "")

os.system("packwiz refresh")
with open("pack-config/flavorgroups.toml", "r") as f, open("pack-config/flavors.yaml") as fl:
    data = toml.load(f) | {"metafile": {k: {"flavors": v.split(",")} for k, v in yaml.safe_load(fl).items()}} # type: ignore
with open("unsup.toml", "w") as f: toml.dump(data, f)
