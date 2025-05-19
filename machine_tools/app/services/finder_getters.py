#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from machine_tools.app.containers import FinderContainer


def get_finder_with_list_names():
    container = FinderContainer()
    return container.finder_with_list_names()


def get_finder_with_list_info():
    container = FinderContainer()
    return container.finder_with_list_info()


def get_finder_with_dict_names():
    container = FinderContainer()
    return container.finder_with_dict_names()


def get_finder_with_dict_info():
    container = FinderContainer()
    return container.finder_with_dict_info()


def get_finder_with_indexed_names():
    container = FinderContainer()
    return container.finder_with_indexed_names()


def get_finder_with_indexed_info():
    container = FinderContainer()
    return container.finder_with_indexed_info()
