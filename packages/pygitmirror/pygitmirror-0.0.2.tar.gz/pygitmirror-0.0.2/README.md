# Git Mirror

[![PyPi Badge](https://img.shields.io/pypi/v/pygitmirror)](https://pypi.org/project/pygitmirror/)
![Publish](https://github.com/pygitmirror/pygitmirror/workflows/Publish/badge.svg)
![Test](https://github.com/pygitmirror/pygitmirror/workflows/Test/badge.svg)
[![Downloads](https://static.pepy.tech/personalized-badge/pygitmirror?period=week&units=international_system&left_color=black&right_color=orange&left_text=Last%20Week)](https://pepy.tech/project/pygitmirror)
[![Downloads](https://static.pepy.tech/personalized-badge/pygitmirror?period=month&units=international_system&left_color=black&right_color=orange&left_text=Month)](https://pepy.tech/project/pygitmirror)
[![Downloads](https://static.pepy.tech/personalized-badge/pygitmirror?period=total&units=international_system&left_color=black&right_color=orange&left_text=Total)](https://pepy.tech/project/pygitmirror)

`git-mirror` is part of the `pygitmirror` Python package. `git-mirror` is an executable to clone git repos from one git server to another.

## Installation

To install `pygitmirror` into your Python environment:

    pip install -U pygitmirror

The package exposes a single executable `git-mirror` which is used to systematically mirror your git repos from one `git` server to another.

## Usage

After installing `pygitmirror`, you can call the `git-mirror` executable to clone/mirror your `git` repository between two git servers:

    git-mirror --source_url <source git server URL> --destination_url <destination git server URL> --org <organization or project name> --repo <repo name>

`git-mirror` will use the current directory to check out your source repository and pushes **all branches** in it to its new location at the destination. Note, the destination repository needs to **_already exist_** at the destination server, albeit being empty!

To use a custom sync/temporary path:

    git-mirror --sync_path <custom sync path> ..

To mirror multiple repositories at once, you should use the `JSON` file option:

```json
{
  "sync_path": "<local path for sync>",
  "source_url": "ssh://<source-git-server>:<source port> or https://<source-server>",
  "destination_url": "ssh://<destination-git-server> or https://<destination-server>",
  "repos": {
    // comments are allowed at the beginning
    "organization-1": [
      // comments are allowed at the beginning
      "repo-1",
      "repo-2",
      "..."
    ],
    "organization-2": ["repo-3", "repo-4", "..."]
  }
}
```

Note: `JSON` file entries supersede the other command line arguments.

To get a list of all available parameters:

    git-mirror -h

## Development

To clone the library for development:

    git clone https://github.com/pygitmirror/pygitmirror.git

or

    git clone git@github.com:pygitmirror/pygitmirror.git

### Build The Virtual Environment

The current earliest Python version supported is `3.9`. You need to be able to create a virtual environment at this version to make sure any changes you make is compatible.

If you are using `conda`:

    conda create --prefix=.venv python=3.9 --yes

If you are using `venv`, make sure you have the right base package:

    >> python --version
    Python 3.9.x

Once you verify your base Python, you can then create a virtual environment using:

    virtualenv -p py3.9 .venv

### Setup

Once you have created your virtual environment and made sure it is active in your current command line:

    python3 -m pip install --upgrade pip
    pip install -e .[dev]

This should all the dependencies you need for developing into the library and also allow you to run the unit tests:

    pytest
