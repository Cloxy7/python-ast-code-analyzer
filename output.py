"""
Output Module
=============

This module handles displaying results and saving them to files.
It's the "presentation layer" — takes data and makes it readable.

DESIGN PHILOSOPHY:
------------------
- Terminal output should be scannable (not walls of text)
- JSON output should be complete (for further processing)
- Mermaid output enables visualization (bonus feature)

WHY SEPARATE OUTPUT FROM LOGIC:
-------------------------------
If we want to change how results look (add colors, change format),
we only touch this file. The extraction logic stays untouched.

This is "separation of concerns" — a key software principle.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


def print_summary(entities: Dict[str, List[Dict]], relationships: Dict[str, Any]):
    """
    Print a human-readable summary to the terminal.

    We aim for:
    - Quick scan (what did we find?)
    - Highlights (what's interesting?)
    - Actionable insights

    Args:
        entities: Extracted entities by file
        relationships: Call relationships and imports
    """
    print("\n" + "=" * 60)
    print("  CODE ANALYSIS SUMMARY")
    print("=" * 60)

    # --- Overview ---
    summary = relationships.get("summary", {})

    print(f"\n📁 Files analyzed: {len(entities)}")
    print(f"📦 Classes found: {summary.get('total_classes', 0)}")
    print(f"🔧 Functions found: {summary.get('total_functions', 0)}")
    print(f"🔗 Call relationships: {summary.get('total_calls', 0)}")

    # --- Most Called Functions ---
    most_called = summary.get("most_called", [])
    if most_called:
        print("\n📊 Most Called Functions (potential core utilities):")
        for name, count in most_called[:5]:
            print(f"   {count:3}x  {name}")

    # --- Functions That Call Most Others ---
    most_calling = summary.get("most_calling", [])
    if most_calling:
        print("\n🎯 Functions That Call Most Others (orchestrators):")
        for name, count in most_calling[:5]:
            print(f"   {count:3} calls  {name}")

    # --- Files Overview ---
    print("\n📄 Files:")
    for file_path, file_entities in sorted(entities.items()):
        class_count = sum(1 for e in file_entities if e["type"] == "class")
        func_count = sum(1 for e in file_entities if e["type"] == "function")
        print(f"   {file_path}")
        print(f"      Classes: {class_count}, Functions: {func_count}")

    # --- Key Entities ---
    print("\n🏛️  Key Entities:")
    for file_path, file_entities in sorted(entities.items()):
        for entity in file_entities:
            if entity["type"] == "class":
                bases = ", ".join(entity.get("bases", [])) or "none"
                methods = entity.get("method_count", 0)
                print(f"   class {entity['name']} (inherits: {bases}, methods: {methods})")
                print(f"         └─ {file_path}:{entity['line']}")

    print("\n" + "=" * 60)


def save_results(
    entities: Dict[str, List[Dict]],
    relationships: Dict[str, Any],
    output_dir: Path
):
    """
    Save analysis results to files.

    Creates:
    - entities.json: All extracted entities
    - relationships.json: Call graph and imports
    - summary.md: Human-readable report
    - diagram.mermaid: Visual call graph

    Args:
        entities: Extracted entities
        relationships: Call relationships
        output_dir: Directory to save files
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save entities JSON
    entities_path = output_dir / "entities.json"
    with open(entities_path, "w", encoding="utf-8") as f:
        json.dump(entities, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {entities_path}")

    # Save relationships JSON
    relationships_path = output_dir / "relationships.json"
    with open(relationships_path, "w", encoding="utf-8") as f:
        json.dump(relationships, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved: {relationships_path}")

    # Generate and save markdown summary
    summary_path = output_dir / "summary.md"
    summary_md = generate_markdown_summary(entities, relationships)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"✓ Saved: {summary_path}")

    # Generate and save mermaid diagram
    mermaid_path = output_dir / "diagram.mermaid"
    mermaid_content = generate_mermaid_diagram(relationships)
    with open(mermaid_path, "w", encoding="utf-8") as f:
        f.write(mermaid_content)
    print(f"✓ Saved: {mermaid_path}")


def generate_markdown_summary(
    entities: Dict[str, List[Dict]],
    relationships: Dict[str, Any]
) -> str:
    """
    Generate a Markdown report of the analysis.

    This creates a document that could be committed to a repo
    or shared with team members.

    Args:
        entities: Extracted entities
        relationships: Call relationships

    Returns:
        Markdown string
    """
    summary = relationships.get("summary", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Code Analysis Report",
        "",
        f"> Generated: {timestamp}",
        "",
        "---",
        "",
        "## Overview",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Files analyzed | {len(entities)} |",
        f"| Classes | {summary.get('total_classes', 0)} |",
        f"| Functions | {summary.get('total_functions', 0)} |",
        f"| Call relationships | {summary.get('total_calls', 0)} |",
        "",
        "---",
        "",
        "## Classes Found",
        "",
    ]

    # List all classes
    for file_path, file_entities in sorted(entities.items()):
        for entity in file_entities:
            if entity["type"] == "class":
                bases = ", ".join(entity.get("bases", [])) or "none"
                lines.append(f"### `{entity['name']}`")
                lines.append(f"")
                lines.append(f"- **File:** `{file_path}`")
                lines.append(f"- **Line:** {entity['line']}")
                lines.append(f"- **Inherits:** {bases}")
                lines.append(f"- **Methods:** {entity.get('method_count', 0)}")
                if entity.get("decorators"):
                    lines.append(f"- **Decorators:** {', '.join(entity['decorators'])}")
                if entity.get("docstring"):
                    lines.append(f"- **Description:** {entity['docstring'][:100]}...")
                lines.append("")

    # Most called functions
    most_called = summary.get("most_called", [])
    if most_called:
        lines.extend([
            "---",
            "",
            "## Most Called Functions",
            "",
            "These functions are called frequently — they're likely core utilities.",
            "",
            "| Function | Call Count |",
            "|----------|------------|",
        ])
        for name, count in most_called[:10]:
            lines.append(f"| `{name}` | {count} |")
        lines.append("")

    # Orchestrator functions
    most_calling = summary.get("most_calling", [])
    if most_calling:
        lines.extend([
            "---",
            "",
            "## Orchestrator Functions",
            "",
            "These functions call many others — they're likely coordinators.",
            "",
            "| Function | Calls Made |",
            "|----------|------------|",
        ])
        for name, count in most_calling[:10]:
            lines.append(f"| `{name}` | {count} |")
        lines.append("")

    # Imports summary
    imports = relationships.get("imports", [])
    if imports:
        # Group imports by module
        modules = {}
        for imp in imports:
            module = imp.get("module", "unknown")
            if module not in modules:
                modules[module] = 0
            modules[module] += 1

        lines.extend([
            "---",
            "",
            "## External Dependencies",
            "",
            "Modules imported across the codebase:",
            "",
        ])
        for module, count in sorted(modules.items(), key=lambda x: x[1], reverse=True)[:15]:
            lines.append(f"- `{module}` ({count} imports)")
        lines.append("")

    lines.extend([
        "---",
        "",
        "*Report generated by Code Analyzer*",
    ])

    return "\n".join(lines)


def generate_mermaid_diagram(relationships: Dict[str, Any]) -> str:
    """
    Generate a Mermaid diagram showing call relationships.

    Mermaid is a text-based diagramming language that renders
    in GitHub, GitLab, Obsidian, and many other tools.

    Format:
        graph TD
            A[Function A] --> B[Function B]

    Args:
        relationships: Call relationships data

    Returns:
        Mermaid diagram string
    """
    calls = relationships.get("calls", [])

    # Limit to avoid huge diagrams
    # Show only the most significant relationships
    MAX_EDGES = 50

    lines = [
        "graph TD",
        "    %% Call Graph - Who calls whom",
        "    %% Arrows point from caller to callee",
        "",
    ]

    # Count edges to prioritize important ones
    edge_counts: Dict[tuple, int] = {}
    for call in calls:
        # Skip self-calls and <module> calls
        if call["caller"] == call["callee"]:
            continue
        if call["caller"] == "<module>":
            continue

        edge = (call["caller"], call["callee"])
        edge_counts[edge] = edge_counts.get(edge, 0) + 1

    # Sort by frequency and take top N
    sorted_edges = sorted(edge_counts.items(), key=lambda x: x[1], reverse=True)[:MAX_EDGES]

    # Track nodes we've seen (for styling)
    seen_nodes = set()

    for (caller, callee), count in sorted_edges:
        # Sanitize names for Mermaid (replace dots with underscores)
        caller_id = caller.replace(".", "_").replace("<", "").replace(">", "")
        callee_id = callee.replace(".", "_").replace("<", "").replace(">", "")

        # Add edge
        if count > 1:
            lines.append(f"    {caller_id}[{caller}] -->|{count}x| {callee_id}[{callee}]")
        else:
            lines.append(f"    {caller_id}[{caller}] --> {callee_id}[{callee}]")

        seen_nodes.add(caller_id)
        seen_nodes.add(callee_id)

    if not sorted_edges:
        lines.append("    NoRelationships[No call relationships found]")

    return "\n".join(lines)
