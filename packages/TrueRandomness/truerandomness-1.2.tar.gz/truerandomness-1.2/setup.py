# setup.py
from setuptools import setup, find_packages

setup(
    name="TrueRandomness",
    version="1.2",
    packages=find_packages(),
    description="A Python library that generates true randomness using real-time data.",
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    author="SForces",
    author_email="forces3564@gmail.com",
    url="https://github.com/SForces/TrueRandomness-Python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
