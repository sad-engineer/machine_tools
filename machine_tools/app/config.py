#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Определяем пути к конфигурационным файлам
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "settings"
ENV_FILE = CONFIG_DIR / "machine_tools.env"

# Создаем директорию config, если её нет
CONFIG_DIR.mkdir(exist_ok=True)


def create_env_file() -> None:
    """Создать файл machine_tools.env с шаблоном настроек"""
    if not ENV_FILE.exists():
        template = """# Настройки базы данных
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=machine_tools

# Настройки приложения
APP_NAME=Machine Tools
DEBUG=True
API_V1_STR=/api/v1
"""
        ENV_FILE.write_text(template, encoding='utf-8')


# Загружаем переменные окружения
if not ENV_FILE.exists():
    create_env_file()
load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    """Основные настройки приложения"""
    # Настройки базы данных
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # Настройки приложения
    APP_NAME: str
    DEBUG: bool
    API_V1_STR: str

    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = True

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache()
def get_settings() -> Settings:
    """Получить настройки приложения"""
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print("Settings loaded successfully")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"App Name: {settings.APP_NAME}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"API Version: {settings.API_V1_STR}")
