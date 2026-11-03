# Sapling
Sapling is a generator and visualizer for linguistic syntax trees. Trees are stored as `.json` files in your working directory.

Visualization is done through the python `matplotlib` library. Visualized trees can be stored as `.png`s on your device

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
  - [visualizer.py](./visualizer.py)
2. make `sapling.py` an executable 
```sh
  chmod +x ./sapling.py
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
  1. python3

     For Linux users, this is already on your device as a dependency
     
     For MacOS users, donwload [here](https://www.python.org/downloads/macos/)
     
     For Windows users, download [here](https://www.python.org/downloads/windows/)

     For BSD (Free, Net, etc.) users, download [here](https://www.python.org/downloads/source/) (other Unix-like systems also download from here)
  2. matplotlib
     
     For Linux users, download with
     ```sh
     apt install python3-matplotlib
     ```
     (^^for Ubuntu and Debian-based systems)
     
     or
     ```sh
     pip install matplotlib
     ```
     or whatever works for you 

     For users of other operating systems, I am unable to test what works and doesn't work for your system. Feel free to make a pr with the proper installation guide for your system
  
# Support

Sapling currently only supports Unix, Unix-like, and POSIX-compliant systems that implement the Unix file system, as all file paths are hard-coded to use '/' as the directory delimiter. (Note that only Linux has been actually tested on)

Windows support is planned but not a priority at the moment.
