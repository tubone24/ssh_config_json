===============
SSH Config JSON
===============

``SSH Config JSON`` is dumping JSON for your ssh config include IdentityFiles and restoring those.

------

Getting Started
===============

``SSH Config JSON`` is ``The Python Package Index(Pypi)``, so that you can use ``pip`` installer.

pip installer
----------------------

.. code-block:: bash

   $ pip install xxxxxx

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
     scj dump <file> [-c|--config=<config>] [-i|--identityFile]
     scj restore <file> [-c|--config=<config>] [-i|--identityFile]

   Options:
     dump                       : dump SSH Config file to JSON
     restore                    : Restore SSH Config file from JSON
     <file>                     : Dumped json file
     -h, --help                 : Help
     -v, --version              : Show version
     -c, --config=<config>      : Specific SSH Config file path [default: ~/.ssh/config]
     -i, --identityFile         : Include IdentityFiles

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

Using pytest, if you want to do integrated tests with mark "--it"

.. code-block:: bash

   $ pytest --it

With tox
--------

With tox, you can test multiple python version.(only python 3.6, 3.7, 3.8)

.. code-block:: bash

   $ tox

Licence
=======

This software is released under the MIT License, see LICENSE.