import setuptools

from ansys.tools.protoc_helper import CMDCLASS_OVERRIDE

if __name__ == "__main__":
    setuptools.setup(
        name="ansys-api-{{ cookiecutter.product_name | lower }}",
        author="ANSYS, Inc.",
        license="MIT",
        python_requires=">=3.7",
        install_requires=["grpcio~=1.17", "protobuf~=3.19"{% for mod in cookiecutter.proto_dependencies['modules'] %}, "{{ mod }}"{% endfor %}],
        packages=setuptools.find_namespace_packages(".", include=("ansys.*",)),
        package_data={
            "": ["*.proto", "*.pyi", "py.typed"],
        },
        entry_points={
            "ansys.tools.protoc_helper.proto_provider": [
                "ansys.api.{{ cookiecutter.product_name | lower }}.v{{ cookiecutter.api_version }}=ansys.api.{{ cookiecutter.product_name | lower }}.v{{ cookiecutter.api_version }}"
            ],
        },
        cmdclass = CMDCLASS_OVERRIDE
    )
