import yaml, toml
import os, sys, platform, pexpect
import Levenshtein as le
from pexpect.popen_spawn import PopenSpawn

match platform.system():
	case "Windows": extension = ".exe"
	case "Linux": extension = ""
	case _: raise OSError("Unsupported platform")

def getModlist():
	modlist = {modname.replace(".pw.toml", "")
		for modname in os.listdir("./mods")}
	return modlist

def updateFlavors():
	modlist = getModlist()
	flavor_groups, flavors = open("pack-config/flavorgroups.yaml", "r"), open("pack-config/flavors.yaml")

	fl = yaml.safe_load(flavors)
	flavorlist = fl if fl is not None else {}

	flls = yaml.safe_load(flavor_groups)
	flavorgrouplist = flls if flls is not None else {}

	modflavors:dict[str, str] = {modname: "misc_on" for modname in modlist} | flavorlist
	data = flavorgrouplist | {"metafile": {k: {"flavors": v} for k, v in flavorlist.items()}}

	new:set = {(mm if mm not in flavorlist.keys() else ...)for mm in modlist};new.discard(...)
	newly_added:set = set() if new is None else new

	old:set = {(mod if mod not in modlist else ...)for mod in modflavors.keys()};old.discard(...)
	outdated:set = set() if old is None else old

	if len(outdated) > 0:
		print("These mods are being removed!!")
		for mod in outdated: print("- ", mod)

		for mod in outdated:
			for m in modlist:
				if le.ratio(mod,m)>=0.85:
					print(mod,"might be related to",m);
					print('%s: %s' % (mod, modflavors.get(mod)))
			modflavors.pop(mod)

	if len(newly_added) > 0:
		print("These mods are being added!!")
		for mod in newly_added: print("- ", mod)

	with open("unsup.toml", "w") as f, open("pack-config/flavors.yaml", "w") as flavorfile:
		yaml.dump(modflavors, flavorfile)
		toml.dump(data, f)

def updateCustom():
	with open("pack-config/custom_sources.yaml") as sources:
		custom_sources = yaml.safe_load(sources); sources.close()
	for mod, mod_url in custom_sources.items():
		os.system("bin/packwiz%s url add %s %s" % (extension, mod, mod_url))

MR = "mr"
CF = "cf"
def addMod(source:str=...,mod:str=..., ):
	"""
	Mod: name or URL of the mod
	Source: name of the source.
	* cf for curseforge
	* mr for modrinth
	"""
	if source is ...: source = input("Source site [mr/cf]: ")
	if mod is ...: mod = input("Mod name/URL: ")
	packwiz = PopenSpawn(
		"bin/packwiz%s %s add %s" % (extension, source, mod),
		encoding='utf-8',
		logfile=sys.stdout
	)

	i = packwiz.expect(["Choose a number", pexpect.EOF])
	if i == 0:
		userinput = input()
		packwiz.sendline(userinput)
		if userinput == "0": print("\rCancelled!!")

def update():
	updater = PopenSpawn(
		"bin/packwiz%s update --all" % (extension),
		encoding='utf-8',
		logfile=sys.stdout)

	i = updater.expect(["Do you want to update?", pexpect.EOF])
	if i == 0:
		userinput = input()
		updater.sendline(userinput)
		if userinput in ["n", "N", "NO", "no","No"]: print("\rCancelled!")
		elif userinput in ["y","Y","Yes","yes","YES"]: print("\rFiles Updated!")

def refresh():
	updateFlavors()
	os.system("bin/packwiz%s refresh" % extension)
