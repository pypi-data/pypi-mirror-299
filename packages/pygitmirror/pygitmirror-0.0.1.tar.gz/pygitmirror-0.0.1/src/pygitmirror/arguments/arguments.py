from argparse import Namespace
from typing import Tuple, Dict
import os

from .check_repos import check_repos
from .check_url import check_url
from .read_json import read_json


class Arguments:
    def __init__(self, args: Namespace) -> None:
        self.__log = str(args.log)

        json_file = str(args.json)

        json_dict = {}
        if os.path.isfile(json_file):
            json_dict = read_json(json_file)

        sync_path = json_dict.get("sync_path", str(args.sync_path))
        source_url = json_dict.get("source_url", str(args.source_url))
        destination_url = json_dict.get("destination_url", str(args.destination_url))
        repos = json_dict.get(
            "repos", {str(args.org): list(args.repo) if args.repo else []}
        )

        check_url("source", source_url)
        check_url("destination", destination_url)
        check_repos(repos)

        self.__sync_path = sync_path
        self.__source_url = source_url
        self.__destination_url = destination_url
        self.__repos = repos

    @property
    def log_level(self) -> str:
        return self.__log

    @property
    def sync_path(self) -> str:
        return self.__sync_path

    @property
    def source_url(self) -> str:
        return self.__source_url

    @property
    def destination_url(self) -> str:
        return self.__destination_url

    @property
    def repos(self) -> Dict[str, Tuple[str, ...]]:
        return self.__repos

    def get_arguments_summary(self) -> str:
        s_str = Arguments.__name__
        s_str += "\n=======================\n"
        s_str += f"log_level='{self.log_level}'\n"
        s_str += f"sync_path='{self.sync_path}'\n"
        s_str += f"source_url='{self.source_url}'\n"
        s_str += f"destination_url='{self.destination_url}'\n"
        s_str += f"repos='{self.repos}'\n"

        return s_str
