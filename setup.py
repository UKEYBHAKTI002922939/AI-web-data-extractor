from setuptools import setup, find_packages

setup(
    name="rufus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "transformers>=4.0.0",
        "torch",  # Required for Hugging Face pipelines
        "nltk>=3.6.1",
    ],
    entry_points={
        "console_scripts": [
            "rufus = rufus.main:main",
        ],
    },
)