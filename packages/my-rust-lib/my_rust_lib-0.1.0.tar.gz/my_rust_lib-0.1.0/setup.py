from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="my_rust_lib",
    version="0.1.0",
    rust_extensions=[RustExtension("my_rust_lib.python", "Cargo.toml")],
    packages=["my_rust_lib"],
    zip_safe=False,
)
