import logging
import os

from .fetch_repo import fetch_repo
from .clone_repo import clone_repo
from .add_destination_remote import add_destination_remote
from .push_origin_destination import push_origin_destination

_logger = logging.getLogger(__name__)


def sync_repo(
    sync_path: str,
    source_url: str,
    destination_url: str,
    org: str,
    repo: str,
) -> int:
    _logger.info("syncing %s/%s", org, repo)

    repo_sync_path = os.path.join(sync_path, org, repo)
    repo_source_url = f"{source_url}/{org}/{repo}"
    repo_destination_url = f"{destination_url}/{org}/{repo}"

    _logger.info("repo_sync_path: %s", repo_sync_path)
    _logger.info("repo_source_url: %s", repo_source_url)
    _logger.info("repo_destination_url: %s", repo_destination_url)

    if os.path.isdir(repo_sync_path):
        fetch_repo(repo_sync_path)
    else:
        clone_repo(repo_sync_path, repo_source_url)

    add_destination_remote(repo_sync_path, repo_destination_url)

    push_origin_destination(repo_sync_path)

    return 0
