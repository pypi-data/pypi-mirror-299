from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="visually",
    version="1.0.0",
    author="Sariya Ansari",
    description="A unified interface for data visualization using Matplotlib, Seaborn, and Plotly.",
    long_description="The Visually class serves as a unified interface for visualizing data using different backends, such as Matplotlib, Seaborn, and Plotly. This document provides a comprehensive guide on how to initialize the class, set the visualization style, and create various types of graphs.",  # This will appear on PyPI project page
    long_description_content_type="text/markdown",
    url="https://github.com/Sariya-Ansari/visually.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "plotly",
        "kaleido",  # For saving Plotly images
    ],
)
