from setuptools import setup

setup(
    name="deathlog",
    version="0.1.0",
    install_requires=["anthropic", "typer", "rich"],
    entry_points={
        "console_scripts": [
            "deathlog=main:app"
        ]
    }
)
