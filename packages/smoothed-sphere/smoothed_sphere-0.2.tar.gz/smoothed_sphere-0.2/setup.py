
from setuptools import setup, find_packages

setup(
    name="smoothed_sphere",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "plotly"
    ],
    description="A package to plot 3D smoothed spheres with electrodes.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
    