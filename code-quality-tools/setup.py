"""Setup configuration for code-quality-tools package."""

from setuptools import setup, find_packages

setup(
    name="code-quality-tools",
    version="0.1.0",
    description="Agent-aware code quality monitoring system",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "termcolor",
        "openai",
        "pytest",
        "pytest-asyncio",
        "watchdog"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3.8",
    ]
) 