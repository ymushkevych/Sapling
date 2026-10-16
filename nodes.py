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

class NodeManager:
  def __init__(self, node: Node):
    self.node = node
  def parent(self)->Optional[str]:
    if self.node.ParentNode:
      return self.node.ParentNode.Name
    else:
      return None
  def children(self)->List[str]:
    return [child.Name for child in [node for node in self.node.ChildNodes if node is not None]]

def new(Name: str, Text: str, Parent: Option[Node]):
  return Node(Name, Text, Parent, [])
