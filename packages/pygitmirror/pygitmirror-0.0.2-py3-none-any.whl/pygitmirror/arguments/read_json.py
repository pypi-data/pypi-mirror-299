from typing import Any

import json


def read_json(file_path: str) -> Any:
    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    active_lines = []
    for line in lines:
        line = line.strip()

        if not line or line.startswith("//"):
            continue

        active_lines.append(line)

    all_str = "\n".join(active_lines)

    return json.loads(all_str)
