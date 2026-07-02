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


def normalize_header(header: str) -> str:
    """Normalize a single header: trim, lowercase, replace spaces with underscores."""
    return header.strip().lower().replace(" ", "_")


def normalize_headers(headers: list) -> list:
    """Normalize all headers."""
    return [normalize_header(h) for h in headers]


def is_empty_row(row: list) -> bool:
    """Check if a row is empty (all fields empty or whitespace only)."""
    return all(not field.strip() for field in row)


def filter_empty_rows(rows: list) -> tuple:
    """Filter out empty rows and return (filtered_rows, removed_count)."""
    filtered = [row for row in rows if not is_empty_row(row)]
    removed = len(rows) - len(filtered)
    return filtered, removed


def deduplicate_rows(rows: list) -> tuple:
    """Remove duplicate rows, keeping first occurrence. Return (deduped_rows, removed_count)."""
    seen = set()
    deduped = []
    removed = 0
    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            deduped.append(row)
        else:
            removed += 1
    return deduped, removed


def fill_missing_values(rows: list, default: str = "unknown") -> tuple:
    """Fill empty string values with default. Return (filled_rows, filled_count)."""
    filled = 0
    result = []
    for row in rows:
        new_row = [cell if cell.strip() else default for cell in row]
        filled += sum(1 for i, cell in enumerate(row) if not cell.strip())
        result.append(new_row)
    return result, filled


def write_csv(filepath: str, headers: list, rows: list):
    """Write headers and rows to CSV file."""
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        return True
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return False


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

    original_headers = headers
    headers = normalize_headers(headers)
    original_count = len(rows)
    rows, removed_empty = filter_empty_rows(rows)
    rows, removed_dup = deduplicate_rows(rows)
    rows, filled_missing = fill_missing_values(rows)

    if not write_csv(args.output, headers, rows):
        return 1

    print(f"Original rows: {original_count}")
    print(f"Headers: {headers}")
    print(f"Rows after cleaning: {len(rows)}")
    print(f"Empty rows removed: {removed_empty}")
    print(f"Duplicate rows removed: {removed_dup}")
    print(f"Missing values filled: {filled_missing}")
    print(f"Output file: {args.output}")
    return 0


if __name__ == "__main__":
    exit(main())