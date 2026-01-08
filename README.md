# Code Analyzer

> Exploring how to build a tool that understands Python code structure.

## The Problem

I need to build something that can:
- Read Python source code
- Extract meaningful information (classes, functions)
- Show relationships between code elements

## If I Were an Intern...

*This section shows my thought process. Not just what I built, but how I approached it.*

### Day 1: Understanding the Problem

**My first question:** "What does 'code intelligence' even mean?"

I started by reading the documentation and realized: we want to help AI tools understand code better than just text. That means extracting *structure* — classes, functions, who calls whom.

**Key insight:** The problem isn't "parse code" — it's "make code queryable."

### Day 2: Research & Small Experiments

Before writing the tool, I experimented:

```python
# experiment_1.py - Can I even parse Python?
import ast
code = open("some_file.py").read()
tree = ast.parse(code)
print(ast.dump(tree))  # Wow, that's a lot of info!
```

```python
# experiment_2.py - Can I find functions?
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(node.name)  # It works!
```

**What I learned:** Python's `ast` module does the hard work. I just need to walk the tree.

## Initial Research

Looking into Python's `ast` module - it can parse source code into a tree structure.
This seems more powerful than regex for understanding code.

*More notes to come as I learn...*
