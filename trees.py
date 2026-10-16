from __future__ import annotations
import sys 
from dataclasses import dataclass
from typing import Optional, List 
import nodes
 
sys.dont_write_bytecode=True
 
@dataclass 
class Tree:
  Name: str
  Nodes: Optional[List[nodes.Node]] = field(default_factory=list)

