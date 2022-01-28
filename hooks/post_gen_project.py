#!/usr/bin/env python

import sys
import shutil
import pathlib

source_path = pathlib.Path("{{ cookiecutter.protos_dir }}") / "ansys"

if not source_path.is_dir():
    print(f"ERROR: Path '{source_path}' does not exist.")
    sys.exit(1)

dest_path = pathlib.Path("src") / "ansys"
shutil.copytree(source_path, dest_path)
(dest_path / "api" / "{{ cookiecutter.product_name | lower }}" / "v{{ cookiecutter.api_version }}" / "__init__.py").touch()
(dest_path / "api" / "{{ cookiecutter.product_name | lower }}" / "v{{ cookiecutter.api_version }}" / "py.typed").touch()
