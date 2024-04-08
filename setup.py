from setuptools import find_packages, setup

with open("docs/README.md", "r") as f:
    description = f.read()

setup(
    name="vulcan-logger",
    version="1.5.1",
    description="A logging utility package with colored logs.",
    packages=find_packages(),
    install_requires=[
        "coloredlogs",
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
