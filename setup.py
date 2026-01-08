"""
FastAPI PayFast Integration Package Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "python-multipart>=0.0.6",
]

dev_requirements = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.24.0",
    "black>=23.7.0",
    "isort>=5.12.0",
    "flake8>=6.1.0",
    "mypy>=1.5.0",
    "pre-commit>=3.3.0",
]

setup(
    name="fastapi-payfast",
    version="0.0.1",
    author="Carrington Muleya",
    author_email="carrington.muleya@outlook.com",
    description="FastAPI integration package for PayFast payment gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fastapi-payfast",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/fastapi-payfast/issues",
        "Documentation": "https://github.com/yourusername/fastapi-payfast#readme",
        "Source Code": "https://github.com/yourusername/fastapi-payfast",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Framework :: Pydantic",
        "Framework :: Pydantic :: 2",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "httpx>=0.24.0",
        ],
    },
    keywords=[
        "fastapi",
        "payfast",
        "payment",
        "gateway",
        "south africa",
        "payments",
        "integration",
        "api",
        "pydantic",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            # Add CLI commands if needed
            # "payfast-cli=fastapi_payfast.cli:main",
        ],
    },
)