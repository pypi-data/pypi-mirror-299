# -*- coding: utf-8 -*-
# setup.py

from setuptools import setup, find_packages

setup(
    name="smsmobileapi",
    version="1.0.8",
    author="Quest-Concept",
    author_email="info@smsmobileapi.com",
    description="A module that allows sending SMS from your own mobile phone and receiving SMS on your mobile phone, all for free since the mobile plan is used",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/smsmobileapi",  # Remplace par ton URL GitHub
    packages=find_packages(),
    install_requires=[
        'requests',  # Dépendance à requests pour faire des requêtes HTTP
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
