# API Repository Template

Template repository for creating gRPC API packages that compile to Python source code.

## Using the Template

Before using the template, you need to install its dependencies. Preferably, in a virtual environment:

```bash
pip install cookiecutter 'click<8'
```

Next, you can create your repository with

```bash
cookiecutter gh:ansys/ansys-api-template
```

This will prompt you for the following inputs:

* ``product_name``: The name of the product for which you are creating an API directory. For example, the product name could be ``MAPDL``.
* ``project_slug``: This will be the PyPI name of the new package. The default should be acceptable in most cases.
* ``api_version``: Version number of the API. If you're just getting started, ``0`` should be used.
* ``api_package_version``
* ``protos_dir``: Path to a directory which contains the ``.proto`` files that should be included in the API package. This can be left empty, in which case you need to manually copy in the ``.proto`` files later.

  **NOTE:** The path needs to be given relative to the root of the package that will be created. In other words, you should add a leading ``../`` compared path relative to your working directory, or alternatively use an absolute path.
* ``proto_dependencies``: Specifies whether your ``.proto`` files depend on another API package. If they are independent, you can simply accept the default. Otherwise, the dependencies need to be passed as a JSON dictionary:
  ```json
  {"module": [<your dependencies here>]}
  ```

  For example, if you depend on ``ansys-api-filetransfer`` and ``ansys-api-mapdl``:
  ```json
  {"module": ["ansys-api-filetransfer", "ansys-api-mapdl"]}
  ```

## Maintaining your API repository

Once your API repository has been generated, you can initialize a ``git`` repository inside the new directory. Any changes to the ``.proto`` files can then be made directly in that repository.

Details for how the ``.proto`` compilation works and how it can be controlled from ``setup.py`` and ``pyproject.toml`` can be found in the ``ansys-tools-protoc-helper`` [documentation](TODO: add link).

**IMPORTANT NOTE:** You **must not** create an ``__init__.py`` file directly in the ``ansys`` or ``ansys/api`` directories. Doing so would make it impossible to use other packages which use the ``ansys.`` or ``ansys.api`` namespace alongside your package. This is because we use implicit namespace packages, see the [PEP 420](https://www.python.org/dev/peps/pep-0420/) for details.
