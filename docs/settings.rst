Settings
========

django-flag-app has a few configuration options that allow you to customize it.

FLAG_ALLOWED
``````````````
The number of flags allowed before a content is set as flagged. Defaults to ``10``.


FLAG_REASONS
`````````````
The reasons for which a content can be flagged. Users will have a choose one of these before they flag a content. This a list of tuples. Defaults to:

.. code:: python

    from django.utils.translation import gettext_lazy as _

    [
        (1, _('Spam | Exists only to promote a service')),
        (2, _('Abusive | Intended at promoting hatred')),
    ]

Remember that ``(100, _('Something else')`` will always be appended to this list.

