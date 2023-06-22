from typing import Any
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
	flavor_groups, flavors = open("pack-config/flavorgroups.yaml", "r"), open("pack-config/flavors.yaml")

	fl = yaml.safe_load(flavors)
	flavorlist = fl if fl is not None else {}

	flls = yaml.safe_load(flavor_groups)
	flavorgrouplist = flls if flls is not None else {}

	modflavors:dict[str, str] = {modname: "srv_on" for modname in modlist} | flavorlist
	data = flavorgrouplist | {"metafile": {k: {"flavors": v} for k, v in flavorlist.items()}}

	new:set = {(mm if mm not in flavorlist.keys() else ...)for mm in modlist};new.discard(...)
	newly_added:set = set() if new is None else new

	old:set = {(mod if mod not in modlist else ...)for mod in modflavors.keys()};old.discard(...)
	outdated:set = set() if old is None else old

	if len(outdated) > 0:
		print("These mods are being removed!!")
		[print("- ", mod) for mod in outdated]

		for mod in outdated:
			for m in modlist:
				if le.ratio(mod,m)>=0.85:
					print(mod,"might be related to",m);
					print('%s: %s' % (mod, modflavors.get(mod)))
			modflavors.pop(mod)

	if len(newly_added) > 0:
		print("These mods are being added!!")
		[print("- ", mod) for mod in newly_added]



	with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml", "w") as flavorfile:
		yaml.dump(modflavors, flavorfile)
		toml.dump(data, f)

update_flavors(get_modlist())

with open("pack-config/custom_sources.yaml") as sources:
	custom_sources = yaml.safe_load(sources); sources.close()
for mod, mod_url in custom_sources.items():
	os.system("bin/packwiz%s url add %s %s" % (extension, mod, mod_url))
os.system("bin/packwiz%s refresh" % extension)
