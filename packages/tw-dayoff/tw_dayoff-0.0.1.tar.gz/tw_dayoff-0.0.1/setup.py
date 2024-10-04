import pathlib

import setuptools

setuptools.setup(
    name="tw_dayoff",
    version="0.0.1",
    descruption="A simple Python package to get Taiwan's dayoff information.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://dybts.cloudns.be",
    author="Neko No Akuma",
    author_email="nekotw@nekotw.serv00.net",
    license="GNU GPLv3",
    project_urls={
        "Documentation": "https://dybts.cloudns.be",
        "Source": "https://github.com/Neko-no-akuma-TW/tw_dayoff",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=["requests"],
    packages=setuptools.find_packages(where="tw_dayoff"),
    include_package_data=True,
    entry_points={"console_scripts": ["tw_dayoff=tw_dayoff.cli:main"]},
)