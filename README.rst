OpenEye Cube/Floe Package CookieCutter Template
===============================================

A `Cookiecutter`_ template for Orion packages containing Cubes and Floes.

Features
--------
* Sets up skeleton of an Orion package containing Cubes and Floes
* simple example Cube and Floe
* Testing setup using `PyTest`_ including working test for the example cube
* Automatic documentation generation (using `Sphinx`_ ) for cubes and floes
* Commands for running tests, building docs, and packaging using `Invoke`_
* Version configuration via storing the version only in the module's ``__init__.py`` file


Requirements
------------
* Python 3.5 or higher. We recommend starting with a clean `conda`_ environment.

* `Cookiecutter`_

* Access to OpenEye’s Python package server, `Magpie`_. If you are a licensed Orion user and don't have access, please contact `OpenEye Support`_. Follow the instructions there to configure access to Orion python packages via your ``pip.conf`` file.


Setup
-----

1. `Install cookiecutter <https://cookiecutter.readthedocs.io/en/latest/installation.html>`_, usually via running ``pip install cookiecutter``

2. run ``cookiecutter  gh:oess/cookiecutter-orion-package``

    *Note:* running cookiecutter directly against the GitHub repository requires ``git`` to be locally installed. To install without requiring ``git``, download the ZIP file from `GitHub <https://github.com/oess/cookiecutter-orion-package>`_ and run  ``cookiecutter cookiecutter-orion-package-master.zip``

3. After ``cookiecutter`` setup is completed run the following command to install all requirements and development requirements:

::

    pip install -r requirements.txt



Commands
--------


Once all dependencies are installed, you should be able to use invoke to build a version of the package for upload to Orion (the tar.gz will be in the dist directory):

::

    invoke package

Documentation can be built via the following command:

::

    invoke docs

A local webserver for the docs can be launched on port 8000 as follows:

::

    invoke serve-docs

Tests are set up for each of the floes included, they can be run locally:

::

    invoke test

To clean up generated documentation and packaging files, run:

::

    invoke clean

You can also selectively clean only documentation files as follows:

::

    invoke clean-docs




Output Skeleton
---------------

The following directory structure will be created by the ``cookiecutter``, the items marked in ``{{ }}`` will be replaced by your choices
upon completion::

    {{cookiecutter.project_slug}}/              <-- Top directory for your Project.
    ├── MANIFEST.in
    ├── README.md                               <-- README with your Project Name and description.
    ├── docs                                    <-- Docs subdirectory set up for automatic documentation of cubes and floes.
    │   ├── Makefile
    │   ├── make.bat
    │   └── source
    │       ├── _static
    │       ├── _templates
    │       ├── conf.py
    │       └── index.rst
    ├── floes                                   <-- Subdirectory where all floes should be placed.
    │   └── myfloe.py                           <-- An example floe.
    ├── manifest.json                           <-- Manifest for Orion.
    ├── requirements_dev.txt                    <-- Requirements file for development of this package.
    ├── setup.py                                <-- Python file for creating a python package
    ├── tasks.py                                <-- Python file with defined tasks for building docs, running tests, and building the package.
    ├── tests                                   <-- Subdirectory for testing of cubes and floes.
    │   ├── floe_tests                          <-- Subdirectory for floe tests
    │   │   └── test_myfloe.py                  <-- Example floe test to run locally or in Orion
    │   ├── test_data
    │   │   └── 10.ism
    │   └── test_mycube.py                      <-- An example unit test for the included cube.
    └── {{cookiecutter.module_name}}            <-- Subdirectory of the package for the python module. All cubes should go in here.
        ├── __init__.py
        └── mycube.py                           <-- An example cube.

..



.. _Cookiecutter: https://cookiecutter.readthedocs.io/
.. _PyTest: https://docs.pytest.org/
.. _Sphinx: http://www.sphinx-doc.org/
.. _Invoke: http://www.pyinvoke.org/
.. _conda: https://conda.io/docs/user-guide/overview.html
.. _magpie: https://magpie.eyesopen.com
.. _OpenEye Support: mailto:support%40eyesopen.com
