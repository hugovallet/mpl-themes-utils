Getting started
---------------

The codebase is built in Python 3.9.

Set up environment for development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The full environment for both usage and development can be set up by
running:

::

    pip install -r requirements.txt -r requirements.dev.txt
    pip install pre-commit
    pre-commit install

This provides all packages used in code and testing, as well as the
pre-commit git hooks used to apply basic quality checks during
commit/push.
