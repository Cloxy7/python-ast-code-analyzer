"""
Entity Extractor
================

This module extracts "entities" from Python source code.
An entity is a class, function, or method.

HOW IT WORKS:
-------------
Python's `ast` module parses source code into a tree structure.
We walk this tree and collect the nodes we care about.

KEY CONCEPTS:
-------------
1. ast.parse(code) - Converts source text to tree
2. ast.walk(tree)  - Visits every node in the tree
3. isinstance(node, ast.FunctionDef) - Checks node type
"""

import ast
from pathlib import Path
from typing import Dict, List, Any


def find_python_files(path: Path) -> List[Path]:
    """
    Find all Python files in a directory.
    """
    if path.is_file():
        return [path] if path.suffix == ".py" else []
    return list(path.rglob("*.py"))


def extract_entities_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract all entities from a single Python file.

    This is where the AST magic happens:
    1. Read the source code
    2. Parse it into an AST
    3. Walk the tree and collect entities
    """
    source_code = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source_code, filename=str(file_path))

    entities = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            entities.append({
                "type": "function",
                "name": node.name,
                "line": node.lineno,
            })
        elif isinstance(node, ast.ClassDef):
            entities.append({
                "type": "class",
                "name": node.name,
                "line": node.lineno,
            })

    return entities


# Quick test
if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
        files = find_python_files(path)
        print(f"Found {len(files)} Python files")

        for f in files[:3]:
            print(f"\n{f}:")
            entities = extract_entities_from_file(f)
            print(json.dumps(entities, indent=2))
