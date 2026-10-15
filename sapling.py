#!/usr/bin/env python3    
import argparse
import os

parser = argparse.ArgumentParser(prog="syntree.py", usage="%(prog)s [options]", color=False)

parser.add_argument("-n", "--new", nargs=1, type=str, help="make a new tree with the given name", metavar="<name>", dest="new")
parser.add_argument("-d","--delete", nargs=1, type=str, help="delete the given tree", metavar="<tree>", dest="delete")
parser.add_argument("-r", "--rename", nargs=2, type=str, help="rename the given tree to the new name", metavar=("<old name>", "<new name>"), dest="rename")

argv = parser.parse_args()

def main():  
  if len([value for value in vars(argv).values() if value is not None]) == 0:
    parser.print_help() 
  else:  
    pass

if __name__ == "__main__":
  main()
