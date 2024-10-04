import os
from argparse import ArgumentParser
from typing import Optional, Tuple

from .arguments import Arguments


def process_arguments(args: Optional[Tuple[str, ...]] = None) -> Arguments:
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        default="DEBUG",
        choices=("DEBUG", "INFO", "WARNING", "CRITICAL"),
        help="log level (default: %(default)s)",
    )

    parser.add_argument(
        "--json",
        type=str,
        help="path to a JSON input file",
    )

    parser.add_argument(
        "--sync_path",
        type=str,
        default=os.getcwd(),
        help="path to use for syncing",
    )

    parser.add_argument(
        "--source_url",
        type=str,
        help="source URL",
    )

    parser.add_argument(
        "--destination_url",
        type=str,
        help="destination URL",
    )

    parser.add_argument(
        "--org",
        type=str,
        help="organization name",
    )

    parser.add_argument(
        "--repo",
        type=str,
        nargs="+",
        help="one or more repo names",
    )

    return Arguments(args=parser.parse_args(args=args))
