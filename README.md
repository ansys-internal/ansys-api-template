# Ansys API Template

This repository contains a template for creating gRPC API packages that compile to Python source code.


## Expected usage

Using this template, you can create a Python package to generate a Python wheel
that exposes the interface files generated from gRPC PROTO files.

Install the `ansys-api-tools-file-transfer` package with this command:

```bash
pip install ansys-api-tools-file-transfer
```

You can then use this package in a "higher-level" Python library.

The directory created by this template is fully compatible with GitHub and can
be uploaded to the [Ansys](https://github.com/ansys) organization to
automatically push the Python package to PyPI.


## Installation and usage

Before using the template, run this command, preferably in a virtual environment, to install
package dependencies:

```bash
pip install cookiecutter 'click<8'
```

Next, create your repository via ssh with this command:

```bash
cookiecutter git+ssh://git@github.com/ansys/ansys-api-template
```

Optionally, if you prefer https, use this command:

```bash
cookiecutter gh:ansys/ansys-api-template
```

You are then prompted for the following inputs:

* `product_name`: Name of the product for which you are creating an API directory. For example, the product name could be ``MAPDL``, ``DPF``, or ``tools``.
* `library_name`: Name of the library for which you are creating an API directory. For example, the library name could be ``core``, ``file-transfer``, or an empty string.
* `project_name_slug`: Name for the API package. In most cases, the suggested default should work fine.
* `api_version`: Version number of the API package. If you're just getting started, ``0`` should be used.
* `api_package_version`: Version of the API package. If this is the first release, the default ``0.1.0`` is suitable.
* `protos_dir`: Path to a directory that contains the PROTO files to include in the API package. This can be left empty, in which case must manually copy in the PROTO files later.

  **NOTE:** The path must be given relative to the root of the package that is to be created. In other words, you should add a leading ``../`` compared path relative to your working directory, or alternatively use an absolute path.
* `proto_dependencies`: Specifies whether your PROTO files depend on another API package. If they are independent, you can accept the default. Otherwise, you must pass dependencies as a JSON dictionary:

  ```json
  {"modules": [<your dependencies here>]}
  ```

  For example, if you depend on the ``ansys-api-file-transfer`` and ``ansys-api-mapdl`` packages, you
  would pass these dependencies:

  ```json
  {"modules": ["ansys-api-tools-file-transfer", "ansys-api-mapdl-core"]}
  ```

## Maintaining your API repository

Once your API repository has been generated, you can initialize a ``git`` repository inside the new directory. Any changes to PROTO files can then be made directly in your repository.

For information on how the compilation of PROTO files works and how compilation can be controlled from the ``setup.py`` and ``pyproject.toml`` files, see the [documentation](https://ansys.github.io/ansys-tools-protoc-helper/) for the ``ansys-tools-protoc-helper`` package.

**NOTE:** You **must not** create an ``__init__.py`` file directly in the ``ansys`` or ``ansys/api`` directories. Doing so would make it impossible to use other packages that use the `ansys.` or `ansys.api` namespace alongside your package. This is because implicit namespace packages are used. For more information, see [PEP 420] - Implicit Namespace Packages (https://www.python.org/dev/peps/pep-0420/).


## Build packages

To build the gRPC packages, run these commands:

```bash
pip install build
python -m build
```

The preceding commands create both the source distribution containing only the PROTO files
and the wheel containing the PROTO files and build Python interface files.

Note that the interface files are identical regardless of the version of Python
used to generate them, but the last pre-built wheel for ``grpcio~=1.17`` was
Python 3.7. To improve your build time, use Python 3.7 when building the
wheel.


#### Manual Deployment

After building the packages, manually deploy them with these commands:

```bash
pip install twine
twine upload dist/*
```

Note that this should be automatically done through CI/CD. See the following section.


## Deploying wheels to public PyPI

The repository generated from this template contains a ``.github`` directory
with the ``ci.yml`` workflow file. This file uses GitHub Actions
to automatically build the packages for the gRPC Python interface files. By
default, these are built on PRs, the main branch, and on tags when
pushing. Artifacts are uploaded for each PR.

It also contains the following (commented out) action:

```
- name: Upload to Public PyPI
  run: |
    pip install twine
    twine upload --skip-existing ./**/*.whl
    twine upload --skip-existing ./**/*.tar.gz
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: {% raw %}${{ secrets.PYPI_TOKEN }} {%- endraw %}

```

This action is triggered only when tags are pushed. It is commented out to avoid
inadvertently pushing wheels to public PyPI. Once you uncomment this section,
you can deploy to [PyPI](https://pypi.org/) with these commands:

```bash
git tag v0.5.0
git push --tags
```

**NOTE:** This upload action use the organizational secret. Be sure to replace it with a project-specific token.
