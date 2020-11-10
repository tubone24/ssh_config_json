===============
SSH Config JSON
===============

``SSH Config JSON`` is dumping JSON for your ssh config include IdentityFiles and restoring those.

------

.. image:: http://img.shields.io/badge/license-MIT-blue.svg?style=flat
   :target: https://github.com/tubone24/ebook_homebrew/blob/master/LICENSE
   :alt: LICENSE

.. image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: http://makeapullrequest.com
   :alt: PR Welcomes

.. image:: https://github.com/tubone24/ssh_config_json/workflows/TestingPythonPackage/badge.svg
   :target: https://github.com/tubone24/ssh_config_json/actions?query=workflow%3ATestingPythonPackage
   :alt: GitHub Actions

.. image:: https://coveralls.io/repos/github/tubone24/ssh_config_json/badge.svg?branch=main
   :target: https://coveralls.io/github/tubone24/ssh_config_json?branch=main
   :alt: Coverage

.. image:: https://img.shields.io/pypi/dm/ssh-config-json.svg
   :target: https://pypi.org/project/ssh-config-json/
   :alt: PyPI downloads
   
.. image:: https://img.shields.io/pypi/v/ssh-config-json.svg
   :target: https://pypi.org/project/ssh-config-json/
   :alt: pip Version
   
.. image:: https://img.shields.io/pypi/pyversions/ssh-config-json.svg
   :target: https://pypi.org/project/ssh-config-json/
   :alt: Python Version
   
.. image:: https://img.shields.io/pypi/format/ssh-config-json.svg
   :target: https://pypi.org/project/ssh-config-json/
   :alt: pip Format

.. image:: https://readthedocs.org/projects/ssh-config-json/badge/?version=latest
   :target: https://ssh-config-json.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
 
 

``SSH Config JSON`` enables you to pack and restore your SSH Config and Private Key in JSON format,
allowing you to backup, put to CI and share with others in the project.

Features
========

* Dumping your SSH Config to JSON and restore it
* Packing up IdentityFiles with the JSON
* AES encrypting with the JSON to enable pushing and saving public GitHub Repository

Getting Started
===============

``SSH Config JSON`` uses ``The Python Package Index(Pypi)``, so that you can use ``pip`` installer.

pip installer
----------------------

.. code-block:: bash

   $ pip install ssh-config-json

Usage
=====

You can use global command ``scj`` .

Show help.

.. code-block:: bash

   $ scj -h
   SSH Config JSON
   Overview:
     Dump JSON for your ssh config include IdentityFiles and restore those.

   Usage:
     scj [-h|--help] [-v|--version]
     scj dump <file> [-c|--config=<config>] [-i|--identityFile]　[-e|--encrypt] [--key=<key>]
     scj restore <file> [-c|--config=<config>] [-i|--identityFile]　[-d|--decrypt=<key>]

   Options:
     dump                       : dump SSH Config file to JSON
     restore                    : Restore SSH Config file from JSON
     <file>                     : Dumped json file
     -h, --help                 : Help
     -v, --version              : Show version
     -c, --config=<config>      : Specific SSH Config file path [default: ~/.ssh/config]
     -i, --identityFile         : Include IdentityFiles
     -e, --encrypt              : Encrypt JSON dump with AES
     --key=<key>                : Set specify key string
     -d, --decrypt=<key>        : Decrypt JSON dump with AES

Ex1) Dump your SSH Config to JSON

.. code-block:: bash

   $ scj dump dump_config.json

Ex2) Dump your SSH Config to JSON with IdentityFiles

.. code-block:: bash

   $ scj dump dump_config.json -i

Ex3) Restore JSON to SSH Config

.. code-block:: bash

   $ scj restore dump_config.json

Ex4) Restore JSON to SSH Config with IdentityFiles

.. code-block:: bash

   $ scj restore dump_config.json -i

Ex5) Dump your SSH Config to JSON with AES Encrypt

.. code-block:: bash

   $ scj dump dump_config.json -i -e
   Encrypt key: 1mado1wmf9amsie0jvo0kfmai9cjasfv # <= This is the "Key"!!

Ex6) Decrypt it

.. code-block:: bash

   $ scj restore dump_config.json -i -d 1mado1wmf9amsie0jvo0kfmai9cjasfv

Testing
=======

Unit Test
---------

Using pytest, if you want to unit testing.

.. code-block:: bash

   $ pytest

If you want to get coverage report, run coverage and check the report.

.. code-block:: bash

   $ coverage run --source=ssh_config_json -m pytest
   $ coverage report -m

Integration Test
----------------

Using pytest, if you want to do integrated tests with mark "--it".

.. code-block:: bash

   $ pytest --it

With tox
--------

With tox, you can test multiple python version.(only python 3.6, 3.7, 3.8)

.. code-block:: bash

   $ tox

Documents
=========

The Document is `HERE <https://ssh-config-json.readthedocs.io/en/latest/>`_ written by mkdocs.

The PyPI page is `HERE <https://pypi.org/project/ssh-config-json/>`_ .

The GitHub page is `HERE <https://github.com/tubone24/ssh_config_json>`_ .

Licence
=======

This software is released under the MIT License, see LICENSE.

Change log
==========

Read the `GitHub Release Page <https://github.com/tubone24/ssh_config_json/releases>`_ !
