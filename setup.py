#!/usr/bin/env python3

from setuptools import setup

setup(
    name="mygit",
    version='1.0.0',
    packages=['mygit'],
    description="A minimal version control system implementation inspired by Git",
    author="sumanengg",
    url="https://github.com/sumanengg/mygit",
    
    # Python version requirement
    python_requires=">=3.7",
    
    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
            "pre-commit>=4.3.0"
        ],
    },
    
    # Command-line script
    entry_points={
        'console_scripts': [
            'mygit = mygit.cli:main'
        ]
    },
    
    # Project classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)