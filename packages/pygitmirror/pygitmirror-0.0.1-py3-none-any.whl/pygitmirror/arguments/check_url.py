def check_url(name: str, url: str) -> None:

    if not url:
        raise RuntimeError(f"{name} URL is null")
