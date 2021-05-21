import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="automata_toolkit",
    version="1.0.2",
    description="A tiny library which contains tools to convert, minimize and visualize Regular Expressions, NFA and DFA.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/b30wulffz/automata-toolkit",
    author="Shlok Pandey",
    author_email="shlokpandey123@gmail.com",
    license="MIT",
    keywords='automata, visualizer, nfa, dfa, regular expression',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["automata_toolkit"],
    include_package_data=True,
    install_requires=[],
    entry_points={},
)