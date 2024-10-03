
from setuptools import setup, find_packages

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smoothed_sphere",
    version="0.4",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "plotly"
    ],
    description="A package to plot 3D smoothed spheres with electrodes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/smoothed-sphere/0.3/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
    