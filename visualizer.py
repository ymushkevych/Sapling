import sys, os, trees, nodes

sys.dont_write_bytecode=True

def visualize(treeFile: str, modeL str) {
	if os.path.isfile(f"./{treeFile}.json"):
		tree = trees.read(treeFile).flatten()
		match mode:
			case "tv":
				pass
			case "th":
				th_visualize(tree.Nodes)
			case "dv":
				pass
			case "dh":
				pass
			case _:
				print("\033[90munrecognized visualization mode\033[0m)
	else:
		print(f"\033[90mCannot visualize tree \"{treeFile}\" as it does not exist\033[0m")
		sys.exit(1)
}

def th_visualize(fnodes: list[nodes.FlatNode], indent:int=0):
	for node in fnodes:
		if node is not None:
			if indent == 0:
				print(node.Text)
			else:
				print(f"{(indent-1)*'     '}|----{node.Text}")
			indent +=1
			th_visualize(node.ChildNodes, indddent)
			indent -=1
		else:
			if indent > 0:
				indent -=1
