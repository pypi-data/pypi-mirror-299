import setuptools
from pathlib import Path
setuptools.setup(
    name="zfcpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_namespace_packages(exclude=["tests", "data"])
)
