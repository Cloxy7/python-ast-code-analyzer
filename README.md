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

**Example:**
```bash
python analyze.py ~/code/erpnext/erpnext/accounts/doctype/sales_invoice/

# Output:
# - List of classes and functions found
# - Import dependencies
# - Call relationships (what calls what)
# - Summary insights
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
| **No classes (mostly)** | Functions are simpler. Classes aren't always needed. |

### What We Deliberately Left Out

- Fancy CLI frameworks (argparse is enough)
- Colorful output (you can add `rich` later)
- Database storage (JSON files work fine)
- Web interface (terminal is plenty)
- Multi-language support (Python only, keep it focused)

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

**Total: ~400 lines of code.** You can read all of it in 30 minutes.

---

## How It Works

### Step 1: Parse Python Files

Python's `ast` (Abstract Syntax Tree) module lets us understand code structure:

```python
import ast

code = """
def calculate_tax(amount):
    return amount * 0.18
"""

tree = ast.parse(code)
# tree now contains a structured representation of the code
```

### Step 2: Walk the Tree

We visit each node in the tree to find what we care about:

```python
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"Found function: {node.name}")
    elif isinstance(node, ast.ClassDef):
        print(f"Found class: {node.name}")
```

### Step 3: Extract Relationships

When we see a function call inside another function, that's a relationship:

```python
def validate_invoice(doc):
    calculate_tax(doc.total)  # <-- validate_invoice CALLS calculate_tax
```

### Step 4: Output Results

We generate:
- `entities.json` — All classes and functions found
- `relationships.json` — Who calls whom
- Terminal summary — Quick insights

---

## Running the Tool

### Basic Usage

```bash
# Analyze a directory
python analyze.py /path/to/python/code

# Analyze with output files
python analyze.py /path/to/code --output ./results

# Analyze specific file
python analyze.py /path/to/file.py
```

### Example with ERPNext

```bash
# Clone ERPNext (if you haven't)
git clone https://github.com/frappe/erpnext.git ~/code/erpnext

# Analyze the Sales Invoice module
python analyze.py ~/code/erpnext/erpnext/accounts/doctype/sales_invoice/

# Or analyze the entire accounts module
python analyze.py ~/code/erpnext/erpnext/accounts/ --output ./erpnext-analysis
```

### Real Output Example

Here's what the tool actually produces when run against ERPNext's Sales Invoice module:

```
============================================================
  CODE ANALYSIS SUMMARY
============================================================

📁 Files analyzed: 3
📦 Classes found: 3
🔧 Functions found: 269
🔗 Call relationships: 2604

📊 Most Called Functions (potential core utilities):
   277x  self.assertEqual
    95x  create_sales_invoice
    94x  _
    83x  flt
    66x  si.get

🎯 Functions That Call Most Others (orchestrators):
    50 calls  SalesInvoice.validate
    37 calls  SalesInvoice.on_submit
    34 calls  SalesInvoice.set_pos_fields
    30 calls  SalesInvoice.on_cancel

🏛️  Key Entities:
   class SalesInvoice (inherits: SellingController, methods: 96)
         └─ sales_invoice/sales_invoice.py:57
```

**What this tells us:**
- `SalesInvoice.validate` calls 50 other functions — it's the main orchestrator
- `flt()` is called 83 times — it's a core utility (float conversion)
- The class has 96 methods — significant complexity
- Most calls are validation and submission logic

**Generated files:**
- `entities.json` — All classes and functions with metadata
- `relationships.json` — Complete call graph
- `summary.md` — Human-readable report
- `diagram.mermaid` — Visual call graph

See the `example-output/` folder for full output.

---

## Understanding the Code

### extractor.py — The Heart of Analysis

This module answers: **"What's in this code?"**

Key concepts:
- **AST parsing**: Converting source code to a tree structure
- **Node visiting**: Walking through the tree systematically
- **Entity extraction**: Pulling out classes, functions, imports

Read it line by line. Every function has comments explaining what it does.

### relationships.py — Finding Connections

This module answers: **"What calls what?"**

Key concepts:
- **Call detection**: Finding `function()` patterns in AST
- **Scope tracking**: Knowing which function we're inside
- **Relationship mapping**: Building caller → callee connections

### output.py — Making It Readable

This module answers: **"How do we show results?"**

Key concepts:
- **JSON serialization**: Saving structured data
- **Terminal formatting**: Making output human-readable
- **Summary generation**: Condensing findings into insights

---

## What You Should Build

Your version doesn't need to match this. Consider:

| Approach | What It Demonstrates |
|----------|---------------------|
| **Focus on one thing** | Extract ONLY functions. Do it really well. |
| **Different output** | Generate Mermaid diagrams instead of JSON. |
| **Different language** | Analyze Java code (for OpenElis/Bahmni). |
| **Add AI** | Use an LLM to summarize what each function does. |
| **Interactive** | Build a REPL that answers questions about the code. |

**The best submissions aren't copies. They're variations that show YOU understood the problem.**

---

## Learning Checkpoints

After studying this code, you should be able to answer:

### Conceptual
- [ ] What is an AST? Why use it instead of regex?
- [ ] What's the difference between `ast.parse()` and `ast.walk()`?
- [ ] Why do we track "scope" when finding relationships?

### Practical
- [ ] How would you add support for detecting decorators?
- [ ] How would you find all database queries in the code?
- [ ] How would you generate a Mermaid diagram from relationships?

### Reflective
- [ ] What did this tool miss? What can't it detect?
- [ ] What would you do differently?
- [ ] Where would AI (LLMs) help most?

---

## Common Questions

### "Can I use AI to help build my tool?"

**Yes, absolutely.** But:
- You must understand what the AI generated
- You must be able to explain every line
- You must be able to modify it when asked
- Your Loom video should show YOUR understanding, not the AI's

### "What if my tool is simpler than this?"

**That's fine.** A tool that extracts just function names — but you understand completely — is better than a complex tool you can't explain.

### "What if I can't finish in 4 days?"

**Ship what you have.** A partial solution with clear documentation of what works, what doesn't, and what you learned is valuable. We're evaluating your learning process, not just the output.

---

## Extending This Tool

Ideas for making it better:

1. **Add Mermaid output** — Generate `graph TD` diagrams
2. **Add statistics** — Lines of code, complexity metrics
3. **Add search** — "Find all functions that mention 'tax'"
4. **Add AI summaries** — Use Claude/GPT to explain functions
5. **Add caching** — Don't re-parse unchanged files
6. **Add tests** — Verify extraction is correct

---

## Resources

### Python AST
- [Official ast module docs](https://docs.python.org/3/library/ast.html)
- [Green Tree Snakes (AST tutorial)](https://greentreesnakes.readthedocs.io/)

### Code Analysis
- [tree-sitter](https://tree-sitter.github.io/) — Multi-language parsing
- [Jedi](https://jedi.readthedocs.io/) — Python static analysis

### The Codebases We're Analyzing
- [ERPNext](https://github.com/frappe/erpnext) — Python/Frappe
- [OpenElis](https://github.com/openelisglobal/openelisglobal-core) — Java
- [Bahmni](https://github.com/Bahmni/bahmni-core) — Java

---

## Final Thought

> "The goal isn't to build the most impressive tool.
> The goal is to learn deeply and share what you learned."

Your code, your README, your Loom video — they should all tell the story of your learning journey.

Good luck!
