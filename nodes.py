from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
import sys

sys.dont_write_bytecode=True

@dataclass
class FlatNode:
	Text: str
	ChildNodes: List[FlatNode] = field(default_factory=list)
	
@dataclass 
class Node:
	Name: str #what the node is called in data
	Text: str #what the node is displayed as
	Parent: str
	ChildNodes: List[Node] = field(default_factory=list)
  
	def __post__init__(self: Node):
		self = self
	def parent(self)->str:
		return self.Parent
	def children(self)->List[str]:
		return [child.Name for child in [node for node in self.ChildNodes if node is not None]]
	def rename(self, name: str):
		self.Name = name
	def retext(self, text: str):
		self.Text = text

	def flatten(self)->FlatNode:
		flat = FlatNode(self.Text, [])
		for child in self.ChildNodes:
			if child is not None:
				flat_child = child.flatten()
				flat.ChildNodes.append(flat_child)
		return flat
		
def new(Name: str, Text: str, Parent: str):
	return Node(Name, Text, Parent, [])
def from_raw(Name: str, Text: str, Parent: str, ChildNodes: List[Node]):
	return Node(Name, Text, Parent, ChildNodes)

