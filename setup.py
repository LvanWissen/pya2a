import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pya2a",
    version="0.0.1",
    author="Leon van Wissen",
    author_email="l.vanwissen@uva.nl",
    description="A2A parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lvanwissen/pya2a",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
