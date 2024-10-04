import logging
import git

from .constants import ORIGIN_NAME

_logger = logging.getLogger(__name__)


def fetch_repo(
    sync_path: str,
) -> None:
    _logger.info("fetching existing repo %s", sync_path)

    repo = git.Repo(sync_path)

    origin = None
    for remote in repo.remotes:
        if remote.name == ORIGIN_NAME:
            origin = remote
            break

    if origin is None:
        raise RuntimeError(f"could not find remote {ORIGIN_NAME}")

    origin.fetch()
