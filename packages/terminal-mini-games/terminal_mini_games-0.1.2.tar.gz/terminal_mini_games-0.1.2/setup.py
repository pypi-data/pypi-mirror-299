from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terminal-mini-games",
    version="0.1.2",
    author="Hanzi Li",
    author_email="hanzili0217@gmail.com",
    description="A collection of mini-games playable in the terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanzili/terminal-mini-games",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama",
    ],
    entry_points={
        "console_scripts": [
            "terminal-mini-games=terminal_mini_games.main:main",
        ],
    },
)