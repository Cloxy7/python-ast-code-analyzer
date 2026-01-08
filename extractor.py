"""
Entity Extractor - First attempt
================================

Starting simple: just find all Python files in a directory.
Will add actual parsing next.
"""

from pathlib import Path
from typing import List


def find_python_files(path: Path) -> List[Path]:
    """
    Find all Python files in a directory.

    Args:
        path: Directory to search

    Returns:
        List of paths to .py files
    """
    if path.is_file():
        return [path] if path.suffix == ".py" else []

    # rglob finds files recursively
    return list(path.rglob("*.py"))


# Quick test
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        files = find_python_files(Path(sys.argv[1]))
        print(f"Found {len(files)} Python files:")
        for f in files[:10]:
            print(f"  {f}")
