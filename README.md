# Sapling
Sapling is a generator and visualizer* for linguistic syntax trees. Trees are stored as `.json` files in your working directory.

*The visualization process is not yet implemented

# Setup

Sapling is designed to exist within the directory of the project you are working on. This means that for every new project, you will need to grab a new copy of sapling and its modules.

Currently, sapling expects that it will exist in the exact same directory as where you store your trees. Otherwise, it will not be able to see, and therefore edit trees.

The setup process is as follows:
1. Move this repo into your project directory. You should have
  - [config.py](./config.py)
  - [nodes.py](./nodes.py)
  - [sapling.py](./sapling.py)
  - [sapling_config.toml](./sapling_config.toml)
  - [trees.py](./trees.py)
2. make `sapling.py` an executable 
```sh
  chmod + x ./sapling.py
```

# Usage

Sapling is a CLT (Command-Line Tool) that is meant to be run in the terminal.

Sapling is run as follows:
```sh
./sapling.py [options]
```

For more information including a list of commands, run:
```sh
./sapling.py -h
```
or
```sh
./sapling.py --help
```
or
```sh
./sapling.py
```

# Dependencies
  Sapling requires `python3` to work. 

  The ability to run commands from the terminal is also a necessity

# Support

Sapling currently only supports Unix, Unix-like, and POSIX-compliant systems that implement the Unix file system, as all file paths are hard-coded to use '/' as the directory delimiter
Windows support is planned but not a priority at the moment
