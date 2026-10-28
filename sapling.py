#!/usr/bin/env -S python3 -B

import time, argparse, os, sys, nodes, trees, config
from pathlib import Path

sys.dont_write_bytecode=True

now = time.asctime()

parser = argparse.ArgumentParser(prog="sapling.py", usage="%(prog)s [options]", color=False, description="Linguistic syntax tree manager and visualizer")

parser.add_argument("-n", "--new", nargs=1, type=str, help="make a new tree with the given name", metavar="<name>", dest="new")
parser.add_argument("-d","--delete", nargs=1, type=str, help="delete the given tree", metavar="<tree>", dest="delete")
parser.add_argument("-r", "--rename", nargs=2, type=str, help="rename the given tree to the new name", metavar=("<old name>", "<new name>"), dest="rename")
parser.add_argument("-c", "--clear", nargs=1, type=str, help="clear the given tree without deleting it", metavar="<tree>", dest="clear")
parser.add_argument("-l", "--list", action='store_true', help="list all trees in the current directory", dest="list")
parser.add_argument("-e", "--edit", nargs=1, type=str, help="edit the given tree", metavar="<tree>", dest="edit")
parser.add_argument("-s", "--settings", action='store_true', help="configure the settings", dest="configure")

argv = parser.parse_args()

def configure_settings():
  def parse_configure_settings_commands(cmds: list[str])->dict[str]:
    settings: dict[str] = {"argsep": config.argsep(), "saveonexit": config.saveonexit(), "rootname": config.rootname(), "roottext": config.roottext()}
    match cmds[0].strip():
      case "set":
        if len (cmds) == 1:
          print ("\033[90mExpected configuration item to change\033[0m")
        else:
          match cmds[1].strip():
            case "rootname":
              if len (cmds) == 3:
                settings["rootname"] = cmds[2].strip()
              else:
                print (f"\033[90mToo many arguments passed. Expected 2, got {len(cmds)-1}\033[0m")
            case "roottext":
              if len (cmds) == 3:
                settings["roottext"] = cmds[2].strip()
              else:
                print (f"\033[90mToo many arguments passed. Expected 2, got {len(cmds)-1}\033[0m")
            case "argsep":
              if len (cmds) == 3:
                settings["argsep"] = cmds[2].strip()
              else:
                print (f"\033[90mToo many arguments passed. Expected 2, got {len(cmds)-1}\033[0m")
            case "saveonexit":
              if len (cmds) == 3:
                if cmds[2].strip() in ["True", "False"]:
                  settings["saveonexit"] = cmds[2].strip()
                else:
                  print ("\033[90mImproper value used when configuring settings\033[0m")
              else:
                print (f"\033[90mToo many arguments passed. Expected 2, got {len(cmds)-1}\033[0m")
        return settings
      case "save":
        config.store(settings)
      case _:
        print ("\033[90munrecognized command\033[0m")
  saveonexit: bool = config.saveonexit()
  argSep: str = config.argsep()
  cmd = str(input("\033[90m- \033[0m"))
  settings: dict[str] = {"argsep": config.argsep(), "saveonexit": config.saveonexit(), "rootname": config.rootname(), "roottext": config.roottext()}
  while str(cmd).lower() != "done":
    cmdarr = cmd.split(argSep)
    settings = parse_configure_settings_commands(cmdarr)
    cmd = str(input("\033[90m- \033[0m"))
  if saveonexit:
    config.store(settings)
  else:
    return 0

def edit_tree(name: str):
  def parse_edit_tree_commands(tree: trees.Tree, cmds: list[str]):
    match cmds[0].strip():
      case "add":
        if len (cmds) == 4:
          tree.Nodes = tree.add_node(cmds[1].strip(), cmds[2].strip(), cmds[3].strip())
        else:
          print(f"\033[90mToo little or too many arguments passed. Expected 3, got {len(cmds)-1}\033[0m")
      case "remove":
        if len(cmds) == 2:
          tree.Nodes = tree.remove_node(cmds[1].strip())
        else:
          print(f"\033[90mToo little or too many arguments passed. Expected 1, got {len(cmds)-1}\033[0m")
      case "help":
        print (f"\033[90m\x1b[1mAddingNodes\x1b[0m \033[90madd {argSep} <name> {argSep} <text> {argSep} <parent name>\033[0m")
        print (f"\033[90m\x1b[1mRemovingNodes\x1b[0m \033[90mremove {argSep} <name>\033[0m")
        print (f"\033[90m\x1b[1mFinishEditing\x1b[0m \033[90mdone\033[0m")
        print (f"\033[90m\x1b[1mSave\x1b[0m \033[90msave\033[0m")
      case "save":
        tree.store(f"./{tree.Name}.json")
      case _:
        print ("\033[90munrecognized command\033[0m")
  argSep: str = config.argsep()
  saveonexit: bool = config.saveonexit()
  if os.path.isfile(f"./{name}.json"):
    cmd = str(input("\033[90m- \033[0m"))
    tree: trees.Tree = trees.read(name)
    while str(cmd).lower() != "done":
      cmdarr = cmd.split(argSep)
      parse_edit_tree_commands(tree, cmdarr)
      cmd = str(input("\033[90m- \033[0m"))
    if saveonexit:
      tree.store(f"./{tree.Name}.json")
    else:
      return 0
  else:
    print(f"\033[90m\"{name}\" cannot be edited as it does not exist\033[0m")
    sys.exit(1)


def list_trees():
	if len([item for item in Path ("./").glob("*.json") if item.is_file()]) == 0:
		print(f"\033[90mNo trees found in current directory\033[0m")
	else:
		for tree in [item for item in Path("./").glob("*.json") if item.is_file()]:
			print(f"\033[90m{str(tree).rstrip('.json')} : {str(tree)}\033[0m")

def rename_tree(old_name: str, new_name: str):
	if os.path.isfile(f"{old_name}.json"):
		if os.path.isfile(f"{new_name}.json"):
			print(f"\033[90m\"{new_name}\" already exists as a tree; \"{old_name}\" cannot be renamed into \"{new_name}\"\033[0m")
			sys.exit(1)
		else:
			os.rename(f"{old_name}.json", f"{new_name}.json")
			if os.path.isfile(f"{new_name}.json"):
				print(f"\033[90mTree \"{old_name}\" successfully renamed to \"{new_name}\" on {now}\033[0m")
			else:
				print(f"\033[90mFailed to rename tree \"{old_name}\"\033[0m")
				sys.exit(1)
	else:
		print(f"\033[90m\"{old_name}\" cannot be renamed as it does not exist\033[0m")
		sys.exit(1)

def clear_tree(name: str):
	if os.path.isfile(f"{name}.json"):
		with open(f"{name}.json") as tree:
			tree = ""
		print(f"\033[90mTree \"{name}\" successfully cleared on {now}\033[0m")
	else:
		print(f"\033[90m\"{name}\" cannot be cleared as it does not exist\033[0m")
		sys.exit(1)

def delete_tree(name: str):
	if os.path.isfile(f"{name}.json"):
		os.remove(f"{name}.json")
		if os.path.isfile(f"{name}.json"):
			print(f"\033[90mFailed to delete tree \"{name}\"\033[0m")
			sys.exit(1)
		else:
			print(f"\033[90mTree \"{name}\" successfully deleted on {now}\033[0m")
	else:
		print(f"\033[90m\"{name}\" cannot be deleted as it does not exist\033[0m")
		sys.exit(1)

def make_tree(name: str):
	if name in [item for item in Path("./").glob("*.json") if item.is_file()]:
		print("\033[90mTree with that name already exists\033[0m")
		sys.exit(1)
	else:
		open(f"{name}.json", "a")
		if os.path.isfile(f"{name}.json"):
			print(f"\033[90mTree \"{name}\" successfully created on {now}\033[0m")
		else:
			print(f"\033[90mFailed to create tree \"{name}\"\033[0m")
			sys.exit(1)

def main():
	if len([value for value in vars(argv).values() if value is not None if value is not False]) == 0:
		parser.print_help()
	else:
		match argv.new:
			case None:
				pass
			case _:
				make_tree(argv.new[0])
		match argv.delete:
			case None:
				pass
			case _:
				delete_tree(argv.delete[0])
		match argv.rename:
			case None:
				pass
			case _:
				rename_tree(argv.rename[0], argv.rename[1])
		match argv.list:
			case False:
				pass
			case True:
				list_trees()
		match argv.clear:
			case None:
				pass
			case _:
				clear_tree(argv.clear[0])
		match argv.edit:
			case None:
				pass
			case _:
				edit_tree(argv.edit[0])
		match argv.configure:
			case False:
				pass
			case True:
				configure_settings()

if __name__ == "__main__":
	if config.config_exists():
		if config.is_config_formatted():
			main()
		else:
			print("\033[90mConfig file is not configured properly\033[0m")
	else:
		print("\033[90mConfig file not found\033[0m")
	sys.exit(1)
