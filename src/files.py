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
