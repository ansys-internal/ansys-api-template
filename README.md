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
