### {{ cookiecutter.project_slug }} gRPC Interface Package

This Python package contains the auto-generated gRPC Python interface files for {{ cookiecutter.product_name }}.


#### Build

To build the wheel, run:

```
pip install build
python -m build
```

This will create both the source distribution containing just the protofiles along with the wheel containing the protofiles and build Python interface files.

Note that the interface files are identical regarless of the version of Python,
but the last pre-built version of ``grpcio~={{ cookiecutter.grpcio_version }}``
was Python 3.7, so to improve your build time, use Python 3.7 when building the
wheel.


#### Deployment

After building the packages, manually deploy them with:

```
pip install twine
twine upload dist/*
```

Note that this is automatically done through CI/CD.


#### Automation
