from setuptools import setup, find_packages
from pathlib import Path

# read the contents of the README.md file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="simplicatus",
    version="0.1.2",
    description="Grossomodo a Python library for converting md documents into PDF, kindle friendly.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Sebastjan Rijavec",
    author_email="sebastjan.rijavec@gmail.com",
    url="https://github.com/sebs-tech/simplicatus",
    packages=find_packages(),
    license="MIT",  # Open-source license for individuals
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[],  # Dependencies go here
)
