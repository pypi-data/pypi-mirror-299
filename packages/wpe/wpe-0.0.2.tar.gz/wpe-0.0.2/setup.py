from setuptools import setup, find_packages

setup(
    name="wpe",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain_community",
        "qdrant_client"
    ],
    author="Dom and Sam",
    author_email="dom@pieces.app, sam@pieces.app",
    description="A Python package for processing WPE events.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
