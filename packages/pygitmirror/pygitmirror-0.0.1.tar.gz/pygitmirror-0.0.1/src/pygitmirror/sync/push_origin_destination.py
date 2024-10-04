import logging
import subprocess

import git

from .constants import DESTINATION_NAME, ORIGIN_NAME
from .get_reference_by_name import get_reference_by_name

_logger = logging.getLogger(__name__)


def push_origin_destination(
    sync_path: str,
) -> None:

    repo = git.Repo(sync_path)

    origin = get_reference_by_name(repo, ORIGIN_NAME)

    if origin is None:
        raise RuntimeError(f"{ORIGIN_NAME} remote does not exist")

    destination = get_reference_by_name(repo, DESTINATION_NAME)

    if destination is None:
        raise RuntimeError(f"{DESTINATION_NAME} remote does not exist")

    for branch in origin.refs:
        if branch.remote_head == "HEAD":
            continue

        _logger.info("%s", branch.remote_head)

        args = [
            "git",
            "checkout",
            branch.remote_head,
        ]
        subprocess.check_call(
            args,
            cwd=sync_path,
        )

    # origin.pull(f"{branch.remote_head}:{branch.remote_head}")

    # destination.push(f"{branch.remote_head}:{branch.remote_head}")

    args = [
        "git",
        "push",
        DESTINATION_NAME,
        "--all",
    ]
    _logger.info(" ".join(args))
    subprocess.check_call(
        args,
        cwd=sync_path,
    )
