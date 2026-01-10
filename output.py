"""
Output Module - First version
=============================

Start with just terminal output.
Will add JSON and Mermaid export next.
"""

from typing import Dict, List, Any


def print_summary(entities: Dict[str, List[Dict]], relationships: Dict[str, Any]):
    """
    Print a human-readable summary to the terminal.
    """
    print("\n" + "=" * 50)
    print("  CODE ANALYSIS SUMMARY")
    print("=" * 50)

    # Count totals
    total_classes = 0
    total_functions = 0

    for file_entities in entities.values():
        for entity in file_entities:
            if entity["type"] == "class":
                total_classes += 1
            elif entity["type"] == "function":
                total_functions += 1

    print(f"\nFiles analyzed: {len(entities)}")
    print(f"Classes found: {total_classes}")
    print(f"Functions found: {total_functions}")

    # Show files
    print("\nFiles:")
    for file_path in sorted(entities.keys()):
        print(f"  {file_path}")

    print("\n" + "=" * 50)
