from setuptools import setup, find_packages

setup(
    name="automated-marking",
    version="0.1.1",  # Update the version number
    author="Youssef Kawook",
    author_email="kawooky@gmail.com",
    description="Python script designed to clone Git repositories, detect programming languages, validate the code, and log the results to an Excel file.",
    url="https://github.com/kawooky/CTA-automated-marking",
    packages=find_packages(),  # Automatically find all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas>=1.0",
        "gitpython>=3.0",
        "requests>=2.0",
        "openpyxl>=3.0",
        "sqlparse>=0.4",
    ],
    entry_points={
        'console_scripts': [
            'automated-marking=automated_marking.main:main',  # Correct reference to main function
        ],
    },
)
