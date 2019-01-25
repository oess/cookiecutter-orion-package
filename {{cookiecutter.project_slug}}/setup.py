# (C) 2018 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

from re import compile
from ast import literal_eval
from sys import argv, exit
from json import dumps
from setuptools import setup, find_packages, convert_path

# Requirements for {{cookiecutter.module_name}}
requirements = ["OpenEye-orionplatform==0.1.12", "OpenEye-snowball==0.13.4"]

# Obtain version of cuberecord
_version_re = compile(r'__version__\s+=\s+(.*)')
version_file = convert_path("./{{cookiecutter.module_name}}/__init__.py")
with open(version_file, 'rb') as f:
    version = str(literal_eval(_version_re.search(f.read().decode('utf-8')).group(1)))

if argv[-1] == "--requires":
    print(dumps(requirements))
    exit()


setup(
    name='{{cookiecutter.project_slug}}',
    version=version,
    packages=find_packages(exclude=['tests/*', 'floes/*']),
    author='{{cookiecutter.full_name}}',
    author_email='{{cookiecutter.email}}',
    description='{{cookiecutter.description}}',
    license='Other/Proprietary License',
    keywords='openeye cloud orion',
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: Beta',
        'Intended Audience :: Orion',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
    ]
)
