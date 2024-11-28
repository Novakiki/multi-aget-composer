"""Setup configuration for code-quality-tools package."""

from setuptools import setup, find_packages

setup(
    name="code-quality-tools",
    version="0.1.0",
    packages=find_packages(include=['code_quality_tools', 'code_quality_tools.*']),
    install_requires=[
        "termcolor",
        "openai",
        "pytest",
        "pytest-asyncio",
        "watchdog"
    ],
    python_requires=">=3.8"
) 