..
   Copyright CNRS/Inria/UCA
   Contributor(s): Eric Debreuve (since 2018)

   eric.debreuve@cnrs.fr

   This software is governed by the CeCILL  license under French law and
   abiding by the rules of distribution of free software.  You can  use,
   modify and/ or redistribute the software under the terms of the CeCILL
   license as circulated by CEA, CNRS and INRIA at the following URL
   "http://www.cecill.info".

   As a counterpart to the access to the source code and  rights to copy,
   modify and redistribute granted by the license, users are provided only
   with a limited warranty  and the software's author,  the holder of the
   economic rights,  and the successive licensors  have only  limited
   liability.

   In this respect, the user's attention is drawn to the risks associated
   with loading,  using,  modifying and/or developing or reproducing the
   software by the user in light of its specific status of free software,
   that may mean  that it is complicated to manipulate,  and  that  also
   therefore means  that it is reserved for developers  and  experienced
   professionals having in-depth computer knowledge. Users are therefore
   encouraged to load and test the software's suitability as regards their
   requirements in conditions enabling the security of their systems and/or
   data to be ensured and,  more generally, to use and operate it in the
   same conditions as regards security.

   The fact that you are presently reading this means that you have had
   knowledge of the CeCILL license and that you accept its terms.

.. |PROJECT_NAME|      replace:: SKLGraph
.. |SHORT_DESCRIPTION| replace:: SKeLeton Graph

.. |PYPI_NAME_LITERAL| replace:: ``skl-graph``
.. |PYPI_PROJECT_URL|  replace:: https://pypi.org/project/skl-graph/
.. _PYPI_PROJECT_URL:  https://pypi.org/project/skl-graph/

.. |DOCUMENTATION_URL| replace:: https://src.koda.cnrs.fr/eric.debreuve/sklgraph/-/wikis/home
.. _DOCUMENTATION_URL: https://src.koda.cnrs.fr/eric.debreuve/sklgraph/-/wikis/home



===================================
|PROJECT_NAME|: |SHORT_DESCRIPTION|
===================================



Installation
============

This project is published
on the `Python Package Index (PyPI) <https://pypi.org/>`_
at: |PYPI_PROJECT_URL|_.
It should be installable from Python distribution platforms or Integrated Development Environments (IDEs).
Otherwise, it can be installed from a command console:

- For all users, after acquiring administrative rights:
    - First installation: ``pip install`` |PYPI_NAME_LITERAL|
    - Installation update: ``pip install --upgrade`` |PYPI_NAME_LITERAL|
- For the current user (no administrative rights required):
    - First installation: ``pip install --user`` |PYPI_NAME_LITERAL|
    - Installation update: ``pip install --user --upgrade`` |PYPI_NAME_LITERAL|



Documentation
=============

SKLGraph Pipeline: 2-D/3-D Object Map -> Object Skeleton -> SKeLeton Graph -> Graph Features

The documentation is available at |DOCUMENTATION_URL|_.



Acknowledgments
===============

The project is developed with `PyCharm Community <https://www.jetbrains.com/pycharm/>`_.

The development relies on several open-source packages
(see ``install_requires`` in ``setup.py``, if present; otherwise ``import`` statements should be searched for).

The code is formatted by `Black <https://github.com/psf/black/>`_, *The Uncompromising Code Formatter*.

The imports are ordered by `isort <https://github.com/timothycrosley/isort/>`_... *your imports, so you don't have to*.
