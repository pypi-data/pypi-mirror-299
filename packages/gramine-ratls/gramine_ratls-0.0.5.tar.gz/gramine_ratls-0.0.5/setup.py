import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="gramine-ratls",
    packages=find_packages(),
    package_dir={"gramine_ratls": "src/gramine_ratls"},
    version="0.0.5",
    description="Gramine RATLS Python wrapper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dscc-admin-ch/gramine-ratls-python/",
    author="Data Science Competence Center, Swiss Federal Statistical Office",
    author_email="dscc@bfs.admin.ch",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Security",
    ],
    keywords=[
        "gramine",
        "sgx",
        "ratls"
    ],
    python_requires=">=3.10, <4",
    install_requires=[],
)
