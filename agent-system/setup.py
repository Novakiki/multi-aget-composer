setup(
    name="agent-system",
    version="0.1.0",
    description="Coordinated agent system for code quality",
    packages=find_packages(),
    install_requires=[
        "code-quality-tools",  # Our other package
        "watchdog",
        "termcolor"
    ]
) 