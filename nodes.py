from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List
import sys

sys.dont_write_bytecode=True

@dataclass 
class Node:
	Name: str #what the node is called in data
	Text: str #what the node is displayed as
	ParentNode: Optional[Node] = None
	ChildNodes: List[Node] = field(default_factory=list)
  
	def _post__init__(self: Node):
		self = self
	def parent(self)->Optional[str]:
		if self.node.ParentNode:
			return self.ParentNode.Name
		else:
			return None
	def children(self)->List[str]:
		return [child.Name for child in [node for node in self.ChildNodes if node is not None]]
	def rename(self, name: str)
		self.Name = name
	def retext(self, text: str)
		self.Text = text
		
def new(Name: str, Text: str, Parent: Optional[Node]):
	return Node(Name, Text, Parent, [])
def from_raw(Name: str, Text: str, Parent: Optional[Node], ChildNodes: List[Node]):
  return Node(Name, Text, Parent, ChildNodes)

