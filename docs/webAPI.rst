Web API
=======

django-flag-app uses `django-rest-framework`_ to expose a Web API that provides developers with access to the same functionality offered through the web user interface.

.. _django-rest-framework: https://www.django-rest-framework.org/

The available actions with permitted user are as follows:

    * Flag content. (authenticated users)
    * Unflag content. (user who has previously flagged that content)

Setup
-----

To integrate the flag API into your app, just follow the instructions as mentioned :ref:`Usage`.

API Actions
-----------

All actions can only be performed by authenticated users. Authorization must be provided as a TOKEN or USERNAME:PASSWORD.
``POST`` is the allowed method for all requests.

All available actions are explained below:

Flag content
`````````````

This action can be performed by providing the URL with data queries related to the content type.

The request requires the following parameters:

- ``model_name``: is the model name of the content type that have flags associated with it.
- ``model_id``: is the id of an object of that model
- ``app_name``: is the name of the app that contains the model.
- ``reason``: number corresponding to the reason(e.g. 1, 2, 3).
- ``info``: '' (This is only required if the reason is ``100`` (``Something else``))


For example, to flag a content of second object (id=1) of a model (content type) called ``post`` inside the app(django app) ``post``.
You may do the following:

.. code:: sh

    $ curl -X POST -u USERNAME:PASSWORD -H "Content-Type: application/json" -d "{'app_name': 'post','model_name': 'post', 'model_id': 1,'reason': 1,'info': ''}" http://localhost:8000/api/flag/


Un-Flag Content
````````````````

To un-flag a **FLAGGED** content, set reason value to ``0`` or remove it from the request.

.. code:: sh

    $ curl -X POST -u USERNAME:PASSWORD -H "Content-Type: application/json" -d "{'app_name': 'post','model_name': 'post', 'model_id': 1}" http://localhost:8000/api/flag/


