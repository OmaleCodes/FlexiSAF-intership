"""Command-line entry point.

Example:
    python main.py data/netflix_titles.csv --output-dir output
"""

import argparse
import logging
from pathlib import Path

from src.processor import format_report, process_file


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check a Netflix titles CSV file. Good rows go to "
        "clean_titles.csv, bad rows (with the reason) go to invalid_titles.csv."
    )
    parser.add_argument("input", type=Path, help="path to the CSV file")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("output"), help="folder for the results"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    try:
        summary = process_file(args.input, args.output_dir)
    except FileNotFoundError:
        print(f"Error: file not found: {args.input}")
        return

    report = format_report(summary, args.input)
    print(report)
    (args.output_dir / "report.txt").write_text(report + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()