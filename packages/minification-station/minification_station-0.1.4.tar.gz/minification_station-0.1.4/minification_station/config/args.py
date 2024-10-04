import argparse
import sys

from minification_station.config.constants import DEFAULT_LANGUAGE

DEFAULT_OUTPUT_FILE = "output.txt"


def get_parsed_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process files in a directory and combine them into a single output file.",
    )
    parser.add_argument("-d", "--directory", required=True, help="Directory to traverse")
    parser.add_argument(
        "--program_lang",
        type=str,
        default=DEFAULT_LANGUAGE,
        help="Programming language (default: python)",
    )

    # parser.add_argument("-o", "--output", required=True, default=DEFAULT_OUTPUT_FILE, help="Output file path")

    return parser.parse_args()
