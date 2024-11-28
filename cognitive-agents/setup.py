"""Setup configuration for cognitive agents system."""

from setuptools import setup, find_packages

setup(
    name="cognitive-agents",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "termcolor",
        "openai",
        "pytest",
        "pytest-asyncio",
        "watchdog"
    ],
    entry_points={
        'console_scripts': [
            'cognitive=cognitive_agents.cli:cli'
        ],
    }
) 