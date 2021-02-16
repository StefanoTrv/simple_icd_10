import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_icd_10",
    version="1.4.0",
    author="Stefano Travasci",
    author_email="stefanotravasci@gmail.com",
    description="A simple python library for ICD-10 codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StefanoTrv/simple_icd_10",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    keywords='ICD-10 icd 10 codes',
)