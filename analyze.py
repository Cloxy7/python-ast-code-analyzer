#!/usr/bin/env python3
"""
Code Analyzer - Main Entry Point
================================

This is the CLI interface for the code analyzer tool.
Run this file to analyze Python codebases.

Usage:
    python analyze.py /path/to/code
    python analyze.py /path/to/code --output ./results

What it does:
1. Finds all Python files in the given directory
2. Extracts entities (classes, functions) from each file
3. Detects relationships (who calls whom)
4. Outputs results to terminal and JSON files

WHY THIS DESIGN:
- argparse is simple and built-in (no dependencies)
- Main function is small — it orchestrates, doesn't do work
- Each step is a separate module (separation of concerns)
"""

import argparse
import sys
from pathlib import Path

# Our modules - each does one thing
from extractor import extract_entities_from_directory
from relationships import find_relationships
from output import print_summary, save_results


def main():
    """
    Main entry point. Parses arguments and runs analysis.

    The flow is:
    1. Parse command-line arguments
    2. Validate the input path exists
    3. Extract entities from all Python files
    4. Find relationships between entities
    5. Output results (terminal + files)
    """

    # --- Step 1: Parse arguments ---
    # argparse handles --help automatically, which is nice
    parser = argparse.ArgumentParser(
        description="Analyze Python code to extract entities and relationships",
        epilog="Example: python analyze.py ~/code/erpnext/erpnext/accounts/"
    )

    parser.add_argument(
        "path",
        help="Path to Python file or directory to analyze"
    )

    parser.add_argument(
        "--output", "-o",
        default="./output",
        help="Directory to save output files (default: ./output)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed progress"
    )

    args = parser.parse_args()

    # --- Step 2: Validate input path ---
    input_path = Path(args.path)

    if not input_path.exists():
        print(f"Error: Path does not exist: {input_path}")
        sys.exit(1)

    # --- Step 3: Extract entities ---
    # This is where the real work starts
    if args.verbose:
        print(f"Analyzing: {input_path}")

    entities = extract_entities_from_directory(input_path, verbose=args.verbose)

    if not entities:
        print("No Python files found or no entities extracted.")
        sys.exit(0)

    # --- Step 4: Find relationships ---
    if args.verbose:
        print("Finding relationships...")

    relationships = find_relationships(input_path, entities)

    # --- Step 5: Output results ---
    output_dir = Path(args.output)

    # Print to terminal
    print_summary(entities, relationships)

    # Save to files
    save_results(entities, relationships, output_dir)

    print(f"\nResults saved to: {output_dir}/")


if __name__ == "__main__":
    main()
