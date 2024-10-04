import logging
import git

from .constants import DESTINATION_NAME

_logger = logging.getLogger(__name__)


def add_destination_remote(
    sync_path: str,
    destination_url: str,
) -> None:

    repo = git.Repo(sync_path)

    destination = None
    for remote in repo.remotes:
        if remote.name == DESTINATION_NAME:
            destination = remote
            break

    if destination is not None:
        _logger.info("%s remote is already defined", DESTINATION_NAME)
        return

    _logger.info("adding remote %s", DESTINATION_NAME)
    repo.create_remote(DESTINATION_NAME, destination_url)
