Changelog
=========
`v2.0.0 <https://github.com/abhiabhi94/django-flag-app/tree/v2.0.0>`__

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.3.0...v2.0.0>`__

We sincerely apologize for the long delay since our last release. This major version brings
the package up to date with the latest Django and Python versions while removing support
for end-of-life versions.

**Breaking Changes**

- **DROPPED** support for Python ``3.6``, ``3.7``, ``3.8``, and ``3.9`` - these versions have reached end-of-life
- **DROPPED** support for Django ``2.2``, ``3.0``, ``3.1``, and ``3.2`` - these versions are no longer supported by Django
- Minimum Python version is now ``3.10``
- Minimum Django version is now ``4.2`` (LTS)

**Features**

- **NEW** support for Python ``3.11``, ``3.12``, and ``3.13``
- **NEW** support for Django ``4.2`` (LTS), ``5.0``, ``5.1``, and ``5.2``
- Removed deprecated Django features and compatibility code for better performance

**Bug Fixes**

- Fix issues with flag form when selecting "something else" reason - requests weren't being sent and other reasons couldn't be selected in the same session
- Fix documentation build issues with sphinx-rtd-theme dependency

**Chores**

- Updated development tooling (switched from flake8/isort to ruff)
- Migrated from ``setup.py`` to ``pyproject.toml`` for modern packaging

`v1.3.0 <https://github.com/abhiabhi94/django-flag-app/tree/v1.3.0>`__
----------------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.2.1...v1.3.0>`__

**Features**

- Confirm support for python ``3.10``.

`v1.2.1 <https://github.com/abhiabhi94/django-flag-app/tree/v1.2.1>`__
----------------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.2.0...v1.2.1>`__

**Bug Fixes**

- Fix links for redirecting unauthenticated from flag form to login page.


`v1.2.0 <https://github.com/abhiabhi94/django-flag-app/tree/v1.2.0>`__ (2021-06-19)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.1.1...v1.2.0>`__


**Features**

- Add link to the related content object in the admin.

- Dropped support for django ``2.1`` (this version is not LTS. See `supported django versions`_ for more information on this).

.. _`supported django versions`: https://www.djangoproject.com/download/#supported-versions

`v1.1.1 <https://github.com/abhiabhi94/django-flag-app/tree/v1.1.1>`__ (2021-05-01)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.1.0...v1.1.1>`__

**Bug fixes**

- Handle Warning for ``default_app_config`` in django >=3.2.

**Features**

- Move metadata from ``setup.py`` to ``setup.cfg``.
    - this means the ``__version__`` string is no longer available. To use the installed versions, you may use ``importlib.metadata.version['django_flag_app']``.

`v1.1.0 <https://github.com/abhiabhi94/django-flag-app/tree/v1.1.0>`__ (2021-04-18)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.0.1...v1.1.0>`__

**Features**

-  Add support for python3.9 and django3.2

`v1.0.1 <https://github.com/abhiabhi94/django-flag-app/tree/v1.0.1>`__ (2021-03-11)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.0.0...v1.0.1>`__

**Bug fixes**

- Circular import caused by the use of ``get_user_model`` at modular level in ``flag.managers``.

- Version number according to PEP440

`v1.0.0 <https://github.com/abhiabhi94/django-flag-app/tree/v1.0.0>`__ (2020-11-17)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v0.1.1...v1.0.0>`__

**Bug fixes**

- Fix API response

**Features**

- Add app settings

`v0.1.1 <https://github.com/abhiabhi94/django-flag-app/tree/v0.1.1>`__ (2020-10-22)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v0.1.0...v0.1.1>`__

**Bug fixes**

- Fix icon title when flagging/unflagging

- Fix template for unauthenticated users

`v0.1.0 <https://github.com/abhiabhi94/django-flag-app/tree/v0.1.0>`__ (2020-09-28)
-----------------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/47b8b136bd62b2c5a75d04ac76ca25f01e91b03e...v0.1.0>`__

- Release first version
