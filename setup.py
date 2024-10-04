from setuptools import setup, find_packages

from src import (
    __name__,
    __version__,
    __author__,
    __author_email__,
    __description__,
    __repo__,
)

setup(
    name=__name__,
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url=__repo__,
    description=__description__,
    packages=find_packages(),
    install_requires=[
        "numpy>=1.15",
        "pandas>=0.23",
        "matplotlib>=3.3.2",
        "seaborn>=0.10",
        "pillow>=6.2.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
