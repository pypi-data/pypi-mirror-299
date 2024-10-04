from setuptools import find_packages, setup

# for typing
__version__ = "0.0.0"
exec(open("../mara/version.py").read())

with open("README.md", "r") as fh:
    long_description = fh.read()

test_version = f'{__version__}.dev0'
setup(
    name="mara_client",
    version=test_version,
    description="A client for the MARA conversational agent for cheminformatics.",
    long_description=long_description,
    author="Sam Hessenauer, Alex McNerney, Mike Rosengrant",
    author_email="sam@nanome.ai, alex@nanome.ai, mike.rosengrant@nanome.ai",
    url="https://nanome.ai/mara",
    license="",
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'pandas==2.1.4',
        'pydantic==2.7.3',
    ],
    # long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
