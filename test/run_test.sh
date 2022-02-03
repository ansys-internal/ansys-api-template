#!/bin/bash

set -e

TEST_WORKDIR=$(realpath $(dirname "$0"))
PROTOC_HELPER_DIR=$(realpath $TEST_WORKDIR"/../../ansys-tools-protoc-helper")

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

# ---- BUILD 'ansys-tools-protoc-helper' WHEEL ----
# Note that we use a local directory as a 'PyPI replacement', since we don't
# yet want to publish the package, but the subsequent builds need to find
# it for the build-time dependencies.
rm -rf local_dist
mkdir local_dist
pushd $PROTOC_HELPER_DIR
pip wheel -w $TEST_WORKDIR/local_dist/ .
popd

# ---- DOWNLOAD ADDITIONAL DEPENDENCIES TO 'local_dist' ----
# We could instead use PyPI _and_ the local directory, but this is unsafe because
# a package on PyPI could shadow 'ansys-tools-protoc-helper' (see example 10 on
# https://pip.pypa.io/en/stable/cli/pip_install/#examples).
pushd ./local_dist
pip download setuptools wheel ansys-tools-protoc-helper
popd

# ---- BUILD 'ansys-api-hello' WHEEL, INSTALL 'ansys-api-greeter' ----
pip wheel --no-index --find-links=./local_dist -w ./local_dist ./ansys-api-hello/
pip install --no-index --find-links=./local_dist ./ansys-api-the-greeter/
python -c "from ansys.api.the_greeter.v1.greeter_pb2_grpc import GreeterStub"
