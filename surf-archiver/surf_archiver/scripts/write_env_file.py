import os
from pathlib import Path


def main() -> None:
    """Write environment variables to file.

    This is intended for development purposes only.
    """
    venv_path = os.getenv("VENV_PATH", "/app/.venv")
    entries: list[str] = [f"PATH={venv_path}/bin:$PATH\n"]
    for k, v in os.environ.items():
        if k.startswith("AWS_") or k.startswith("SURF_"):
            entries.append(f"{k}={v}\n")

    user = os.getenv("USER", "guest")
    path_to_environment = Path("/home", user, ".ssh", "environment")
    path_to_environment.parent.mkdir(exist_ok=True)
    with path_to_environment.open("w") as file:
        file.writelines(entries)


if __name__ == "__main__":
    main()
