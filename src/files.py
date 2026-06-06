import shutil
from pathlib import Path


def copy_folder(src: Path, dst: Path):
    if not src.is_dir() or src.is_file():
        raise FileNotFoundError("The source directory does not exist or is a file.")
    if dst.exists() and dst.is_file():
        raise FileExistsError("The source directory provided is already a file.")

    if dst.is_dir():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)


def read_file(file: Path) -> str:
    if not file.exists():
        raise FileNotFoundError("The provided file does not exist.")
    if file.exists() and file.is_dir():
        raise FileExistsError("Target path points to a directory.")

    with open(file, "r") as f:
        content = f.read()

    return content


def write_file(file: Path, content: str | None = None):
    if file.exists() and file.is_dir():
        raise FileExistsError("Target path points to a directory.")

    try:
        content = content if content is not None else ""
        with open(file, "w") as f:
            f.write(content)
    except Exception as e:
        raise e
