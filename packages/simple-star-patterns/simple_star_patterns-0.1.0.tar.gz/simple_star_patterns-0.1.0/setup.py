# setup.py

from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="simple-star-patterns",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple library for printing star patterns",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-star-patterns",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    keywords="star patterns ascii art",
)