Angular Gettext Babel
=====================

A babel extractor extension for angular

This is a very simple extractor that looks for Jed usages (gettext, pgettext & ngettext) within html attributes and tag contents.
Forked from neillc/angular-gettext-babel

Usage:

Create a `babel.cfg`  config file

    [angular: **.html]
    encoding = utf-8

    [extractors]
    angular = angular_gettext_babel.extract:extract_angular

Then run with:

    pybabel extract -F babel.cfg  static -o locale/eb_GB/LC_MESSAGES/django_angular.po
