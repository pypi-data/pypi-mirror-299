from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'A set of tools for extracting and working with Wikipedia API and dump data.'
LONG_DESCRIPTION = 'WikiToolkit is a Python package that provides a set of tools for extracting and working with Wikipedia API and dump data.'

# Setting up
setup(
        name="wikitoolkit", 
        version=VERSION,
        author="Patrick Gildersleve",
        author_email="<p.gildersleve@exeter.ac.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['mwapi', 'mwviews'],
        keywords=['python', 'wikipedia', 'wikimedia', 'mediawiki', 'API', 'dump'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)