from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Doc-Converter',
    version='0.0.1',
    description='This module is designed to convert all types of files into usable text str to make it easier to work with python',
    author='Ibrahim',
    author_email='string2025@gmail.com',
    packages=find_packages(),
    install_requires=[
        'python-docx',
'python-pptx',
'pypdf2'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
)