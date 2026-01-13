import ast  #python built-in module
import json # need for the output format

with open("sample.py", "r") as f:
    code = f.read()   #reads its entire contents as a string.

tree = ast.parse(code) #converting the source code(sample.py) into AST

functions = [] # empty lists to store information
classes = []
imports = []

for node in ast.walk(tree):  # for every node in the tree (ast.walk traverses the entire tree)
    if isinstance(node, ast.FunctionDef): #Whether the current node represents a function definition.
        functions.append({
            "name": node.name,
            "line": node.lineno
        })
    elif isinstance(node, ast.ClassDef): #Whether the node represents a class definition.
        classes.append({
            "name": node.name,
            "line": node.lineno
        })
    elif isinstance(node, ast.Import): # This records which external modules the source code depends on.
        imports.extend([n.name for n in node.names])


output = {
    "num_functions": len(functions),
    "functions": functions,
    "num_classes": len(classes),
    "classes": classes,
    "imports": imports
}

print(json.dumps(output, indent=2))