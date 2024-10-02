import importlib
import sys
from pathlib import Path

from setuptools import find_packages, setup


def import_module(file: str):
    file = Path(file).resolve()
    if file.parent not in sys.path:
        sys.path.append(str(file.parent))
    return importlib.import_module(file.stem)

path = Path(__file__).parent.resolve()

readme_file = path / "README.md"
package_path = path / r"rangeutils"
version = import_module(file=package_path / "version.py")

setup(
    name="rangeutils",
    version=version.__version__,
    description="Utilities for manipulating and converting Python ranges and boolean lists",
    long_description=readme_file.read_text(encoding="utf8"),
    long_description_content_type="text/markdown",
    license="MIT",

    author="Kris Wang",
    author_email="wenhom.wang@gmail.com",
    url="https://github.com/Hom-Wang/rangeutils",

    packages=find_packages(),
    package_data={"rangeutils": ["*"]},
    # include_package_data=True,
    entry_points={"console_scripts": []},
    python_requires=">=3.10",
    install_requires=[
        "numpy",
    ],
)
