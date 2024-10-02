# Copyright 2024 Wirepas Ltd licensed under Apache License, Version 2.0
#
# See file LICENSE for full license details.
#
import os
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme_file = "README.md"


with open(os.path.join(here, "wirepas_wpe_apt", readme_file)) as f:
    long_description = f.read()


def get_requirements(path):
    """ Get requirements requirements.txt """
    requirements = set()
    with open(path) as handle:
        for line in handle:
            # Strip comments.
            line = re.sub(r"^#.*|\s#.*", "", line)
            # Ignore empty lines
            if line and not line.isspace():
                requirements.add(re.sub(r"\s+", "", line))
    return sorted(requirements)


about = {}
with open("./wirepas_wpe_apt/__about__.py") as f:
    exec(f.read(), about)


setup(
    name=about["__pkg_name__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    classifiers=about["__classifiers__"],
    keywords=about["__keywords__"],
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements("./wirepas_wpe_apt/requirements.txt"),
    entry_points={
        "console_scripts": [
            "wirepas_apt_data_collector=wirepas_wpe_apt.data_collector:main",
            "wirepas_apt_playback=wirepas_wpe_apt.playback:main",
            "wirepas_apt_report_generator=wirepas_wpe_apt.report_generator:main",
        ]
    }
)
