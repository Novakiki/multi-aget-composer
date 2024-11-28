"""Setup configuration for cognitive agents system."""

from setuptools import setup, find_packages

setup(
    name="cognitive-agents",
    version="0.1.0",
    description="Recursive cognitive agent system for mental health",
    packages=find_packages(include=['cognitive_agents', 'cognitive_agents.*']),
    install_requires=[
        "termcolor",
        "openai",
        "pytest",
        "pytest-asyncio",
        "watchdog"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'cognitive-shell=cognitive_agents.examples.interactive:main',
        ],
    }
) 