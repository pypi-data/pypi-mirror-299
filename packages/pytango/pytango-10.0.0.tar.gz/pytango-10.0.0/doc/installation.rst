.. highlight:: python
   :linenothreshold: 10

.. _installation:

Installation
============

.. contents:: Contents
   :depth: 2
   :local:
   :backlinks: none

Minimum setup
-------------

To explore PyTango you should have a running Tango system. If you are working in
a facility/institute that uses Tango, this has probably already been prepared
for you. You need to ask your facility/institute Tango contact for the
:envvar:`TANGO_HOST` variable where Tango system is running.

If you are working on an isolated machine you may want to create your own Tango
system (see `How to try Tango <https://tango-controls.readthedocs.io/en/latest/tutorials-and-howtos/how-tos/how-to-try-tango.html>`_).
This is not a pre-requisite for installing PyTango, but will be useful when you want to start testing.

Installation of PyTango
-----------------------

First you should try the easy installation way:  pre-compiled packages.
But if that doesn't work, or you need to compile from source, see the next section.

PyPI (Linux, Windows)
~~~~~~~~~~~~~~~~~~~~~

You can install the latest version from `PyPI`_.

PyTango has binary wheels for common platforms, so no compilation or dependencies required.

Install PyTango with pip:

.. sourcecode:: console

    $ python -m pip install pytango

If this step downloads a ``.tar.gz`` file instead of a ``.whl`` file, then we don't have a binary package
for your platform.  Try Conda.

If you are going to utilize the gevent green mode of PyTango it is recommended to have a recent version of gevent.
You can force gevent installation with the "gevent" keyword:

.. sourcecode:: console

    $ python -m pip install pytango[gevent]

Conda (Linux, Windows, MacOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install the latest version from `Conda-forge`_.

Conda-forge provides binary wheels for different platforms, compared to `PyPI`_.
MacOS binaries are available since version 9.4.0.

If you don't already have conda, try the `Miniforge3`_ installer (an alternative installer to `Miniconda`_).

To install PyTango in a new conda environment (you can choose a different version of Python):

.. sourcecode:: console

    $ conda create --channel conda-forge --name pytango-env python=3.11 pytango
    $ conda activate pytango-env

Other useful packages on conda-forge include:  ``tango-test``, ``jive`` and ``tango-database``.

Linux
~~~~~

PyTango is available on linux as an official debian/ubuntu package (however, this may not be the latest release):

For Python 3:

.. sourcecode:: console

    $ sudo apt-get install python3-tango

RPM packages are also available for RHEL & CentOS:

.. hlist::
   :columns: 2

   * `CentOS 6 32bits <http://pubrepo.maxiv.lu.se/rpm/el6/x86_64/>`_
   * `CentOS 6 64bits <http://pubrepo.maxiv.lu.se/rpm/el6/x86_64/>`_
   * `CentOS 7 64bits <http://pubrepo.maxiv.lu.se/rpm/el7/x86_64/>`_
   * `Fedora 23 32bits <http://pubrepo.maxiv.lu.se/rpm/fc23/i/386/>`_
   * `Fedora 23 64bits <http://pubrepo.maxiv.lu.se/rpm/fc23/x86_64/>`_

Windows
~~~~~~~

First, make sure `Python`_  is installed.  Then follow the same instructions as for `PyPI`_ above.
There are binary wheels for some Windows platforms available.

.. _build-from-source:

Building and installing from source
-----------------------------------

This is the more complicated option, as you need to have all the correct dependencies and build tools
installed.  It is possible to build in Conda environments on Linux, macOS and Windows.  It is also possible
to build natively on those operating system.  Conda is the recommended option for simplicity.  For details see the file
`BUILD.md <https://gitlab.com/tango-controls/pytango/-/blob/develop/BUILD.md>`_ in the root of the
source repository.

Basic installation check
------------------------

To test the installation, import ``tango`` and check ``tango.Release.version``:

.. sourcecode:: console

    $ cd  # move to a folder that doesn't contain the source code, if you built it
    $ python -c "import tango; print(tango.Release.version)"
    9.4.0

Next steps: Check out the :ref:`tutorial`.
