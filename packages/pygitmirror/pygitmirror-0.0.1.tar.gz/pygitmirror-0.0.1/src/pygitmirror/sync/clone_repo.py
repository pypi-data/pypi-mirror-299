import logging
import git

_logger = logging.getLogger(__name__)


def clone_repo(
    sync_path: str,
    source_url: str,
) -> None:
    _logger.info(
        "cloning new repo from %s to %s",
        source_url,
        sync_path,
    )

    git.Repo.clone_from(source_url, sync_path)
