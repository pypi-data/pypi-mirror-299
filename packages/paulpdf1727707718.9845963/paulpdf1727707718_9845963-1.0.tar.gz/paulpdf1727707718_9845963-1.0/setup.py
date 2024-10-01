import setuptools
from pathlib import Path
import time

setuptools.setup(
    name="paulpdf" + str(time.time()),
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
