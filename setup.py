from setuptools import find_packages, setup

with open("docs/README.md", "r") as f:
    description = f.read()

setup(
    name="vulcan-utils",
    version="1.12.1",
    description="A utility package for Python",
    packages=find_packages(),
    install_requires=[
        "coloredlogs",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
