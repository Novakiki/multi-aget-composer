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
        'openai>=1.0.0',
        'click',
        'termcolor',
        'pytest',
        'pytest-asyncio',
        'pytest-mock',
        'watchdog'
    ],
    extras_require={
        'test': [
            'pytest>=8.3.3',
            'pytest-asyncio>=0.24.0',
            'pytest-mock>=3.14.0'
        ],
        'advanced': [
            'sentence-transformers>=2.2.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'evolve=cognitive_agents.cli:cli'
        ],
    }
) 