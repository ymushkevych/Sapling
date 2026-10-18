from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import nodes, sys

sys.dont_write_bytecode=True

@dataclass
class Tree:
	Name: str
	Nodes: List[nodes.Node] = field(default_factory=list)

class TreeManager:
	def __init__(self, tree: Tree):
		self.tree = tree

	def node_names(self)->list[str]:
		def collect_names(currentNode: nodes.Node, names: list[str]):
			names.append(currentNode.Name)
			for node in currentNode.ChildNodes:
				if node is not None:
					collect_names(node, names)
			return names
		node_names: list[str] = []
		for node in self.tree.Nodes:
			if node is not None:
				node_names = collect_names(node, node_names)
		return node_names

	def find_node(self, targetNodeName: str, currentNode: Optional[nodes.Node]=None)->Optional[nodes.Node]:
		if currentNode is None:
			for node in self.tree.Nodes:
				if node is not None:
					foundNode = self.find_node(targetNodeName, node)
					if foundNode is not None:
						return foundNode
			return None

		if currentNode.Name == targetNodeName:
			return currentNode

		for node in list(child for child in currentNode.ChildNodes if child is not None):
			foundNode = self.find_node(targetNodeName, node)
			if foundNode is not None:
				return foundNode
		return None

	def add_node(self, nodeName: str, nodeText: str, parent: str)->list[node.Nodes]:
		existing_nodes = self.node_names()
		if nodeName in existing_nodes:
			print(f"\033[90m\"{nodeName}\" is already a node in \"{self.tree.Name}\"\033[0m")
		else:
			if parent not in existing_nodes:
				print (f"\033[90m\"{parent}\" does not exist; it cannot be declared as the parent node; create \"{parent}\" first\033[0m")
			match self.find_node(parent):
				case None:
					pass
				case _:
					self.find_node(parent).ChildNodes.append(nodes.new(nodeName,nodeText,parent))
		return self.tree.Nodes

	def remove_node(self, nodeName: str)->list[node.Nodes]:
		existing_nodes = self.node_names()
		if nodeName not in existing_nodes:
			print(f"\033[90m\"{nodeName}\" cannot be removed as it does not exist\033[0m")
		else:
			target = self.find_node(nodeName)
			if target.ParentNode == self.tree.Name:
				self.tree.Nodes.remove(target_node)
			else:
				parent = self.find_node(target.ParentNode)
				if parent is not None and target in parent.ChildNodes:
					parent.ChildNodes.remove(target)
		return self.tree.Nodes


	class Drawer():
		pass
	class Storage():
		def __init__(self):
			pass

		def store(self, tree: Tree, fileName: str):
			with open(f"./{fileName}.json", "r+") as treeFile:
				treeJson = json.load(treeFile)

		def read(self, fileName: str):
			with open(f"./{fileName}.json", "r") as treeFile:

				treeJson = json.load(treeFile)

def new(treeName: str)->Tree:
	return Tree(treeName, [nodes.new("S", "Sentence", treeName)])
