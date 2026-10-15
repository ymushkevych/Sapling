#!/usr/bin/env python3    
import argparse
import os
import time
import sys
from pathlib import Path

now = time.asctime()

parser = argparse.ArgumentParser(prog="syntree.py", usage="%(prog)s [options]", color=False)

parser.add_argument("-n", "--new", nargs=1, type=str, help="make a new tree with the given name", metavar="<name>", dest="new")
parser.add_argument("-d","--delete", nargs=1, type=str, help="delete the given tree", metavar="<tree>", dest="delete")
parser.add_argument("-r", "--rename", nargs=2, type=str, help="rename the given tree to the new name", metavar=("<old name>", "<new name>"), dest="rename")
parser.add_argument("-c", "--clear", nargs=1, type=str, help="clear the given tree without deleting it", metavar="<tree>", dest="clear")
parser.add_argument("-l", "--list", action='store_true', help="list all trees in the current directory", dest="list")

argv = parser.parse_args()

def list_trees():
  if len([item for item in Path ("./").glob("*.json") if item.is_file()]) == 0:
    print(f"No trees found in current directory")
  else:
    for tree in [item for item in Path("./").glob("*.json") if item.is_file()]:
      print(f"{str(tree).rstrip('.json')}")

def rename_tree(old_name: str, new_name: str):
  if os.path.isfile(f"{old_name}.json"):
    if os.path.isfile(f"{new_name}.json"):
      print(f"\"{new_name}\" already exists as a tree; \"{old_name}\" cannot be renamed into \"{new_name}\"")
      sys.exit(1)
    else:
      os.rename(f"{old_name}.json", f"{new_name}.json")
      if os.path.isfile(f"{new_name}.json"):
        print(f"Tree \"{old_name}\" successfully renamed to \"{new_name}\" on {now}")
      else:
        print(f"Failed to rename tree \"{old_name}\"")
        sys.exit(1)
  else:
    print(f"\"{old_name}\" cannot be renamed as it does not exist")
    sys.exit(1)

def clear_tree(name: str):
  if os.path.isfile(f"{name}.json"):
    with open(f"{name}.json") as tree:
      pass
    print(f"Tree \"{name}\" successfully cleared on {now}")
  else:
    print(f"\"{name}\" cannot be cleared as it does not exist")
    sys.exit(1)
    
def delete_tree(name: str):
  if os.path.isfile(f"{name}.json"):
    os.remove(f"{name}.json")    
    if os.path.isfile(f"{name}.json"):
      print(f"Failed to delete tree \"{name}\"")
      sys.exit(1)
    else:
      print(f"Tree \"{name}\" successfully deleted on {now}")
  else:
    print(f"\"{name}\" cannot be deleted as it does not exist")
    sys.exit(1)

def make_tree(name: str):
  if name in [item for item in Path("./").glob("*.json") if item.is_file()]:
    print("tree with that name already exists")
    sys.exit(1)
  else:
    open(f"{name}.json", "a")
    if os.path.isfile(f"{name}.json"):
      print(f"Tree \"{name}\" successfully created on {now}")
    else:
      print(f"Failed to create tree \"{name}\"")
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

if __name__ == "__main__":
  main()
