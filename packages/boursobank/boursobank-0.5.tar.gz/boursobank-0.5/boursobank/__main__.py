"""Command-line tool to parse BoursoBank statements."""

import argparse
import logging
from pathlib import Path

from rich import print as rich_print
from rich.panel import Panel

from boursobank import Statement


def main() -> None:
    """Module entry point."""
    args = parse_args()

    logging.getLogger("pypdf._text_extraction._layout_mode._fixed_width_page").setLevel(
        logging.ERROR
    )

    for file in args.files:
        statement = Statement.from_pdf(file)
        if args.debug:
            rich_print(Panel(statement.text))
        statement.pretty_print(args.show_descriptions)
        statement.validate()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-s", "--show-descriptions", action="store_true")
    parser.add_argument("files", nargs="*", type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    main()
