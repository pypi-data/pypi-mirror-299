from dataclasses import dataclass, field
import re
from typing import List, Dict, Any
from uuid import UUID, uuid4

@dataclass
class Node:
    """
    Represents a node (vertex) in the graph.
    """
    name: str
    labels: List[str]
    uuid: UUID = field(default_factory=uuid4)
    properties: Dict[str, Any] = field(default_factory=dict)
    _properties: Dict[str, Any] = field(init=False, repr=False)
    
    def __post_init__(self):
        valid_label = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
        for label in self.labels:
            if not valid_label.match(label):
                raise ValueError(f"Invalid label: '{label}'. Labels must start with a letter and contain only alphanumeric characters and underscores.")

    def __str__(self) -> str:
        labels_str = ":".join(self.labels)
        return f'(:{labels_str} {self.properties})'

    def __hash__(self):
        return hash(self.uuid)

    @property
    def properties(self) -> Dict[str, Any]:
        return {"uuid": str(self.uuid), "name": self.name, **self._properties}
    
    @properties.setter
    def properties(self, properties: Dict[str, Any]) -> None:
        self._properties = properties if isinstance(properties, dict) else {}


@dataclass
class Relationship:
    """
    Represents a relationship (edge) between two nodes in the graph.
    """
    source: Node
    type: str
    target: Node
    properties: Dict[str, Any] = field(default_factory=dict)


    def __str__(self) -> str:
        _properties = str(self.properties) if self.properties else ''
        return f'{self.source}-[:{self.type} {_properties}]->{self.target}'

    def __hash__(self):
        return hash((self.source, self.type, self.target))


@dataclass
class Graph:
    """
    Represents a graph that contains nodes and relationships.
    """
    nodes: List[Node] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)

    def add_node(self, node: Node):
        """
        Adds a node to the graph if it doesn't already exist.
        """
        if node not in self.nodes:
            self.nodes.append(node)

    def add_relationship(self, relationship: Relationship):
        """
        Adds a relationship to the graph, ensuring the nodes exist.
        """
        self.add_node(relationship.source)
        self.add_node(relationship.target)
        
        if relationship not in self.relationships:
            self.relationships.append(relationship)
