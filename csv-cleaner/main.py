#!/usr/bin/env python3
"""CSV data cleaning and standardization command-line tool."""

import argparse
import csv
from pathlib import Path


def validate_input(input_path: str) -> bool:
    """Validate input file exists."""
    if not Path(input_path).exists():
        print(f"Error: Input file '{input_path}' does not exist.")
        return False
    return True


def read_csv(filepath: str):
    """Read CSV file and return headers and rows."""
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        return headers, rows
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return None, None
    except StopIteration:
        print("Error: Empty CSV file.")
        return [], []
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, None


def main():
    parser = argparse.ArgumentParser(
        description="CSV data cleaning and standardization tool"
    )
    parser.add_argument(
        "-input", required=True, help="Path to input CSV file"
    )
    parser.add_argument(
        "-output", required=True, help="Path to output cleaned CSV file"
    )
    args = parser.parse_args()

    if not validate_input(args.input):
        return 1

    headers, rows = read_csv(args.input)
    if headers is None:
        return 1

    print(f"Headers: {headers}")
    print(f"Rows read: {len(rows)}")
    return 0


if __name__ == "__main__":
    exit(main())