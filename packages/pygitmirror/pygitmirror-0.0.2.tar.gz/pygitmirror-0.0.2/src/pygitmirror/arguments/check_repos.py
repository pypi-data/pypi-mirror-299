from typing import Dict, List


def check_repos(repos: Dict[str, List[str]]) -> None:

    if not repos:
        raise RuntimeError("repos are null")

    if not isinstance(repos, dict):
        raise RuntimeError(f"repos object is not a dict {repos.__class__.__name__}")

    for key, value in repos.items():
        if not key:
            raise RuntimeError("key is null")

        if not isinstance(key, str):
            raise RuntimeError(f"key {key} is not a string: {key.__class__.__name__}")

        if not value:
            raise RuntimeError("value is null")

        if not isinstance(value, list):
            raise RuntimeError(
                f"value {value} is not a list: {value.__class__.__name__}"
            )

        for v in value:
            if not v:
                raise RuntimeError("value element is null")

            if not isinstance(v, str):
                raise RuntimeError(
                    f"value element {v} is not a string: {v.__class__.__name__}"
                )
