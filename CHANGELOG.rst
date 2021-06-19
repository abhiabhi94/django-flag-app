Changelog
=========


`v1.2.0 <https://github.com/abhiabhi94/django-flag-app/tree/HEAD>`__
------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.2.0...1.1.1>`__


**Features**

- Add link to the related content object in the admin.

- Dropped support for django ``2.1`` (this version is not LTS. See `supported django versions`_ for more information on this).

.. _`supported django versions`: https://www.djangoproject.com/download/#supported-versions

`v1.1.1 <https://github.com/abhiabhi94/django-flag-app/tree/HEAD>`__
------------------------------------------------------------------------

`Full
Changelog <https://github.com/abhiabhi94/django-flag-app/compare/v1.1.0...HEAD>`__

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
