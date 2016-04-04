#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base visitor class. Visitor object carries information about the databases,
tables withing databases and columns within tables that it is allowed to
access. It also has a dictionary of allowed keywords and function as well as
permission flag for using the wildcard operator. The class implements a
method `format` which formats the the query as an output.

"""

from __future__ import print_function

__all__ = ["Visitor"]


class Visitor(object):
    """
    ...

    """
    def __init__(self):
        self._columns = []
        self._keywords = []

    @property
    def columns(self):
        return self._columns

    def set_columns(self, array):
        self._columns = array 

    @property
    def keywords(self):
        return self._keywords

    def set_keywords(self, array):
        self._keywords = array 
