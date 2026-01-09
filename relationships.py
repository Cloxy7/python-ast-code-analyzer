"""
Relationship Detector - Work in Progress
=========================================

Next step: find what calls what.
Starting with just extracting imports.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any


def extract_imports(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Extract all import statements from the AST.

    Handles both:
    - import foo
    - from foo import bar
    """
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    "type": "import",
                    "module": alias.name,
                    "line": node.lineno,
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append({
                    "type": "from_import",
                    "module": module,
                    "name": alias.name,
                    "line": node.lineno,
                })

    return imports


# Quick test
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        source = Path(sys.argv[1]).read_text()
        tree = ast.parse(source)
        imports = extract_imports(tree)
        for imp in imports:
            print(imp)
