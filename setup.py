"""
Setup script for Enzyme Kinetics Extractor
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="enzyme-kinetics-extractor",
    version="1.0.1",
    author="Enzyme Kinetics Research Team",
    author_email="your-email@example.com",
    description="Universal tool for extracting enzyme kinetics data from IWBK files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/enzyme-kinetics-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: Public Domain",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "enzyme-kinetics-extractor=enzyme_kinetics_extractor:main",
        ],
    },
    keywords="enzyme kinetics spectrophotometry IWBK Thermo Scientific data extraction",
    project_urls={
        "Bug Reports": "https://github.com/your-username/enzyme-kinetics-extractor/issues",
        "Source": "https://github.com/your-username/enzyme-kinetics-extractor",
        "Documentation": "https://github.com/your-username/enzyme-kinetics-extractor/blob/main/README.md",
    },
)