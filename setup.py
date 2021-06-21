import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ftx-api-py",
    version="0.0.1",
    author="Charly Chiu",
    description="FTX Python API",
    url="https://github.com/charlychiu/FTX-api-py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=['examples', 'tests', 'docs']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4, <4',
    # deps installed by pip
    install_requires=[
        'asyncio~=3.0',
        'aiohttp~=3.0',
    ],
)