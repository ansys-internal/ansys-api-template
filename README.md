# API Repository Template

Template repository for creating gRPC API packages that compile to Python source code.


## Expected Usage

Using this template you can create a Python package to generate a Python wheel
that exposes the interface files generated from the gRPC proto files. For
example, for a `file_transfer` service:

```bash
pip install ansys-api-tools-file-transfer
```

This package would then be used by a "higher level" Python library.

The directory created by this template is fully compatible with GitHub and can
be uploaded to the [ansys](https://github.com/ansys) organization to
automatically push the Python package to PyPI.


## Using the Template

Before using the template, you need to install its dependencies. Preferably, in a virtual environment:

```bash
pip install cookiecutter 'click<8'
```

Next, you can create your repository (via ssh) with:

```bash
cookiecutter git+ssh://git@github.com/ansys/ansys-api-template
```

or if you prefer https:

```bash
cookiecutter gh:ansys/ansys-api-template
```

This will prompt you for the following inputs:

* `product_name`: The name of the product for which you are creating an API directory. For example, the product name could be `MAPDL`, `DPF`, or `tools`.
* `library_name`: The name of the library for which you are creating an API directory. For example, the library name could be `core`, `file-transfer` or an empty string.
* `project_name_slug`: The package name used for the API package. In most cases, the suggested default should work fine.
* `api_version`: Version number of the API. If you're just getting started, `0` should be used.
* `api_package_version`: The version of the API package. The default `0.1.0` is suitable if this is the first release.
* `protos_dir`: Path to a directory which contains the `.proto` files that should be included in the API package. This can be left empty, in which case you need to manually copy in the `.proto` files later.

  **NOTE:** The path needs to be given relative to the root of the package that will be created. In other words, you should add a leading `../` compared path relative to your working directory, or alternatively use an absolute path.
* `proto_dependencies`: Specifies whether your `.proto` files depend on another API package. If they are independent, you can simply accept the default. Otherwise, the dependencies need to be passed as a JSON dictionary:
  ```json
  {"modules": [<your dependencies here>]}
  ```

  For example, if you depend on ``ansys-api-file-transfer`` and ``ansys-api-mapdl``:
  ```json
  {"modules": ["ansys-api-tools-file-transfer", "ansys-api-mapdl-core"]}
  ```

## Maintaining your API repository

Once your API repository has been generated, you can initialize a `git` repository inside the new directory. Any changes to the `.proto` files can then be made directly in that repository.

Details for how the `.proto` compilation works and how it can be controlled from `setup.py` and `pyproject.toml` can be found in the `ansys-tools-protoc-helper` [documentation](https://github.com/ansys/ansys-tools-protoc-helper).

**IMPORTANT NOTE:** You **must not** create an `__init__.py` file directly in the `ansys` or `ansys/api` directories. Doing so would make it impossible to use other packages which use the `ansys.` or `ansys.api` namespace alongside your package. This is because we use implicit namespace packages, see the [PEP 420](https://www.python.org/dev/peps/pep-0420/) for details.


## Building Packages

To build the gRPC packages, run:

```bash
pip install build
python -m build
```

This will create both the source distribution containing just the protofiles
along with the wheel containing the protofiles and build Python interface
files.

Note that the interface files are identical regardless of the version of Python
used to generate them, but the last pre-built wheel for ``grpcio~=1.17`` was
Python 3.7, so to improve your build time, use Python 3.7 when building the
wheel.


#### Manual Deployment

After building the packages, manually deploy them with:

```bash
pip install twine
twine upload dist/*
```

Note that this should be automatically done through CI/CD. See the following section.


## Deploying Wheels to Public PyPI

The repository generated from this template contains a `.github` directory
containing the workflow file ``ci.yml`` which uses contains the GitHub Actions
to automatically build the packages for these gRPC Python interface files. By
default, these are built on PRs, the main branch, and on tags when
pushing. Artifacts are uploaded for each PR.

It also contains the following (commented out) step:

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

This step is triggered only when tags are pushed and is commented out to avoid
inadvertently pushing wheels to public PyPI. Once uncommenting this section,
deploy to [PyPI](https://pypi.org/) via:

```bash
git tag v0.5.0
git push --tags
```

This will use the organizational secret. Be sure to replace it with a project specific token.
