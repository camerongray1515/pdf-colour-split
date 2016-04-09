#!/usr/bin/env python3
from distutils.core import setup
from pip.req import parse_requirements
from pip.download import PipSession

install_requirements = parse_requirements("requirements.txt",
    session=PipSession())

setup(
    name="pdfcoloursplit_web",
    description="PDF Colour Split Web Interface",
    version="1.0",
    author="Cameron Gray",
    packages=["pdfcoloursplit_web"],
    package_data={"pdfcoloursplit_web": ["config.ini"]},
    install_requires=[str(ir.req) for ir in install_requirements],
    entry_points={
        "console_scripts": [
            "pdfcoloursplit_web = pdfcoloursplit_web.web:main",
            "pdfcoloursplit_web_worker = pdfcoloursplit_web.worker:main"
        ]
    }
)
