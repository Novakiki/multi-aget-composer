"""Setup configuration for cognitive agents system."""

from setuptools import setup, find_packages

setup(
    name="cognitive_agents",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pinecone-client',
        'neo4j',
        'motor',
        'pymongo',
        'asyncpg',
        'click',
        'termcolor',
        'pytest',
        'pytest-asyncio',
        'pytest-mock',
        'watchdog'
    ],
    entry_points={
        'console_scripts': [
            'cognitive=cognitive_agents.cli:cli'
        ],
    }
) 