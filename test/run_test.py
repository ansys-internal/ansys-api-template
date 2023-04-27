"""Test the cookiecutter ansys-api-template."""
import argparse
import glob
import os
import shutil
import subprocess
import sys
from subprocess import PIPE
from subprocess import Popen
from subprocess import STDOUT

HERE = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="run tests")
    parser.add_argument(
        "--skip-venv-check", help="Do not check if within a virtualenv", action="store_true"
    )
    args = parser.parse_args()

    # check if within a virtual environment
    if not args.skip_venv_check:
        if not hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix
        ):
            raise RuntimeError(
                "Must run the test script from within a virtual environment.\n\n"
                "Skip this check by passing --skip-venv-check"
            )

    # ---- INSTALL PREREQUISITES ----
    # We need versions of pip and setuptools that understand the
    # 'pyproject.toml' - based build, at least
    subprocess.run(["pip", "install", "-U", "pip", "setuptools>=42"])
    subprocess.run(["pip", "install", "cookiecutter", "click<8"])

    # # ---- CREATE TEST PACKAGES ----
    for path in glob.glob(os.path.join(HERE, "ansys-api-*")):
        shutil.rmtree(path)

    # feed inputs into cookiecutter
    for inp in ["hello_input.txt", "greeter_input.txt"]:
        proc = Popen(
            ["python", "-m", "cookiecutter", ".."],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT,
            cwd=HERE,
        )
        with open(os.path.join(HERE, inp), "rb") as fid:
            out = proc.communicate(input=fid.read())[0]

    # ---- CREATE LOCAL PACKAGE DIRECTORY ----
    # Since the 'greeter' has 'hello' as a build-time dependency, it needs
    # to be findable by 'pip'. We use a local directory as 'PyPI replacement'.
    local_dist = os.path.join(HERE, "local_dist")
    if os.path.isdir(local_dist):
        shutil.rmtree(local_dist)
    os.mkdir(local_dist)

    # ---- DOWNLOAD ADDITIONAL DEPENDENCIES TO 'local_dist' ----
    # We could instead use PyPI _and_ the local directory, but this is unsafe because
    # a package on PyPI could shadow 'ansys-api-hello' (see example 10 on
    # https://pip.pypa.io/en/stable/cli/pip_install/#examples).
    subprocess.run(
        ["pip", "download", "setuptools", "wheel", "ansys-tools-protoc-helper"],
        cwd=local_dist,
    )

    # ---- BUILD 'ansys-api-hello' WHEEL, INSTALL 'ansys-api-greeter' ----
    subprocess.run(
        [
            "pip",
            "wheel",
            "--no-index",
            "--find-links=./local_dist",
            "-w",
            "./local_dist",
            "./ansys-api-hello-world/",
        ],
        cwd=HERE,
    )
    subprocess.run(
        ["pip", "install", "--no-index", "--find-links=./local_dist", "./ansys-api-the-greeter/"],
        cwd=HERE,
    )
    subprocess.run(
        ["python", "-c", '"from ansys.api.the_greeter.v1.greeter_pb2_grpc import GreeterStub"'],
        cwd=HERE,
    )
