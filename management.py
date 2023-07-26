import yaml, toml
import os, sys, platform, pexpect
import Levenshtein as le
from pexpect.popen_spawn import PopenSpawn

class Pack:
	match platform.system():
		case "Windows": _extension = ".exe"
		case "Linux": _extension = ""
		case _: raise OSError("Unsupported platform")

	def __init__(self, source,flavors):
		"""
		Args:
			source: path to source file (usually pack.toml)
			flavors: path to flavor file when using unsup (usually unsup.toml)
		"""
		self.source = source
		self.flavors = flavors
		self.info = toml.load(source)

	def getModlist(self):
		modlist = {modname.replace(".pw.toml", "")
			for modname in os.listdir("./mods")}
		return modlist

	def updateFlavors(self):
		modlist = self.getModlist()
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

		with open(self.flavors, "w") as f, open("pack-config/flavors.yaml", "w") as flavorfile:
			yaml.dump(modflavors, flavorfile)
			toml.dump(data, f)

	def updateCustom(self):
		with open("pack-config/custom_sources.yaml") as sources:
			custom_sources = yaml.safe_load(sources); sources.close()
		for mod, mod_url in custom_sources.items():
			os.system("bin/packwiz%s url add %s %s" % (self._extension, mod, mod_url))

	def addMod(self,source:str=...,mod:str=..., ):
		"""
		Mod: name or URL of the mod
		Source: name of the source.
		* cf for curseforge
		* mr for modrinth
		"""
		if source is ...: source = input("Source site [mr/cf]: ")
		if mod is ...: mod = input("Mod name/URL: ")
		packwiz = PopenSpawn(
			"bin/packwiz%s %s add %s" % (self._extension, source, mod),
			encoding='utf-8',
			logfile=sys.stdout
		)

		i = packwiz.expect(["Choose a number", pexpect.EOF])
		if i == 0:
			userinput = input()
			packwiz.sendline(userinput)
			if userinput == "0": print("\rCancelled!!")

	def update(self):
		updater = PopenSpawn(
			"bin/packwiz%s update --all" % (self._extension),
			encoding='utf-8',
			logfile=sys.stdout
		)

		i = updater.expect(["Do you want to update?", pexpect.EOF])
		if i == 0:
			userinput = input()
			updater.sendline(userinput)
			if userinput in ["n", "N", "NO", "no","No"]: print("\rCancelled!")
			elif userinput in ["y","Y","Yes","yes","YES"]: print("\rFiles Updated!")

	def refresh(self):
		self.updateFlavors()
		os.system("bin/packwiz%s refresh" % self._extension)

	def export(self):



		for file in [
			self.info['name']+'-'+self.info['version']+side+'.zip'
			for side in ['[C]','[S]','']
		]:
			try:
				os.remove(file)
				print('removing file: '+file)
			except:pass
		for side in ['[C]','[S]']:
			try:
				print('\nExporting','server' if side == '[S]' else 'client','side pack...')
				exporter = PopenSpawn(
					"bin/packwiz%s cf export -s %s" % (
						self._extension,
						'server' if side == '[S]' else 'client'
					)
				)
				exporter.wait()
				print('done exporting file!')
				os.rename(
					self.info['name']+'-'+self.info['version']+".zip",
					self.info['name']+'-'+self.info['version']+side+'.zip'
				)
				print('-',self.info['name']+'-'+self.info['version']+side+'.zip','created!')
			except Exception as e: print(e)

pack = Pack("pack.toml","unsup.toml")