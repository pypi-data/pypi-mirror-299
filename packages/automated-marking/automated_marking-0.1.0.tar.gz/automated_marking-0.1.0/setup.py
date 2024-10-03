from setuptools import setup, find_packages

setup(
    name="automated-marking",  # Your package name
    version="0.1.0",  # Package version
    author="Youssef Kawook",
    author_email="kawooky@gmail.com",
    description="Python script designed to clone Git repositories, detect programming languages, validate the code, and log the results to an Excel file.",
    url="https://github.com/kawooky/CTA-automated-marking",  # Project URL (GitHub, etc.)
    packages=find_packages(),  # Automatically find all packages
    classifiers=[  # Optional: Classifiers to categorize your project
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version requirement
    install_requires=[  # Optional: Dependencies
    "pandas>=1.0",        # Data manipulation library
    "gitpython>=3.0",     # Git integration library
    "requests>=2.0",      # For making HTTP requests
    "openpyxl>=3.0",      # For reading and writing Excel files
    "sqlparse>=0.4",      # For parsing SQL statements
    ],
)
