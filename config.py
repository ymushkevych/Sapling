import sys, os, tomllib

sys.dont_write_bytecode = True

def config_exists()->bool:
	return os.path.isfile("./sapling_config.toml")

def is_config_formatted()->bool:
	with open("./sapling_config.toml", "rb") as c:
		toml = tomllib.load(c)
		if "Project_Details" not in toml.keys() or "Tree_Details" not in toml.keys():
			return False
		if "argument_separator" not in toml["Project_Details"].keys() or "save_when_exiting" not in toml["Project_Details"].keys():
			return False
		if "root_name" not in toml["Tree_Details"].keys() or "root_text" not in toml["Tree_Details"].keys():
			return False
		if type(toml["Project_Details"]["argument_separator"]) != str or toml["Project_Details"]["argument_separator"] == "" or toml["Project_Details"]["argument_separator"].isspace():
			return False
		if type(toml["Project_Details"]["save_when_exiting"]) != str or toml["Project_Details"]["save_when_exiting"] == "" or toml["Project_Details"]["save_when_exiting"].isspace() or toml["Project_Details"]["save_when_exiting"] not in ["True", "False"]:
			return False
		if type(toml["Tree_Details"]["root_name"]) != str or toml["Tree_Details"]["root_name"] == "" or toml["Tree_Details"]["root_name"].isspace():
			return False
		if type(toml["Tree_Details"]["root_text"]) != str or toml["Tree_Details"]["root_text"] == "" or toml["Tree_Details"]["root_text"].isspace():
			return False
	return True

def store(settings: dict[str]):
	with open("./sapling_config.toml", "w") as f:
		f.write("[Project_Details]\n")
		f.write(f"\targument_separator = \"{settings['argsep']}\"\n")
		f.write(f"\tsave_when_exiting = \"{settings['saveonexit']}\"\n")
		f.write("[Tree_Details]\n")
		f.write(f"\troot_name = \"{settings['rootname']}\"\n")
		f.write(f"\troot_text = \"{settings['roottext']}\"")
	return 0

def argsep():
	return str(tomllib.load(open("./sapling_config.toml", "rb"))["Project_Details"]["argument_separator"])

def saveonexit():
	if str(tomllib.load(open("./sapling_config.toml", "rb"))["Project_Details"]["save_when_exiting"]) == "True":
		return True
	else:
		return False

def rootname():
	return str(tomllib.load(open("./sapling_config.toml", "rb"))["Tree_Details"]["root_name"])

def roottext():
	return str(tomllib.load(open("./sapling_config.toml", "rb"))["Tree_Details"]["root_text"])

