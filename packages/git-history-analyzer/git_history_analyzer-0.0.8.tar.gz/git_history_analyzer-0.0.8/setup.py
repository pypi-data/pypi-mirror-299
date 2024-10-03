# python3 setup.py sdist bdist_wheel
import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="git-history-analyzer",
    version="0.0.8",
    author="Jorge Cardona",
    description="Generate Reports from Your Repository's Git History",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgecardona/git-history-analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)