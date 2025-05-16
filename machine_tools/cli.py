#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import click

from machine_tools.app.db.init_db import init_db_from_csv


@click.group()
def main():
    """Machine Tools CLI"""
    pass


@main.command()
def init():
    """Инициализирует базу данных"""
    init_db_from_csv()


if __name__ == "__main__":
    main()
