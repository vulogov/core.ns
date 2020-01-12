import os
from setuptools import setup, find_packages
try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

name="corens"
version="0.0"
release="0.0.1"

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name=name,
    setup_requires=['pytest-runner'],
    version=release,
    description='Functional, Namespace-based application CORE',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    python_requires='>=3.6',
    url='https://github.com/vulogov/core.ns',
    author='Vladimir Ulogov',
    author_email='vladimir.ulogov@me.com',
    license='GPL3',
    install_requires=load_requirements("requirements.txt"),
    packages=find_packages())
