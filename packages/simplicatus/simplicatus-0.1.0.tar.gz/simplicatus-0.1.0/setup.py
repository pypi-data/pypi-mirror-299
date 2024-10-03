from setuptools import setup, find_packages

setup(
    name="simplicatus",
    version="0.1.0",
    description="Grossomodo a Python library for converting md documents into PDF, kindle friendly. ",
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
