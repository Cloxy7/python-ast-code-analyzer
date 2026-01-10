#!/usr/bin/env python3
"""
Code Analyzer - Main Entry Point
================================

Putting it all together. This script:
1. Takes a directory path
2. Extracts entities
3. Finds relationships
4. Outputs results
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python code to extract entities and relationships"
    )
    parser.add_argument("path", help="Path to analyze")
    parser.add_argument("--output", "-o", default="./output", help="Output directory")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    input_path = Path(args.path)

    if not input_path.exists():
        print(f"Error: Path does not exist: {input_path}")
        sys.exit(1)

    print(f"Analyzing: {input_path}")
    print("TODO: Wire up extractor and relationships modules")


if __name__ == "__main__":
    main()
