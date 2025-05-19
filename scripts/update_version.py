#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from pathlib import Path

def update_version(new_version: str) -> None:
    """
    Обновляет версию во всех необходимых файлах.

    Args:
        new_version (str): Новая версия в формате X.Y.Z
    """
    # Проверяем формат версии
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print("Ошибка: версия должна быть в формате X.Y.Z")
        sys.exit(1)

    # Обновляем версию в version.py
    version_file = Path("machine_tools/version.py")
    version_content = version_file.read_text()
    version_content = re.sub(
        r'__version__ = ".*"',
        f'__version__ = "{new_version}"',
        version_content
    )
    version_file.write_text(version_content)

    # Обновляем версию в pyproject.toml
    pyproject_file = Path("pyproject.toml")
    pyproject_content = pyproject_file.read_text()
    pyproject_content = re.sub(
        r'version = ".*"',
        f'version = "{new_version}"',
        pyproject_content
    )
    pyproject_file.write_text(pyproject_content)

    print(f"Версия успешно обновлена до {new_version}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python update_version.py X.Y.Z")
        sys.exit(1)
    
    update_version(sys.argv[1]) 