import yaml, toml
import os, sys, platform
import Levenshtein as le
from pexpect.popen_spawn import PopenSpawn as ps
import pexpect as px
import re

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
		SuccessfulUpdates=[]
		FailedUpdates=[]
		with open("pack-config/custom_sources.yaml") as sources:
			custom_sources = yaml.safe_load(sources); sources.close()
		for mod, mod_url in custom_sources.items():
			customUpdater = ps(
				'bin/packwiz%s url add "%s" %s' % (self._extension, mod, mod_url),
				encoding='utf-8',
			)
			customUpdater.expect(px.EOF)
			log=customUpdater.before
			status = re.match("(?:Success)|(?:Fail)",log).group(0)# type: ignore
			if status == "Success":
				localPath=re.search("\(.*\)",log).group(0) # type: ignore
				SuccessfulUpdates.append([mod,localPath,mod_url])
			elif status == "Fail": FailedUpdates.append(mod)
			else: print('\n---------------------------\n',log,'\n---------------------------\n')
		if len(FailedUpdates) <= 0: pass
		else:
			print("Failed updating:")
			for mod in FailedUpdates: print("- "+mod)
		if len(SuccessfulUpdates) <= 0:pass
		else:
			print('Succesfully updated:')
			for mod,path,url in SuccessfulUpdates: print("- %s %s" %(mod,path))

			# os.system('bin/packwiz%s url add "%s" %s' % (self._extension, mod, mod_url))

	def addMod(self,source:str=...,mod:str=..., ):
		"""
		Mod: name or URL of the mod
		Source: name of the source.
		* cf for curseforge
		* mr for modrinth
		"""
		if source is ...: source = input("Source site [mr/cf]: ")
		if mod is ...: mod = input("Mod name/URL: ")
		packwiz = ps(
			"bin/packwiz%s %s add %s" % (self._extension, source, mod),
			encoding='utf-8',
		)

		i = packwiz.expect(["Choose a number", px.EOF])
		print(packwiz.before)
		if i == 0:
			packwiz.sendline(input("Choose a number: "))
			print(packwiz.readlines()[-1])

	def update(self):
		p = re.compile(r'A supported update system for ".*" cannot be found\.\n')
		updater = ps(
			"bin/packwiz%s update --all" % (self._extension),
			encoding='utf-8',
		)

		i = updater.expect([r"Do you want to update\?", px.EOF])
		print(p.sub("",updater.before)) # type: ignore
		if i == 0:
			userinput = input()
			updater.sendline(userinput)
			print(updater.readlines()[-1])

	def refresh(self):
		self.updateFlavors()
		os.system("bin/packwiz%s refresh" % self._extension)

	def export(self):
		pattern=re.compile(
			"(Disclaimer:.*\n)"
			+"|(Note that mods bundled.*\n)"
			+"|(packwiz is currently unable to match metadata.*\n)",
			re.M
		)


		for file in [
			self.info['name']+'-'+self.info['version']+side+'.zip'
			for side in ['[C]','[S]','']
		]:
			try:
				os.remove(file)
				print('removing file: '+file)
			except:pass
		print()
		for side in ['[C]','[S]']:
			print("------------------------------------------")
			print()
			print('Exporting','server' if side == '[S]' else 'client','side pack...')
			exporter = ps(
				"bin/packwiz%s cf export -s %s" % (
					self._extension,
					'server' if side == '[S]' else 'client',
				),
				encoding='utf-8'
			)
			i=exporter.expect(["Error","failed",px.EOF])
			print(pattern.sub('',exporter.before)) # type: ignore
			if i in [0,1]: pass
			elif i == 2:
				print("renaming...")
				os.rename(
					self.info['name']+'-'+self.info['version']+".zip",
					self.info['name']+'-'+self.info['version']+side+'.zip'
				)
				print('-',self.info['name']+'-'+self.info['version']+side+'.zip','created!\n')
			print()

pack = Pack("pack.toml","unsup.toml")

def updateAll():
	print()
	pack.update()
	print()
	pack.updateCustom()
	print()
	pack.updateFlavors()
	print()
	pack.refresh()
