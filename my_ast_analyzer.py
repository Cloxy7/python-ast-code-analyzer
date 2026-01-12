import ast
import json

with open("sample.py", "r") as f:
    code = f.read()

tree = ast.parse(code)

functions = []
classes = []
imports = []

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        functions.append({
            "name": node.name,
            "line": node.lineno
        })
    elif isinstance(node, ast.ClassDef):
        classes.append({
            "name": node.name,
            "line": node.lineno
        })
    elif isinstance(node, ast.Import):
        imports.extend([n.name for n in node.names])


output = {
    "num_functions": len(functions),
    "functions": functions,
    "num_classes": len(classes),
    "classes": classes,
    "imports": imports
}

print(json.dumps(output, indent=2))
