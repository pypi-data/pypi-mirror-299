from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Node:
    """Container for a doubly linked list. The 'id' must be a hashable value."""

    id: str
    parents: set["Node"] = field(default_factory=set)
    children: set["Node"] = field(default_factory=set)

    def __str__(self):
        """Nicer string representation, which avoids infinite recursion in case of circular references."""
        return f"Node(id={self.id}, n_parents={len(self.parents)}, n_children={len(self.children)})"

    def __hash__(self):
        return hash(self.id)


def _build_tree(inp: Iterable[str, str | None]) -> dict[str, Node]:
    tree: dict[str, Node] = {}

    def _get_node(node_id: str) -> Node:
        try:
            return tree[node_id]
        except KeyError:
            new_node = Node(id=node_id)
            tree[node_id] = new_node
            return new_node

    # Tree where node -> parents
    for n, parent in inp:
        n = str(n)
        node = _get_node(n)
        if parent not in [None, "NULL"]:
            parent_node = _get_node(parent)
            node.parents.add(parent_node)
            parent_node.children.add(node)
    return tree


def _build_row(chain: list[Node]) -> dict[str, Any]:
    s = ",".join([tmp.id for tmp in chain])
    is_final = len(chain[-1].children) == 0
    row = {
        "hierarchy_string": s,
        "last_value": chain[-1].id,
        "chain_length": len(chain),
        "is_final": is_final,
    }
    for ii, node in enumerate(chain):
        row[f"level_{ii+1}"] = node.id
    return row


def _build_hierarchy_with_dfs(roots: list[Node]) -> Iterator[dict[str, Any]]:
    def _dfs(chain: list[Node]):
        yield _build_row(chain)
        n = chain[-1]
        for child in n.children:
            yield from _dfs([*chain, child])

    for root in roots:
        yield from _dfs([root])


def build_hierarchy_from_iterable(inp: Iterable[str, str | None]) -> Iterator[dict[str, Any]]:
    tree = _build_tree(inp)
    # Identify the root nodes (entities without parents)
    roots = [n for n in tree.values() if not n.parents]
    return _build_hierarchy_with_dfs(roots)
