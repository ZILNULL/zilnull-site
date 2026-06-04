import sys
from pathlib import Path

from src.files import copy_folder


def main():
    copy_folder(Path("website/static/"), Path("dist/static/"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
