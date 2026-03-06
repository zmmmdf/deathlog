from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deathlog",
    version="1.0.0",
    author="ziyam",
    description="AI Post-Mortem Generator from git history",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zmmmdf/deathlog",
    py_modules=["main"],
    install_requires=["anthropic", "typer", "rich"],
    entry_points={
        "console_scripts": [
            "deathlog=main:app"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Build Tools",
    ],
    python_requires=">=3.11",
)
