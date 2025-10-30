#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from pathlib import Path

import click
from sqlalchemy import text

from machine_tools.app.config import save_setting, show_settings, check_file_settings, create_env_file
from machine_tools.app.checks import check_connection as check_db_connection
from machine_tools.app.checks import (
    check_database_exists,
    check_tables_exist,
)
from machine_tools.app.constants import HELP_CONNECTION, HELP_DATABASE, HELP_TABLES
from machine_tools.app.db.init_db import init_db_from_csv
from machine_tools.app.db.delete_db import delete_database
from machine_tools.app.db.session_manager import session_manager
from machine_tools.version import __version__


@click.group()
def main():
    """Machine Tools CLI"""
    pass


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def init(ctx, verbose):
    """Инициализирует базу данных"""
    __ensure_settings_configured(ctx, verbose)
    init_db_from_csv()


@main.command(name="drop-db")
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def drop_db(ctx, verbose):
    """Удаляет базу данных machine_tools"""
    __ensure_settings_configured(ctx, verbose)
    try:
        success = delete_database()
        if success:
            click.echo("[OK] База данных удалена")
        else:
            click.echo("[ERROR] Не удалось удалить базу данных", err=True)
    except Exception as e:
        click.echo(f"[ERROR] Ошибка при удалении базы данных: {e}", err=True)



def __ensure_settings_configured(ctx, verbose):
    success = check_file_settings()
    if not success:
        click.echo("Перед началом работы необходимо создать нового пользователя.")
        ctx.invoke(setup_db_connection, verbose=verbose)


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def setup_db_connection(ctx, verbose):
    """Создает нового пользователя для работы с базой"""
    host = click.prompt("Хост PostgreSQL", default="localhost")
    port = click.prompt("Порт PostgreSQL", default=5432, type=int)
    user = click.prompt("Пользователь PostgreSQL")
    password = click.prompt("Пароль PostgreSQL", hide_input=True)

    try:
        create_env_file()
        save_setting('POSTGRES_HOST', host)
        save_setting('POSTGRES_PORT', str(port))
        save_setting('POSTGRES_USER', user)
        save_setting('POSTGRES_PASSWORD', password)

        click.echo("Проверка подключения с текущими настройками:")

        success = ctx.invoke(check_connection, verbose=verbose)
        if success:
            click.echo("Подключение установлено успешно.")
        else:
            click.echo("Ошибка подключения к PostgreSQL.")
            if click.confirm("Хотите попробовать другие настройки?"):
                ctx.invoke(setup_db_connection, verbose=verbose)

    except Exception as e:
        click.echo(f"Ошибка при сохранении настроек: {e}")


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def status(ctx, verbose):
    """Показать общий статус системы"""
    __ensure_settings_configured(ctx, verbose)
    click.echo("Проверка статуса системы Machine Tools...")
    click.echo()

    click.echo("1. Проверка подключения к PostgreSQL:")
    connection_success = ctx.invoke(check_connection, verbose=verbose)
    if not connection_success:
        return
    click.echo()

    click.echo("2. Проверка базы данных:")
    db_success = ctx.invoke(check_database, verbose=verbose)
    if not db_success:
        return
    click.echo()

    click.echo("3. Проверка таблиц:")
    ctx.invoke(check_tables, verbose=verbose)
    click.echo()

    click.echo("Проверка статуса завершена!")


@main.command()
@click.pass_context
def version(ctx):
    """Показать версию Machine Tools"""
    __ensure_settings_configured(ctx, False)

    try:
        click.echo(f"Machine Tools версия: {__version__}")
    except ImportError:
        click.echo("Machine Tools версия: неизвестна")


@main.command()
@click.option('--limit', '-l', default=10, type=int, help='Количество строк для отображения (по умолчанию: 10)')
@click.pass_context
def show_machines(ctx, limit):
    """Показать станки из базы данных"""
    __ensure_settings_configured(ctx, False)

    try:
        with session_manager.engine.connect() as connection:
            result = connection.execute(
                text(
                    f"SELECT id, name, \"group\", type, power, efficiency, accuracy, automation FROM machine_tools ORDER BY id LIMIT {limit}"
                )
            )
            columns = result.keys()
            header = " | ".join(columns)
            click.echo(header)
            click.echo("-" * len(header))
            for row in result:
                row_str = " | ".join(str(value) if value is not None else "NULL" for value in row)
                click.echo(row_str)

    except Exception as e:
        click.echo(f"{click.style('[ERROR]', fg='red')} Ошибка при получении данных о станках: {e}", err=True)


@main.command()
@click.option('--limit', '-l', default=10, type=int, help='Количество строк для отображения (по умолчанию: 10)')
@click.pass_context
def show_technical_requirements(ctx, limit):
    """Показать технические требования из базы данных"""
    __ensure_settings_configured(ctx, False)

    try:
        with session_manager.engine.connect() as connection:
            result = connection.execute(
                text(f"SELECT id, machine_name, requirement, value FROM technical_requirements LIMIT {limit}")
            )
            columns = result.keys()
            header = " | ".join(columns)
            click.echo(header)
            click.echo("-" * len(header))
            for row in result:
                row_str = " | ".join(str(value) if value is not None else "NULL" for value in row)
                click.echo(row_str)

    except Exception as e:
        click.echo(f"{click.style('[ERROR]', fg='red')} Ошибка при получении технических требований: {e}", err=True)


@main.group()
def config():
    """Управление настройками подключения к базе данных"""
    pass


@config.command()
@click.pass_context
def show(ctx):
    """Показать текущие настройки подключения к базе данных"""
    __ensure_settings_configured(ctx, False)

    show_settings()


@config.command()
@click.option('--host', prompt='Хост', default='localhost', help='Хост PostgreSQL')
@click.option('--port', prompt='Порт', default=5432, type=int, help='Порт PostgreSQL')
@click.option('--user', prompt='Пользователь', default='local_user', help='Имя пользователя PostgreSQL')
@click.option('--password', prompt='Пароль', hide_input=True, help='Пароль PostgreSQL')
@click.pass_context
def set(ctx, host, port, user, password):
    """Настроить параметры подключения к базе данных"""
    __ensure_settings_configured(ctx, False)

    try:
        save_setting('POSTGRES_HOST', host)
        save_setting('POSTGRES_PORT', str(port))
        save_setting('POSTGRES_USER', user)
        save_setting('POSTGRES_PASSWORD', password)
        click.echo("[OK] Настройки подключения сохранены успешно!")
        click.echo(f"Файл настроек: {Path(__file__).parent.parent / 'settings' / 'machine_tools.env'}")

    except Exception as e:
        click.echo(f"[ERROR] Ошибка при сохранении настроек: {e}", err=True)


@config.command()
@click.option('--host', prompt='Хост', help='Хост PostgreSQL')
@click.pass_context
def set_host(ctx, host):
    """Настроить только хост PostgreSQL"""
    __ensure_settings_configured(ctx, False)

    try:
        save_setting('POSTGRES_HOST', host)
        click.echo(f"[OK] Хост установлен: {host}")
    except Exception as e:
        click.echo(f"[ERROR] Ошибка при установке хоста: {e}", err=True)


@config.command()
@click.option('--port', prompt='Порт', type=int, help='Порт PostgreSQL')
@click.pass_context
def set_port(ctx, port):
    """Настроить только порт PostgreSQL"""
    __ensure_settings_configured(ctx, False)

    try:
        save_setting('POSTGRES_PORT', str(port))
        click.echo(f"[OK] Порт установлен: {port}")
    except Exception as e:
        click.echo(f"[ERROR] Ошибка при установке порта: {e}", err=True)


@config.command()
@click.option('--user', prompt='Пользователь', help='Имя пользователя PostgreSQL')
@click.pass_context
def set_user(ctx, user):
    """Настроить только пользователя PostgreSQL"""
    __ensure_settings_configured(ctx, False)

    try:
        save_setting('POSTGRES_USER', user)
        click.echo(f"[OK] Пользователь установлен: {user}")
    except Exception as e:
        click.echo(f"[ERROR] Ошибка при установке пользователя: {e}", err=True)


@config.command()
@click.option('--password', prompt='Пароль', hide_input=True, help='Пароль PostgreSQL')
@click.pass_context
def set_password(ctx, password):
    """Настроить только пароль PostgreSQL"""
    __ensure_settings_configured(ctx, False)

    try:
        save_setting('POSTGRES_PASSWORD', password)
        click.echo("[OK] Пароль установлен")
    except Exception as e:
        click.echo(f"[ERROR] Ошибка при установке пароля: {e}", err=True)


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def check_connection(ctx, verbose):
    """Проверить подключение к базе данных"""
    __ensure_settings_configured(ctx, verbose)

    success, message = check_db_connection()

    if success:
        click.echo(f"Проверка подключения к PostgreSQL...")
        click.echo(message)
        click.echo(f"{click.style('[OK]', fg='green')} Подключение установлено успешно!")
    else:
        click.echo(f"{click.style('[ERROR]', fg='red')} Ошибка подключения к PostgreSQL!")
        if verbose:
            click.echo(f"Детали ошибки: {message}")
        click.echo(HELP_CONNECTION)
    return success


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def check_database(ctx, verbose):
    """Проверить существование базы данных machine_tools"""
    __ensure_settings_configured(ctx, verbose)

    success, error_msg, db_info = check_database_exists()

    if success:
        click.echo(f"Проверка базы данных...")
        click.echo(f"  База данных: {click.style('[OK]', fg='green')}")

        if db_info:
            click.echo(f"    - Имя: {db_info['name']}")
            click.echo(f"    - Кодировка: {db_info['encoding']}")
            click.echo(f"    - Collate: {db_info['collate']}")
            click.echo(f"    - Ctype: {db_info['ctype']}")

        click.echo(f"\n{click.style('[OK]', fg='green')} Проверка базы данных завершена!")
    else:
        click.echo(f"Проверка базы данных...")
        click.echo(f"  База данных: {click.style('[MISSING]', fg='yellow')}")
        if verbose:
            click.echo(f"    {error_msg}")
        click.echo(HELP_DATABASE)
    return success


@main.command()
@click.option('--verbose', '-v', is_flag=False, help='Показать детали ошибки')
@click.pass_context
def check_tables(ctx, verbose):
    """Проверить существование таблиц в базе данных"""
    __ensure_settings_configured(ctx, verbose)

    success, error_msg, tables = check_tables_exist()

    if success:
        click.echo(f"Проверка таблиц...")
        click.echo(f"  Таблицы: {click.style('[OK]', fg='green')}")

        if tables:
            click.echo(f"    Найдено таблиц: {len(tables)}")
            for table in tables:
                click.echo(f"    - {table}")
        else:
            click.echo(f"    Таблицы не найдены")

        click.echo(f"\n{click.style('[OK]', fg='green')} Проверка таблиц завершена!")
    else:
        click.echo(f"Проверка таблиц...")
        click.echo(f"  Таблицы: {click.style('[ERROR]', fg='red')}")
        if verbose:
            click.echo(f"    {error_msg}")
        click.echo(HELP_TABLES)
    return success


if __name__ == "__main__":
    main()
