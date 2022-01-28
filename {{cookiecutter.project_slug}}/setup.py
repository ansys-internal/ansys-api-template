import setuptools

from pyansys_protoc_helper import CMDCLASS_OVERRIDE


if __name__ == "__main__":
    setuptools.setup(
        name="ansys-{{ cookiecutter.product_name | lower }}-protos",
        author="ANSYS, Inc.",
        python_requires=">=3.7",
        install_requires=["grpcio~=1.0", "protobuf~=3.0"{% for mod in cookiecutter.proto_dependencies['modules'] %}, "{{ mod }}"{% endfor %}],
        packages = ["ansys.api.{{ cookiecutter.product_name | lower }}.v{{ cookiecutter.api_version }}"],
        package_dir={'': "src"},
        package_data={
            "": ["*.proto", "*.pyi", "py.typed"],
        },
        entry_points={
            "pyansys_protoc_helper.proto_provider": {
                "{{ cookiecutter.product_name | lower }}.v{{ cookiecutter.api_version }}=ansys.api.{{ cookiecutter.product_name | lower }}.v{{ cookiecutter.api_version }}"
            },
        },
        cmdclass = CMDCLASS_OVERRIDE
    )
