Django Template Graph
========================

Welcome to the documentation for django-template-graph

Overview
------------------------------------

django-template-graph is debugging/data-visualization tool for front-end
developers working with Django that charts template hierarchies (extends tags)
and includes.

At least at the moment, only extend tags and include tags that use strings
directly are considered. As a result, include tags or tags that use a variable
are skipped.

The project is in a very early experimental state but should be functional
soon.

Requirements
------------------------------------
The only requirement for this project is Django. The project was built against
Django1.6. Other versions likely work but are yet to be tested and officially
supported.

Installation
------------------------------------

django-template-graph is not available on Pypi yet. The easiest way to install
it is with a pip source checkout from github

Setup
------------------------------------
Add 'template_graph' to the INSTALLED_APPS iterable in your settings file. For example::

    INSTALLED_APPS = (
        ...
        'template_graph',
        ...
    )

Add a template_graph entry to your root urls.py::

    url(r'^template-graph/$', include('template_graph.urls')),

Ideally, you wrap the above url conditionally on ``settings.DEBUG = True`` to
enforce that it is available in development environments only

Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
