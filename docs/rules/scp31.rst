.. _scp31:

==================================
SCP31: Missing setting requirement
==================================

What it does
============

Reports setting names that belong to packages that are missing from your
:ref:`project requirements <requirements>`.

.. note::

   The package that your code base defines, i.e. the ``name`` of the
   ``[project]`` table of :file:`pyproject.toml`, also counts as required, so
   that you can lint the code base of a package.


Why is this bad?
================

Such settings are silently ignored.
