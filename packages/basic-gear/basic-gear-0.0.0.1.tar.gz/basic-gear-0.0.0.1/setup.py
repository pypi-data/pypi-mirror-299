import setuptools
from setuptools.command.build_ext import build_ext
import subprocess

from setuptools import setup, find_packages

class CFFIBuild(build_ext):
    def run(self):
        subprocess.run(["python", "core/cffi_interface.py"], check=True)

setup(
    name="basic-gear",
    version="0.0.0.1",
    author="Enrico Zanardo",
    author_email="enrico.zanardo101@gmail.com",
    description="Basic Template Gear",
    url="https://github.com/enricozanardo/basic-gear.git",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'basic-gear=cli.shell:shell', 
        ],
    },
    install_requires=[
        "cffi",
        "pyfiglet"
    ],
    setup_requires=["cffi"],
    cmdclass={"build_ext": CFFIBuild},
    package_data={
    "basic-gear": ["*.so", "*.dylib", "*.dll"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning"
    ],
    python_requires=">=3.11",
)