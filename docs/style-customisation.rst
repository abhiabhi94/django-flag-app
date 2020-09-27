Style Customization
===================

The flag app has been built in a way that you can customise its look and feel completely. Most of the styles can be customised through HTML classes.

In case, you feel there is some customisation that can be added, feel free to open an `issue`_.

.. _issue: https://github.com/abhiabhi94/django-flag-app/issues

The template structure of the flag app looks something like this:

    .. code:: sh

        ├── templates
        └── flag
            ├── flag_form.html
            └── flag_icon.html

Overriding templates
`````````````````````

To customise a template,

    * Create ``flag`` folder inside templates directory.

    * Inside it, create a new template file, giving it the same name as that of the default template that needs to be overridden.

For example, to override the HTML classes of ``submit button``

create ``templates/flag/flag_form.html`` (assuming all your templates are placed under the directory ``templates``)

    .. code:: jinja

        {% extends "flag/flag_form.html" %}

        {% block cls_flag_modal_submit %}
        my-class
        {% endblock cls_flag_modal_submit %}


Blocks
------

Please refer to this table when using blocks to customise HTML classes

+----------------------------------------+-----------------------------------------------------------+--------------+
| Block                                  | Use                                                       | HTML element |
+========================================+===========================================================+==============+
| ``{% block cls_flag %}``               | complete flag element                                     | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{%  block cls_flag_icon_img %}``     | flag icon image element                                   | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal %}``         | modal that appears when flagging                          | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_content %}`` | modal content                                             | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_close %}``   | the cross icon(close button) inside the modal             | ``span``     |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_form_div %}``| the ``div`` element containing the modal form             | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_form %}``    | modal form element                                        | ``form``     |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_title %}``   | the text containing modal title                           | ``div``      |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_reasons %}`` | the element that displays reasons for flagging            | ``tr``       |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_reason %}``  | individual reasons                                        | ``input``    |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_info %}``    | text box which appears when ``Somthing else`` is selected | ``textarea`` |
+----------------------------------------+-----------------------------------------------------------+--------------+
| ``{% block cls_flag_modal_submit %}``  | submit button inside the modal                            | ``input``    |
+----------------------------------------+-----------------------------------------------------------+--------------+


Flag Icon
---------

To change the flag icon, just override the template ``flag_icon.html`` as explained above.
Make sure that you add the property ``class="flag-icon {% if has_flagged %}user-has-flagged{% else %}user-has-not-flagged{% endif %}"`` to your HTML element. These classes are used by ``javascript`` files.

For other customisation, please refer to the :ref:`Blocks` above
