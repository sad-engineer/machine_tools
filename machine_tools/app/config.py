#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


def get_project_root():
    """Возвращает корневую директорию проекта"""
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / 'pyproject.toml').exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent.parent


PROJECT_ROOT = get_project_root()
CONFIG_DIR = PROJECT_ROOT / "settings"
ENV_FILE = CONFIG_DIR / "machine_tools.env"
CONFIG_DIR.mkdir(exist_ok=True)


def create_env_file() -> None:
    """Создать файл machine_tools.env с шаблоном настроек"""
    if not ENV_FILE.exists():
        template = """# Настройки базы данных
POSTGRES_USER=local_user
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=machine_tools

# Настройки приложения
APP_NAME=Machine Tools
DEBUG=False
API_V1_STR=/api/v1
"""
        ENV_FILE.write_text(template, encoding='utf-8')


TEST_ENV = os.environ.get("MACHINE_TOOLS_ENV")
if TEST_ENV and Path(TEST_ENV).exists():
    load_dotenv(TEST_ENV, override=True)
else:
    load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    """Основные настройки приложения"""

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    APP_NAME: str
    DEBUG: bool
    API_V1_STR: str

    class Config:
        env_file = str(TEST_ENV if TEST_ENV and Path(TEST_ENV).exists() else ENV_FILE)
        case_sensitive = True

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


def save_setting(key: str, value: str) -> None:
    """Сохранить одну настройку в файл конфигурации"""
    current_settings = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    current_settings[k.strip()] = v.strip()

    current_settings[key] = value

    with open(ENV_FILE, 'w', encoding='utf-8') as f:
        f.write("# Настройки базы данных\n")
        f.write(f"POSTGRES_USER={current_settings.get('POSTGRES_USER', 'local_user')}\n")
        f.write(f"POSTGRES_PASSWORD={current_settings.get('POSTGRES_PASSWORD', 'postgres')}\n")
        f.write(f"POSTGRES_HOST={current_settings.get('POSTGRES_HOST', 'localhost')}\n")
        f.write(f"POSTGRES_PORT={current_settings.get('POSTGRES_PORT', '5432')}\n")
        f.write(f"POSTGRES_DB={current_settings.get('POSTGRES_DB', 'machine_tools')}\n")
        f.write("\n")
        f.write("# Настройки приложения\n")
        f.write(f"APP_NAME={current_settings.get('APP_NAME', 'Machine Tools')}\n")
        f.write(f"DEBUG={current_settings.get('DEBUG', 'True')}\n")
        f.write(f"API_V1_STR={current_settings.get('API_V1_STR', '/api/v1')}\n")


def get_settings() -> Settings:
    """Получить настройки приложения"""
    return Settings()


def show_settings() -> None:
    """Показать текущие настройки приложения"""
    settings = get_settings()
    print("НАСТРОЙКИ БАЗЫ ДАННЫХ:")
    print(f"    Пользователь: {settings.POSTGRES_USER}")
    print(f"    Хост: {settings.POSTGRES_HOST}")
    print(f"    Порт: {settings.POSTGRES_PORT}")
    print(f"    База данных: {settings.POSTGRES_DB}")
    print(f"    URL подключения: {settings.DATABASE_URL}")
    print("Настройки приложения:")
    print(f"    Название приложения: {settings.APP_NAME}")
    print(f"    Режим отладки: {settings.DEBUG}")
    print(f"    API версия: {settings.API_V1_STR}")


def check_file_settings():
    """Проверяет, являются ли настройки файла дефолтными (первый запуск)"""
    return ENV_FILE.exists()


if __name__ == "__main__":
    show_settings()

    # POSTGRES_USER = test_user
    # POSTGRES_PASSWORD = 753951
