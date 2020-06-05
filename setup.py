"""setup.py file."""
from setuptools import setup, find_packages

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (len(r) > 0 and not r.startswith("#"))]

with open("README.md", "r") as fs:
    long_description = fs.read()


__author__ = "Roman Dodin <dodin.roman@gmail.com>"

setup(
    name="napalm-sros_ssh",
    version="0.0.1",
    packages=find_packages(),
    author="Roman Dodin",
    author_email="dodin.roman@gmail.com",
    description="Nokia SR OS SSH based driver for NAPALM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    url="https://github.com/hellt/napalm_sros-ssh",
    include_package_data=True,
    install_requires=reqs,
)
