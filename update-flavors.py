import yaml
import toml
with open("unsup.toml", "r") as f, open("flavors.yaml") as fl:
    data = toml.load(f) | {"metafile": {k: {"flavors": v.split(",")} for k, v in yaml.safe_load(fl).items()}} #type: ignore
with open("unsup.toml", "w") as f:
    toml.dump(data, f)