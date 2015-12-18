respawn tests
============

Test scripts are named ``test_xxx.py`` and use the ``py.test`` module.

Dependencies
-----------

Install::

    pip install pytest coverage pytest-cov


Execution
---------

**If respawn has been built in-place**

To run an individual test::

    python respawn/test_image.py

Run all the tests from the root of the respawn source distribution::

    py.test --cov=respawn/

Or with coverage::

    py.test --cov=respawn/ --cov-report term

