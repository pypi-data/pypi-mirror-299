Django UI Forms
===============

A Django reusable app to extend forms and provide UI with templates available for Bootstrap and Tailwind CSS.

Features
--------

- Custom form handling with Bootstrap and Tailwind CSS support.
- Easy to use and integrate into existing Django projects.
- Flexible and reusable components for better form management.

Installation
------------

You can install this package via pip:

.. code-block:: bash

    pip install django-ui-forms

Usage
-----

To use this package in your Django project, follow these steps:

1. Add `django_ui_forms` to your `INSTALLED_APPS` in your Django settings:

   .. code-block:: python

       INSTALLED_APPS = [
           ...
           'django_ui_forms',
       ]

2. Create your forms by extending `BootstrapBaseUiForms` or `TailwindBaseUiForms`:

   .. code-block:: python

   from django import forms
   from django_ui_forms.forms import BootstrapBaseUiForms, TailwindBaseUiForms

   class MyForm(BootstrapBaseUiForms, forms.Form):
       my_field = forms.CharField(label='My Field')

   class MyModelForm(TailwindBaseUiForms, forms.ModelForm):
       class Meta:
           model = MyModel
           fields = '__all__'

3. Use the forms in your views and templates.

Example
-------

See the `examples/` directory for a complete example of how to use this package in a Django project.

Running Tests
-------------

To run the tests, you can use the following command:

.. code-block:: bash

    python -m unittest discover tests

Contributing
------------

Contributions are welcome! Please submit a pull request or open an issue.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
