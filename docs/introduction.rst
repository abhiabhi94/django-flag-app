django-flag-app
===============

.. image:: https://travis-ci.org/abhiabhi94/django-flag-app.svg?branch=master
    :target: https://travis-ci.org/abhiabhi94/django-flag-app
    :alt: build

.. image:: https://coveralls.io/repos/github/abhiabhi94/django-flag-app/badge.svg
    :target: https://coveralls.io/github/abhiabhi94/django-flag-app
    :alt: coverage

.. image:: https://img.shields.io/pypi/pyversions/django-flag-app.svg
    :target: https://pypi.python.org/pypi/django-flag-app/
    :alt: python

.. image:: https://img.shields.io/pypi/djversions/django-flag-app.svg
    :target: https://pypi.python.org/pypi/django-flag-app/
    :alt: django

.. image:: https://readthedocs.org/projects/django-flag-app/badge/?version=latest
    :target: https://django-flag-app.readthedocs.io/?badge=latest
    :alt: docs

.. image:: https://img.shields.io/github/license/abhiabhi94/django-flag-app?color=gr
    :target: https://github.com/abhiabhi94/django-flag-app/blob/master/LICENSE
    :alt: licence

A pluggable django application that adds the ability for users to flag(or report) your models.

.. image:: ./_static/images/django-flag-app.gif
    :alt: flagging-process

Installation
------------

Install using ``pip``

.. code:: sh

    $ pip install django-flag-app

If you want, you may install it from the source, grab the source code and run ``setup.py``.

.. code:: sh

    $ git clone git://github.com/abhiabhi94/django-flag-app.git
    $ cd django-flag-app
    $ python setup.py install

Usage
-----

Add app
````````

To enable ``django_flag_app`` in your project you need to add it to ``INSTALLED_APPS`` in your projects ``settings.py`` file:

.. code:: python

    INSTALLED_APPS = (
        ...
        'flag',
        ...
    )

Add URL
````````

In your root ``urls.py``:

.. code:: python

    urlpatterns = patterns(
            path('admin/', admin.site.urls),
            path('flag/', include('flag.urls')),
            ...
            path('api/', include('flag.api.urls')),  # only required for API Framework
            ...
        )

Migrate
````````

Run the migrations to add the new models to your database:

.. code:: sh

    python manage.py migrate flag


Connect the flag model with the target model
`````````````````````````````````````````````

In ``models.py`` add the field **flags** as a ``GenericRelation`` field to the required model.

E.g. for a ``Post`` model, you may add the field as shown below:

.. code:: python

    from django.contrib.contenttypes.fields import GenericRelation

    from flag.models import Flag


    class Post(models.Model):
        user = models.ForeignKey(User)
        title = models.CharField(max_length=200)
        body = models.TextField()
        # the field name should be flags
        flags = GenericRelation(Flag)


Use template tag
`````````````````

If you want to use web API, this step is not required. See further instructions at :ref:`API Actions`.

``render_flag_form`` tag requires 2 required positional arguments:

    1. Instance of the targeted model.
    2. User object.

To render the ``flag`` form for a the instance ``post``, place this inside your detail view, perhaps in some template of the sort ``postdetail.html``.

.. code:: jinja

    {% render_flag_form post user %}


Contributing
------------

Please see the instructions at :ref:`Contributing to Django Flag App`.
