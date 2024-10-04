from setuptools import find_packages, setup

__version__ = "0.1.0"

setup(
    name="mara_client",
    version=__version__,
    description="A client for the MARA conversational agent for cheminformatics.",
    author="Sam Hessenauer, Alex McNerney, Mike Rosengrant",
    author_email="sam@nanome.ai, alex@nanome.ai, mike.rosengrant@nanome.ai",
    url="https://nanome.ai/mara",
    license="",
    packages=find_packages(),
    install_requires=[],
    # long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
