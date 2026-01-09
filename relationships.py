"""
Relationship Detector
=====================

This module finds relationships between entities in the code.
The main relationship we care about: WHO CALLS WHOM.

HOW IT WORKS:
-------------
We parse the code again, but this time we track:
1. What function/method we're currently inside (the "caller")
2. Every function call we see (the "callee")

When we see `validate_items()` inside `def on_submit()`, we record:
    caller: on_submit
    callee: validate_items

WHY THIS MATTERS:
-----------------
Relationships tell us about code structure:
- If function A calls B, C, D → A is probably coordinating/orchestrating
- If function X is called by many others → X is a utility/shared function
- If changing X breaks Y → we know about the dependency

This is the foundation for "impact analysis" — understanding
what might break when you change something.

LIMITATIONS:
------------
Static analysis can't detect:
- Dynamic calls: getattr(obj, method_name)()
- Callbacks passed to other functions
- Calls made through decorators
- Runtime-only code paths

That's okay. We catch the common cases. Something is better than nothing.
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Set


def find_relationships(path: Path, entities: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Find call relationships between entities.

    Args:
        path: Root path of the codebase
        entities: Previously extracted entities (from extractor.py)

    Returns:
        Dictionary containing:
        - calls: List of {caller, callee, file, line} relationships
        - imports: List of import statements found
        - summary: Statistics about the relationships
    """
    all_calls = []
    all_imports = []

    # Get all Python files we analyzed
    if path.is_file():
        python_files = [path] if path.suffix == ".py" else []
    else:
        python_files = list(path.rglob("*.py"))

    for file_path in python_files:
        try:
            source_code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(source_code, filename=str(file_path))

            # Get relative path for cleaner output
            relative_path = str(file_path.relative_to(path.parent))

            # Find imports in this file
            imports = extract_imports(tree)
            for imp in imports:
                imp["file"] = relative_path
            all_imports.extend(imports)

            # Find function calls
            calls = extract_calls(tree, relative_path)
            all_calls.extend(calls)

        except Exception as e:
            # Skip files with errors
            pass

    # Build summary statistics
    summary = build_summary(all_calls, entities)

    return {
        "calls": all_calls,
        "imports": all_imports,
        "summary": summary,
    }


def extract_imports(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Extract all import statements from the AST.

    Handles both:
    - import foo
    - from foo import bar

    Args:
        tree: The parsed AST

    Returns:
        List of import dictionaries
    """
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # import foo, bar
            for alias in node.names:
                imports.append({
                    "type": "import",
                    "module": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                })

        elif isinstance(node, ast.ImportFrom):
            # from foo import bar, baz
            module = node.module or ""
            for alias in node.names:
                imports.append({
                    "type": "from_import",
                    "module": module,
                    "name": alias.name,
                    "alias": alias.asname,
                    "line": node.lineno,
                })

    return imports


def extract_calls(tree: ast.AST, file_path: str) -> List[Dict[str, Any]]:
    """
    Extract all function calls and track their context.

    We use a custom NodeVisitor to track:
    - Which function we're currently inside (scope)
    - Every Call node we encounter

    Args:
        tree: The parsed AST
        file_path: Path to the file (for context)

    Returns:
        List of call relationship dictionaries
    """
    # Use a custom visitor to track scope
    visitor = CallVisitor(file_path)
    visitor.visit(tree)
    return visitor.calls


class CallVisitor(ast.NodeVisitor):
    """
    Custom AST visitor that tracks function calls within their context.

    NodeVisitor is a design pattern for traversing trees.
    We override visit_* methods to handle specific node types.

    Key insight: We track "scope" — which function we're inside.
    This lets us record "function A calls function B".
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.calls = []
        self.scope_stack = []  # Stack of function names we're inside

    @property
    def current_scope(self) -> str:
        """Get the name of the function we're currently inside."""
        if self.scope_stack:
            return ".".join(self.scope_stack)
        return "<module>"  # Top-level code

    def visit_ClassDef(self, node: ast.ClassDef):
        """
        When entering a class, push its name onto the scope stack.
        """
        self.scope_stack.append(node.name)
        self.generic_visit(node)  # Visit children
        self.scope_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """
        When entering a function, push its name and look for calls inside.
        """
        self.scope_stack.append(node.name)
        self.generic_visit(node)  # This visits all children, including Call nodes
        self.scope_stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Same as visit_FunctionDef but for async functions."""
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()

    def visit_Call(self, node: ast.Call):
        """
        Found a function call! Record the relationship.

        A Call node looks like:
            call_expression(arg1, arg2, keyword=value)

        node.func is the thing being called (could be Name, Attribute, etc.)
        node.args are positional arguments
        node.keywords are keyword arguments
        """
        callee_name = self._get_call_name(node.func)

        if callee_name:  # Skip if we couldn't determine the name
            self.calls.append({
                "caller": self.current_scope,
                "callee": callee_name,
                "file": self.file_path,
                "line": node.lineno,
            })

        # Continue visiting children (calls can be nested)
        self.generic_visit(node)

    def _get_call_name(self, node) -> str:
        """
        Get the name of what's being called.

        Examples:
        - foo()         -> "foo"
        - self.foo()    -> "self.foo"
        - obj.bar.baz() -> "obj.bar.baz"
        - Foo()         -> "Foo" (constructor call)

        Args:
            node: The func part of a Call node

        Returns:
            String name of the callee, or empty string if unknown
        """
        if isinstance(node, ast.Name):
            # Simple function call: foo()
            return node.id

        elif isinstance(node, ast.Attribute):
            # Method call: obj.method() or self.method()
            parts = []
            current = node

            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value

            if isinstance(current, ast.Name):
                parts.append(current.id)

            return ".".join(reversed(parts))

        # Other cases (subscript, lambda, etc.) - skip
        return ""


def build_summary(calls: List[Dict], entities: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """
    Build summary statistics about the relationships found.

    This helps answer questions like:
    - Which functions are called most often? (hotspots)
    - Which functions call many others? (coordinators)
    - Which functions are never called? (dead code or entry points)

    Args:
        calls: List of call relationships
        entities: Dictionary of extracted entities

    Returns:
        Summary statistics dictionary
    """
    # Count how many times each function is called
    callee_counts: Dict[str, int] = {}
    for call in calls:
        callee = call["callee"]
        callee_counts[callee] = callee_counts.get(callee, 0) + 1

    # Count how many calls each function makes
    caller_counts: Dict[str, int] = {}
    for call in calls:
        caller = call["caller"]
        caller_counts[caller] = caller_counts.get(caller, 0) + 1

    # Find most-called functions (potential utilities/core functions)
    most_called = sorted(callee_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Find functions that call the most others (potential orchestrators)
    most_calling = sorted(caller_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Count total entities
    total_functions = 0
    total_classes = 0
    for file_entities in entities.values():
        for entity in file_entities:
            if entity["type"] == "class":
                total_classes += 1
                total_functions += entity.get("method_count", 0)
            elif entity["type"] == "function":
                total_functions += 1

    return {
        "total_calls": len(calls),
        "total_functions": total_functions,
        "total_classes": total_classes,
        "unique_callees": len(callee_counts),
        "most_called": most_called,
        "most_calling": most_calling,
    }
