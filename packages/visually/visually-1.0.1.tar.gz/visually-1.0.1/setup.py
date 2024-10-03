from pathlib import Path

from setuptools import setup, find_packages

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="visually",
    version="1.0.1",
    author="Sariya Ansari",
    description="A unified interface for data visualization using Matplotlib, Seaborn, and Plotly.",
    long_description=long_description,
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
