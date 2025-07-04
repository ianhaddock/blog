"""setup.py"""

from setuptools import find_packages, setup

setup(
    name="app",
    version="0.2.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
        "Flask-Markdown",
        "Markdown",
        "configparser",
        "datetime",
        "PyYAML",
        "Pygments",
    ],
)
