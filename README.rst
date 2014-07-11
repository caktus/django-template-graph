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

Configuration
------------------------------------

The default behavior of django-template-graph is to generate the graph data for
the project its in on each request. This is sufficient for medium to small size
projects and takes at most one or two seconds. For large projects, the
performance might be unacceptable. For these, a flat file can pre-generated and
served to avoid the wait time. To configure a project this way, set the
TEMPLATE_GRAPH_PATH setting to a path that should store this file. The file
will be named template_graph.json. If this is done, it is a good idea to add
this file to .gitignore or similar in the same way that files like ctags are
often handled.

With TEMPLATE_GRAPH_PATH set, likely to a root project directory, the view will
automatically generate this file if it is not present. To regenerate it run::

django-admin.py template_graph_gen

To use a per request behavior, simply do not set TEMPLATE_GRAPH_PATH or set it
to None

Running the Tests
------------------------------------

You can run the tests with via::

    python setup.py test

or::

    python runtests.py
