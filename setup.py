"""Setup configuration for qrgen."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = ""
readme_file = this_directory / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text()

setup(
    name="qrgen",
    version="0.1.0",
    description="A simple command-line tool for generating QR codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dougie Richardson",
    python_requires=">=3.7",
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]",
        "pillow",
    ],
    entry_points={
        "console_scripts": [
            "qrgen=qrgen.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
