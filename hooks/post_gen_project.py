#!/usr/bin/env python
"""Hook to copy the .proto files into the project, and create __init__.py and py.typed files."""
import os
import pathlib
import shutil
import sys

PROTOS_DIR = "{{ cookiecutter.protos_dir }}"
DEST_PATH = (
    pathlib.Path("ansys")
    / "api"
    / "{{ cookiecutter.product_name | lower }}"
    / "v{{ cookiecutter.api_version }}"
)


if PROTOS_DIR:
    source_path = pathlib.Path(PROTOS_DIR)

    if not source_path.is_dir():
        print(f"ERROR: Path '{source_path}' does not exist.")
        sys.exit(1)

    shutil.copytree(source_path, DEST_PATH)
else:
    os.makedirs(DEST_PATH)
    print(
        "\nNOTE: No protos directory specified. Make sure to manually "
        f"copy the .proto files to '{DEST_PATH.absolute()}'."
    )

(DEST_PATH / "__init__.py").touch()
(DEST_PATH / "py.typed").touch()
