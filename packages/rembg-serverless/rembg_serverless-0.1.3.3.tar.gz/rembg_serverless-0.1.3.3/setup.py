import os
import pathlib
import sys

sys.path.append(os.path.dirname(__file__))
from setuptools import setup, find_packages

import versioneer

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

requires = [
    "numpy",
    "onnxruntime",
    "pillow",
]

extras_require = {
    "gpu": ["onnxruntime-gpu"],
}

setup(
    name="rembg_serverless",
    version="0.1.3.3",
    description="Remove image background",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rnag/rembg-aws-lambda",
    author="Daniel Gatis",
    author_email="danielgatis@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="remove, background, u2net",
    include_package_data=False,
    packages=find_packages(),
    package_data={"": ["*.onnx"]},
    python_requires=">3.7, <3.12",
    install_requires=requires,
    extras_require=extras_require,
    # version=versioneer.get_version(),
    # cmdclass=versioneer.get_cmdclass(),
)
