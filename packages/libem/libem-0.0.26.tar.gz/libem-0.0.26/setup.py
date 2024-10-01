from setuptools import setup, find_packages

setup(
    name="libem",
    version="0.0.26",
    description="Libem python library",
    author="Systems Design Studio",
    author_email="team@SD.studio",
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.10',
    include_package_data=True,
    install_requires = open('requirements.txt').readlines(),
    scripts=['cli/libem'],
)

