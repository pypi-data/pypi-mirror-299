from typing import List, Type, Literal, Union, TypeVar, Generic
import ast
from ast import unparse
from .getter import get_node, SourceObjectType

T = TypeVar("T", bound=ast.AST)


class NodeCollector(ast.NodeVisitor, Generic[T]):
    def __init__(self, node_type: Type[T]):
        self.node_type = node_type
        self.nodes: List[T] = []

    def visit(self, node: ast.AST):
        if isinstance(node, self.node_type):
            self.nodes.append(node)
        self.generic_visit(node)


class NodeCollectorMulti(ast.NodeVisitor):
    def __init__(self, node_types):
        self.node_types = node_types
        self.nodes: List[T] = []

    def visit(self, node: ast.AST):
        if any([isinstance(node, node_type) for node_type in self.node_types]):
            self.nodes.append(node)
        self.generic_visit(node)


def collect_nodes(
    input: Union[str, ast.AST, SourceObjectType],
    node_type: Type[T],
    return_type: Literal["nodes", "sources"] = "nodes",
) -> Union[List[T], List[str]]:

    node = get_node(input)

    collector = NodeCollector(node_type)
    collector.visit(node)
    nodes = collector.nodes

    if return_type == "nodes":
        return nodes
    elif return_type == "sources":
        return [unparse(node) for node in nodes]

    raise ValueError("Invalid return_type")


def collect_nodes_multi(
    input: Union[str, ast.AST, SourceObjectType], node_types: List[Type[T]]
) -> List[T]:

    node = get_node(input)

    collector = NodeCollectorMulti(node_types)
    collector.visit(node)
    nodes = collector.nodes

    return nodes
