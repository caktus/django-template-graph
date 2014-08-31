Django Template Graph
========================

Welcome to the documentation for django-template-graph

Overview
------------------------------------

django-template-graph is debugging/data-visualization tool for front-end
developers working with Django that charts template hierarchies (extends tags)
and includes.

Include or extends tags that use a variable are displayed as "var:variable"
where variable is the variable used in the template.

Requirements
------------------------------------
The only requirement for this project is Django>=1.3.

Installation
------------------------------------

django-template-graph is not available on Pypi yet. The easiest way to install
it is with a pip source checkout from github.

Setup
------------------------------------
Add 'template_graph' to the INSTALLED_APPS iterable in your settings file. For
example::

    INSTALLED_APPS = (
        ...
        'template_graph',
        ...
    )

Add a template_graph entry to your root urls.py conditionally on
settings.DEBUG::

    from django.conf import settings
    from django.conf.urls import patterns, include, url

    urlpatterns = patterns(
        ...
    )
    if settings.DEBUG:
        urlpatterns += patterns(
            url(r'^template-graph/$', include('template_graph.urls')),
        )

Configuration
------------------------------------

The default behavior of django-template-graph is to generate the graph data for
each request. This is sufficient for medium to small size projects and takes at
most one or two seconds. For large projects, the performance might be
unacceptable. For these, a flat file can pre-generated and served to avoid the
wait time. To configure a project this way, set the TEMPLATE_GRAPH_PATH setting
to a path that should store this file. The file will be named
template_graph.json. It is a good idea to add this file to .gitignore or
similar in the same way that files like tags are often handled.

With TEMPLATE_GRAPH_PATH set, likely to a root project directory, the view will
automatically generate this file if it is not present. To regenerate it run::

    django-admin.py template_graph_gen

To use a per request behavior, simply do not set TEMPLATE_GRAPH_PATH or set it
to None

Running the Tests
------------------------------------

You can run the tests for this project with::

    python setup.py test

or::

    python runtests.py
