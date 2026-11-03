import matplotlib.pyplot as plt
import sys, config, json, os, trees, nodes
from typing import List

sys.dont_write_bytecode=True

def visualize(treeFile: str):
	if os.path.isfile(f"./{treeFile}.json"):
		tree = trees.read(treeFile).flatten()

		def flatten(fnodes: List[nodes.FlatNode], flatList=[]):
			curr_depth = []
			for node in fnodes:
				if node is not None:
					curr_depth.append((node.Text, len(node.ChildNodes)))
			flatList.append(curr_depth)
			children = []
			for node in fnodes:
				if len(node.ChildNodes) > 0:
					children.extend(node.ChildNodes)
			if len(children) > 0:			
				flatList = flatten(children, flatList)
			return flatList

		def get_lowest_children(fnodes: List[nodes.FlatNode], children:List[str]=[])->List[str]:
			for node in fnodes:
				if len(node.ChildNodes) == 0:
					children.append(str(node.Text))
				else:
					for child in node.ChildNodes:
						children = get_lowest_children(child.ChildNodes, children)
			return children
		
		def get_plots(flattenedList: List[tuple])->List[str]:
			plots = []
			for flat in flattenedList:
				plots.append(flat[0])
			return plots

		def get_max_x(names: List[str])->int:
			return len(max(names, key=len)) * len(names) * 0.5

		def get_max_y(allNodes: List[nodes.Node]):
			def find_node_depth(node):
				if isinstance(node, list):
					if not node:
						return 0
					return max(find_node_depth(item) for item in node)
				if not node.ChildNodes:
					return 1
				return 1 + max(find_node_depth(child) for child in node.ChildNodes)
			return 0.5 * max(find_node_depth(node) for node in allNodes)

		def get_x_coords(names: List[str], maximum:int)->List[int]:
			spacing = maximum/(len(names)+1)
			x = []
			for name in names:
				x.append((names.index(name)+1) * spacing)
			return x

		def get_y_coords(names: List[str], depth: int)->List[int]:
			return [-depth*2]*len(names)

		def plot_points(currNodes, fig, ax, max_x, depth):
			x = get_x_coords(currNodes, max_x)
			y = get_y_coords(currNodes, depth)
			for i in range(len(x)):
				ax.annotate(currNodes[i], xy=(x[i], y[i]), xytext=(0, 0), textcoords='offset points')
			plt.scatter(x, y, s=0)

		def plot_lines(currNodes, nextNodes, fig, ax, max_x, depth):
			cx = get_x_coords(get_plots(currNodes), max_x)
			cy = get_y_coords(get_plots(currNodes), depth)
			nx = get_x_coords(get_plots(nextNodes), max_x)
			ny = get_y_coords(get_plots(nextNodes), depth)
			x_values = []
			y_values = []
			already_done = 0
			for node, length in currNodes:
				x_values.append(cx[get_plots(currNodes).index(node)]+0.035)
				y_values.append(cy[get_plots(currNodes).index(node)]-0.2)
				if length > 0:
					for i in range(length):
						x_values.append(nx[i+already_done]+0.035)
						y_values.append(ny[i+already_done]-1.8)
						plt.plot(x_values, y_values, color="black", linestyle="-")
						x_values.pop()
						y_values.pop()
					already_done+=length
				x_values.clear()
				y_values.clear()
		plt.rcParams.update({'font.size': 22})
		fig, ax = plt.subplots()
		max_x = get_max_x(get_lowest_children(tree.Nodes))
		flattened = flatten(tree.Nodes)
		for i in range(len(flattened)):
			plot_points(get_plots(flattened[i]), fig, ax, max_x, i)
			if i < len(flattened)-1:
				plot_lines(flattened[i], flattened[i+1], fig, ax, max_x, i)
		plt.axis("off")
		plt.title(treeFile)
		plt.show()
	else:
		print (f"\033[90mCannot visualize \"{treeFile}\" as it does not exist\033[0m")
		sys.exit(1)
