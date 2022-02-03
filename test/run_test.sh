#!/bin/bash

set -e

TEST_WORKDIR=$(realpath $(dirname "$0"))


if [ "$1" != "--no-virtualenv-check" ]
then
    # check that we are in a virtualenv..
    python -c 'import sys; assert hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix), "Must run the test script from within a virtual environment."'
fi

pushd $TEST_WORKDIR
# ---- INSTALL PREREQUISITES ----
# We need versions of pip and setuptools that understand the 'pyproject.toml' - based build, at least
pip install -U pip setuptools==42
pip install cookiecutter 'click<8'

# ---- CREATE TEST PACKAGES ----
rm -rf ./ansys-api-*
cookiecutter ..  < hello_input.txt
cookiecutter ..  < greeter_input.txt

# ---- CREATE LOCAL PACKAGE DIRECTORY ----
# Since the 'greeter' has 'hello' as a build-time dependency, it needs
# to be findable by 'pip'. We use a local directory as 'PyPI replacement'.
rm -rf local_dist
mkdir local_dist

# ---- DOWNLOAD ADDITIONAL DEPENDENCIES TO 'local_dist' ----
# We could instead use PyPI _and_ the local directory, but this is unsafe because
# a package on PyPI could shadow 'ansys-api-hello' (see example 10 on
# https://pip.pypa.io/en/stable/cli/pip_install/#examples).
pushd ./local_dist
pip download setuptools wheel ansys-tools-protoc-helper
popd

# ---- BUILD 'ansys-api-hello' WHEEL, INSTALL 'ansys-api-greeter' ----
pip wheel --no-index --find-links=./local_dist -w ./local_dist ./ansys-api-hello/
pip install --no-index --find-links=./local_dist ./ansys-api-the-greeter/
python -c "from ansys.api.the_greeter.v1.greeter_pb2_grpc import GreeterStub"
