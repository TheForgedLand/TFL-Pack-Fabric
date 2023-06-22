import yaml
import toml
import os
import Levenshtein as le
import platform

match platform.system():
	case "Windows": extension = ".exe"
	case "Linux": extension = ""
	case _: raise OSError("Unsupported platform")

def get_modlist():
	modlist = {modname.replace(".pw.toml", "")
		for modname in os.listdir("./mods")}
	return modlist

def update_flavors(modlist):
	flavor_groups, flavors = open("pack-config/flavorgroups.toml", "r"), open("pack-config/flavors.yaml")
	_ = yaml.safe_load(flavors)
	fl = _ if _ is not None else {}

	modflavors = {modname: "srv_on" for modname in modlist} | fl
	data = toml.load(flavor_groups) | {"metafile": {k: {"flavors": v} for k, v in fl.items()}}

	_ = {(mm if mm not in fl.keys() else ...)for mm in modlist}
	newly_added = _ if _ is not {...} else {}

	_ = {(mod if mod not in modlist else ...)for mod in modflavors.keys()}
	outdated = _ if _ is not {...} else {}

	if len(outdated) > 0:
		print("These mods are being removed!!")
		[print("- ", mod) for mod in outdated]

		for mod in outdated:
			for m in modlist:
				if le.ratio(mod,m)>=0.85: # type: ignore
					print(mod,"might be related to",m);
					print('%s: %s' % (mod, modflavors.get(mod)))
			modflavors.pop(mod)

	if len(newly_added) > 0:
		print("These mods are being added!!")
		[print("- ", mod) for mod in newly_added]



	with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml", "w") as fl:
		yaml.dump(modflavors, fl)
		toml.dump(data, f)

with open("pack-config/custom_sources.yaml") as sources:
	custom_sources = yaml.safe_load(sources); sources.close()
for mod, mod_url in custom_sources.items():
	os.system("bin/packwiz%s url add %s %s" % (extension, mod, mod_url))
os.system("bin/packwiz%s refresh" % extension)
