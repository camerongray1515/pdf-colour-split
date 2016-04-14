#!/usr/bin/env python3
import os
import re
from distutils.core import setup
from pip.req import parse_requirements
from pip.download import PipSession

install_requirements = parse_requirements("requirements.txt",
    session=PipSession())

#TODO - Tidy up package data logic
def find_files(directory):
    found_files = []
    for root, subFolders, files in os.walk(directory):
        for filename in files:
            found_files.append(os.path.join(root, filename))
    return found_files

package_data_files = ["config.ini"]
package_data_files += find_files("pdfcoloursplit_web/templates")

setup(
    name="pdfcoloursplit_web",
    description="PDF Colour Split Web Interface",
    version="1.0",
    author="Cameron Gray",
    packages=["pdfcoloursplit_web"],
    package_data={"pdfcoloursplit_web":
        [re.sub("^pdfcoloursplit_web/", "", f) for f in package_data_files]},
    install_requires=[str(ir.req) for ir in install_requirements],
    entry_points={
        "console_scripts": [
            "pdfcoloursplit_web = pdfcoloursplit_web.web:main",
            "pdfcoloursplit_web_worker = pdfcoloursplit_web.worker:main"
        ]
    }
)
