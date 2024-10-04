from typing import Optional

import git


def get_reference_by_name(
    repo: git.Repo,
    name: str,
) -> Optional[git.Reference]:

    for remote in repo.remotes:
        if remote.name == name:
            return remote

    return None
