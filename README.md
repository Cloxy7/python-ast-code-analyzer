# Code Analyzer - Reference Implementation

> **For AI Internship Candidates**: This is a working example of what you might build.
> The goal isn't to copy this — it's to **understand the concepts** and build your own version.

---

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

### Day 3: Building the MVP

I decided to focus on THREE things only:
1. Extract functions and classes
2. Find what calls what
3. Print useful output

Everything else is scope creep. Ship something that works.

### Day 4: Polish & Document

Spent time on:
- Comments explaining WHY, not just WHAT
- A README that helps others learn
- Example output so people can see what it does

**What I'd do differently next time:**
- Start with the output format first (what do I want to see?)
- Write tests earlier (caught bugs manually that tests would've found)
- Talk to other interns sooner (they had useful ideas)

---

## What This Tool Does

```
INPUT:  A directory containing Python source code
OUTPUT: Extracted entities, relationships, and insights
```

---

## Why We Built It This Way

### Design Decisions (Read This!)

| Decision | Why |
|----------|-----|
| **Plain Python** | No frameworks to learn. Focus on the concepts. |
| **Standard library only** | `ast`, `pathlib`, `json` — nothing to install. |
| **Small modules** | Each file does ONE thing. Easy to understand. |
| **Heavy comments** | Code explains itself. Learn by reading. |

### What We Deliberately Left Out

- Fancy CLI frameworks (argparse is enough)
- Colorful output (you can add `rich` later)
- Database storage (JSON files work fine)
- Web interface (terminal is plenty)

**Why?** Because constraints force clarity. Build the simplest thing that works.

---

## Project Structure

```
code-analyzer/
├── analyze.py          # Entry point - run this
├── extractor.py        # Finds classes, functions, imports
├── relationships.py    # Detects who calls whom
├── output.py           # Formats and displays results
└── README.md           # You're reading it
```

*More documentation coming as I build the actual code...*
