#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
SQL команды для модуля базы данных.
"""

GET_POSTGRES_VERSION = "SELECT version();"

CHECK_DATABASE_EXISTS = """
    SELECT EXISTS (
        SELECT FROM pg_database 
        WHERE datname = %s
    );
"""

GET_DATABASE_INFO = """
    SELECT datname, encoding, datcollate, datctype
    FROM pg_database 
    WHERE datname = %s;
"""

GET_TABLES_LIST = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
"""

GET_TABLE_COUNT = """
    SELECT COUNT(*) 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name = %s;
"""

GET_TABLE_COLUMNS = """
    SELECT column_name, data_type, is_nullable
    FROM information_schema.columns 
    WHERE table_schema = 'public' 
    AND table_name = %s
    ORDER BY ordinal_position;
"""

# SQL команды для init_db.py
CHECK_DATABASE_EXISTS_SIMPLE = "SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
CREATE_DATABASE_WITH_ENCODING = """
    CREATE DATABASE {db_name} 
    WITH ENCODING 'UTF8' 
    LC_COLLATE='ru_RU.UTF-8' 
    LC_CTYPE='ru_RU.UTF-8' 
    TEMPLATE=template0
"""
