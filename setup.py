from setuptools import find_packages, setup

setup(
    name="medusa-logger",
    version="1.0.0",
    description="A logging utility package with colored logs.",
    packages=find_packages(),
    install_requires=[
        "coloredlogs",
    ],
)
