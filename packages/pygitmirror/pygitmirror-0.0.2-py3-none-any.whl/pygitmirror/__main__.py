import logging
import os
import sys
from typing import Optional, Tuple
from pprint import pformat

from .arguments import process_arguments
from .sync import sync_repo


def main(args: Optional[Tuple[str, ...]] = None) -> int:
    p_args = process_arguments(args=args)

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    logger.info(
        "System paths:\n%s",
        pformat(
            os.environ["PATH"].split(":"),
            indent=2,
        ),
    )
    logger.info(
        "Python paths:\n%s",
        pformat(
            sys.path,
            indent=2,
        ),
    )
    logger.info(p_args.get_arguments_summary())

    logger.info("using sync path %s", p_args.sync_path)

    for org, repos in p_args.repos.items():
        for repo in repos:
            sync_repo(
                sync_path=p_args.sync_path,
                source_url=p_args.source_url,
                destination_url=p_args.destination_url,
                org=org,
                repo=repo,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
