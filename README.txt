.. image:: https://github.com/IMIO/communesplone.layout/actions/workflows/main.yml/badge.svg
    :target: https://github.com/IMIO/communesplone.layout/actions/workflows/main.yml
.. image:: https://coveralls.io/repos/github/IMIO/communesplone.layout/badge.svg
    :target: https://coveralls.io/github/IMIO/communesplone.layout

Introduction
============

This product is dedicated to override default plone layout.

Plone 6.2 (Classic UI), Python 3.10+. Plone 4 versions: 4.3.15.1 and older.

default profile
===============
Installs a browser layer: the login form (``@@login``, ``@@login_form``) shows a maintenance message
instead of the form when the ``source_users`` authentication plugin is deactivated.
The ``uninstall`` profile removes the browser layer.

simplify profile
================
Set site permissions only for managers (sharing, display menu, constrain types, ...)
and creates the ``full-layout`` group (members: Administrators, Site Administrators).
Adds the ``communesplone-layout-simplify`` CSS bundle for the authenticated users that are not Manager
nor in the ``full-layout`` group: it hides the Actions menu, the workflow "Advanced..." item,
the edit-form tabs but the first one and the versioning comment.
