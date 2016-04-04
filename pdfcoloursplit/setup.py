#!/usr/bin/env python3
from distutils.core import setup
from pip.req import parse_requirements
from pip.download import PipSession

install_requirements = parse_requirements("requirements.txt",
    session=PipSession())

setup(
    name="pdfcoloursplit",
    description="PDF Colour Split",
    version="1.0",
    author="Cameron Gray",
    packages=["pdfcoloursplit"],
    install_requires=[str(ir.req) for ir in install_requirements],
    entry_points={
        "console_scripts": [
            "pdfcoloursplit = pdfcoloursplit.pdfcoloursplit:main"
        ]
    }
)
