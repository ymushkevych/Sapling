from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import nodes, sys, os, json, config

sys.dont_write_bytecode=True

@dataclass
class FlatTree:
	Nodes: List[nodes.FlatNode] = field(default_factory = List)

@dataclass
class Tree:
	Name: str
	Nodes: List[nodes.Node] = field(default_factory=list)

	def __post__init__(self: Tree):
		self = self

	def flatten(self)->FlatTree:
		flat = FlatTree([])
		for node in self.Nodes:
			flat.Nodes.append(node.flatten())
		return flat

	def node_names(self)->List[str]:
		def collect_names(currentNode: nodes.Node, names: List[str])->List[str]:
			names.append(currentNode.Name)
			for node in currentNode.ChildNodes:
				if node is not None:
					collect_names(node, names)
			return names
		node_names: List[str] = []
		for node in self.Nodes:
			if node is not None:
				node_names = collect_names(node, node_names)
		return node_names

	def find_node(self, targetNodeName: str, currentNode: Optional[nodes.Node]=None)->Optional[nodes.Node]:
		if currentNode is None:
			for node in self.Nodes:
				if node is not None:
					foundNode = self.find_node(targetNodeName, node)
					if foundNode is not None:
						return foundNode
			return None

		if currentNode.Name == targetNodeName:
			return currentNode

		for node in List(child for child in currentNode.ChildNodes if child is not None):
			foundNode = self.find_node(targetNodeName, node)
			if foundNode is not None:
				return foundNode
		return None

	def add_node(self, nodeName: str, nodeText: str, parent: str)->List[node.Nodes]:
		if parent ==  self.Name:
			print(f"\033[90mONly one top-level node allowed per tree\033[0m")
			return self.Nodes
		existing_nodes = self.node_names()
		if nodeName in existing_nodes:
			print(f"\033[90m\"{nodeName}\" is already a node in \"{self.Name}\"\033[0m")
		else:
			if parent not in existing_nodes:
				print (f"\033[90m\"{parent}\" does not exist; it cannot be declared as the parent node; create \"{parent}\" first\033[0m")
			match self.find_node(parent):
				case None:
					pass
				case _:
					self.find_node(parent).ChildNodes.append(nodes.new(nodeName,nodeText,parent))
		return self.Nodes

	def remove_node(self, nodeName: str)->List[node.Nodes]:
		existing_nodes = self.node_names()
		if nodeName not in existing_nodes:
			print(f"\033[90m\"{nodeName}\" cannot be removed as it does not exist\033[0m")
		else:
			target = self.find_node(nodeName)
			if target.Parent == self.Name:
				self.Nodes.remove(target_node)
			else:
				parent = self.find_node(target.Parent)
				if parent is not None and target in parent.ChildNodes:
					parent.ChildNodes.remove(target)
		return self.Nodes

	def rename_node(self, oldName: str, newName:str)->List[nodes.Node]:
		existing_nodes = self.node_names()
		if oldName in existing_nodes:
			print(f"\033[90m\"{oldName}\" cannot be renamed as it does not exist\033[0m")
		else:
			if newName in exsting names:
				print(f"\033[90mCannot rename \"{oldName}\" to \"{newName}\" as that would create a naming conflict\033[0m")
			else:
				self.find_node(oldName).rename(newName)
		return self.Nodes
	
	def retext_node(self, nodeName: str, newText:str)->List[nodes.Node]:
		existing_nodes = self.node_names()
		if oldName in existing_nodes:
			print(f"\033[90mThe text of \"{nodeName}\" cannot be changed as it does not exist\033[0m")
		else:
			self.find_node(nodeName).retext(newText)
		return self.Nodes

	def store(self, fileName: str):
		def store_node(node: Node, text: str):
			if len(node.ChildNodes) == 0:
				text+=f"\n\"{node.Name}\": \"{node.Text}\""    
				if self.find_node(node.Parent) is not None:
					if self.find_node(node.Parent).ChildNodes.index(node) != len(self.find_node(node.Parent).ChildNodes)-1:
						text+=","
				else:
					text+=f"\n\"{node.Name}\": [\"{node.Text}\", {{"
					for child in node.ChildNodes:
						if node is not None:
							text = store_node(child, text)
					text+="\n}]"
					if self.Name != node.Parent:
						if self.find_node(node.Parent).ChildNodes.index(node) != len(self.find_node(node.Parent).ChildNodes)-1:
							text+=","
				return text
		with open(fileName, "w") as treeFile:
			treeFile.write("{")
			treeFile.write(f"\n\"Name\": \"{self.Name}\",") 
			treeFile.write("\n\"Nodes\": {")
			for node in self.Nodes:
				if node is not None:
					treeFile.write(store_node(node, ""))
			treeFile.write("\n}")  
			treeFile.write("\n}\n")
			
def split(self, node: str, name: str, split_kind: str)->Tree:
	existing_nodes = self.node_names()
	split_tree = new(name)
	if node not in existing_nodes:
		print (f"\033[90mCannot split at node \"{node}\" as it does not exist")
	else:
		match split_kind:
			case "inclusive_preserve":
				split_tree.find_node(config.rootname()).ChildNodes.append(self.find_node(node))
			case "uninclusive_preserve":
				for child in self.find_node(node).ChildNodes:
					if child is not None:
						split_tree.find_node(config.rootname()).ChildNodes.append(child)
						split_tree.find_node(child.Name).Parent = config.rootname()
			case "inclusive":
				split_tree.find_node(config.rootname()).ChildNodes.append(self.find_node(node))
				self.Nodes = self.remove_node(node)
				self.store(f"./{self.Name}.json")
				case "uninclusive":
				for child in self.find_node(node).ChildNodes:
					if child is not None:
						split_tree.find_node(config.rootname()).ChildNodes.append(child)
						split_tree.find_node(child.Name).Parent = config.rootname()
				self.find_node(node).ChildNodes = []
				self.store(f"./{self.Name}.json")
	return split_tree

	def copy(self, node: str,name: str, clusivity: str)->list[nodes.Node]:
		other_nodes = read({name}).node_names()
		node_buffer: list[nodes.Node] = []
		match clusivity:
			case "inclusive":
				if name in other_nodes and name != config.rootname():
					print (f"\033[90mcannot perform inclusive copy of \"{node}\" in \"{self.Name}\" to \"{name}\" as it would create a naming conflict\033[0m")
					return node_buffer
				else:
					for child in self.find_node(node).ChildNodes:
						if child is not None:
							if child.Name in other_nodes:
								print (f"\033[90mcannot perform inclusive copy of \"{node}\" in \"{self.Name}\" to \"{name}\" as it would create a naming conflict\033[0m")
								return node_buffer
					node_buffer.append(self.find_node(node))
			case "uninclusive":
				for child in self.find_node(node).ChildNodes:
					if child is not None:
						if child.Name in other_nodes:
							print (f"\033[90mcannot perform uninclusive copy of \"{node}\" in \"{self.Name}\" to \"{name}\" as it would create a naming conflict\033[0m") 
							return node_buffer
				node_buffer.append(self.find_node(node))
		for node in node_buffer:
			if node is not None:
				node.Parent = config.rootname()
		return node_buffer

def read(self, fileName: str):
	def read_nodes(node, previous, treeJson)->nodes.Node:
		if type(treeJson[node]) != List
			return nodes.new(node, treeJson[node], previous)
		else: 
			new_node = nodes.new(node, treeJson[node][0], previous)
			for child in treeJson[node][1]:
				new_node.ChildNodes.append(read_nodes(child, node, treeJson[node][1])
			return new_node
	with open(f"./{fileName}.json", "r") as treeFile:
		if os.path.getsize(f"./fileName}.json") <= 5:
			return new(fileName)
		treeJson = json.load(treeFile)
		tree: Tree == new(treeJson['Name'])
		tree.Nodes = []
		for node in treeJson['Nodes']:
			if node is not None:
				tree.Nodes.append(read_nodes(node, fileName, treeJson['Nodes']))
		return tree
def new(treeName: str)->Tree:
	return Tree(treeName, [nodes.new(config.rootname(), config.roottext(), treeName)])
