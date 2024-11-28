"""Setup configuration for agent-coordinator package."""

from setuptools import setup, find_packages

setup(
    name="agent-coordinator",
    version="0.1.0",
    description="Coordinated agent system for code quality monitoring",
    author="Novakiki",
    packages=find_packages(),
    install_requires=[
        "watchdog",
        "termcolor",
        "typing-extensions",
        "pytest",
        "pytest-asyncio"
    ],
    python_requires=">=3.9",
    entry_points={
        'console_scripts': [
            'agent-monitor=coordinator.agents.monitor.monitor_agent:main',
        ],
    }
) 