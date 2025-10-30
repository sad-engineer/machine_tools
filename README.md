# Machine Tools

| | |
| --- | --- |
| Testing | [![CI - Test](https://github.com/sad-engineer/machine_tools/actions/workflows/python-tests.yml/badge.svg)](https://github.com/sad-engineer/machine_tools/actions/workflows/python-tests.yml) |

# Machine Tools Database

Пакет для работы с базой данных станков и их технических требований.

## Графический интерфейс

Для удобной работы с базой данных доступно отдельное GUI приложение:

[![Machine Tools GUI](https://img.shields.io/badge/Machine%20Tools-GUI%20Application-blue?style=for-the-badge)](https://github.com/sad-engineer/machine_tools_gui_kivi)

Приложение предоставляет удобный интерфейс для:
- Просмотра и редактирования данных о станках
- Фильтрации и поиска станков
- Управления техническими требованиями
- Экспорта и импорта данных

## Установка

### Вариант 1: Poetry (рекомендуется)
```bash
poetry add git+https://github.com/sad-engineer/machine_tools.git
```

### Вариант 2: pip
```bash
pip install git+https://github.com/sad-engineer/machine_tools.git
```

### Установите зависимости:
```bash
poetry install
```


## Инициализация базы данных

### Настройка PostgreSQL

1) Установите PostgreSQL, если еще не установлен:
   - Windows: скачайте установщик с [официального сайта](https://www.postgresql.org/download/windows/)
   - Linux: `sudo apt-get install postgresql`
   - Mac: `brew install postgresql`

2) Запустите сервер PostgreSQL, если еще не запущен:
```bash
# Windows (если установлен в стандартную папку)
"C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe" start -D "C:\Program Files\PostgreSQL\17\data"

# Linux
sudo systemctl start postgresql

# Mac
brew services start postgresql
```

3) Создайте подключение для работы с базой данных по станкам:
```powershell
.\psql.exe -U postgres -c "CREATE USER your_user WITH PASSWORD 'your_password';"
```

4) Передайте созданному пользователю права для работы с базой
```powershell
.\psql.exe -U postgres -h localhost -p 5432 -c "ALTER ROLE your_user CREATEDB;"
```

### Настройка пакета для работы с данными

1) Передайте настройки подключения.
```bash
machine_tools setup-db-connection
# или просто запустите любую команду, мастер настройки запустится автоматически
```

2) Установите базу данных 

Проект использует базу данных станков. База данных поставляется с пакетом machine_tools. 
Перед использованием пакетных данных, необходимо инициализировать данные.

```bash
# Вариант 1: Используя команду machine_tools
machine_tools init
```

### Мастер настройки

При первом запуске любой команды (например, `machine_tools status`), если файл настроек отсутствует, автоматически запустится мастер первоначальной настройки.

Мастер запросит у вас:
- **Хост PostgreSQL** 
- **Порт PostgreSQL** 
- **Пользователь PostgreSQL**
- **Пароль PostgreSQL**

После ввода настроек автоматически проверяется подключение к серверу PostgreSQL.


### Настройка подключения к базе данных

Проект предоставляет удобные команды CLI для проверки соединения, управления настройками подключения к PostgreSQL:

| Параметр                        | Команда               | Поддерживаемые параметры |
|---------------------------------|-----------------------|--------------------------|
| Загрузить настройки подключения | `setup-db-connection` | `--verbose` или `-v`     |
 | Проверка подключения           | `check-connection`    | `--verbose` или `-v`     |
| Проверка базы данных            | `check-database`      | `--verbose` или `-v`     |
| Проверка таблиц                 | `check-tables`        | `--verbose` или `-v`     |
| Общий статус системы            | `status`              | `--verbose` или `-v`     |
| Удаление базы данных            | `drop-db`             | `--verbose` или `-v`     |

* Например:
```bash
machine_tools status
# или 
python -m machine_tools.cli status

machine_tools status --verbose
# или 
python -m machine_tools.cli status --verbose
```

#### Команда `status` - Проверка статуса системы

Команда `status` выполняет комплексную проверку всей системы:

1. **Проверка наличия настроек** - если файл настроек отсутствует, автоматически запускается мастер настройки
2. **Проверка подключения к PostgreSQL** - проверяет доступность сервера БД
3. **Проверка базы данных** - проверяет существование базы данных `machine_tools`
4. **Проверка таблиц** - проверяет наличие необходимых таблиц в базе данных

```bash
# Базовая проверка
machine_tools status

# Проверка с подробным выводом ошибок
machine_tools status --verbose
```
Используйте флаг `--verbose` для подробной информации об ошибке

#### Настройка параметров подключения

| Параметр                         | Команда                | Параметр с примеров использования              |
|----------------------------------|------------------------|------------------------------------------------|
| Просмотр настроек подключения    | `config show`          |                                                |
| Хост                             | `config set-host`      | `--host "192.168.1.100"`                       |
| Порт                             | `config set-port`      | `--port 5432`                                  |
| Пользователь                     | `config set-user`      | `--user "user"`                                |
| Пароль                           | `config set-password`  | `--password "new_password"`                    |
| Комплексно                       | `config set`           | `--host localhost --port 5432 --user postgres` |

* Например:
```bash
machine_tools config set-host --host "192.168.1.100"
# или через запрос:
machine_tools config set-host
# Команда запросит адрес хоста интерактивно
```

 Команда `config set` позволяет настроить все основные параметры подключения к базе данных одновременно:

```bash
machine_tools config set --host localhost --port 5432 --user postgres
#Параметры команды:
# --host - Хост PostgreSQL сервера (по умолчанию: localhost)
# --port - Порт PostgreSQL сервера (по умолчанию: 5432)  
# --user - Имя пользователя PostgreSQL (по умолчанию: local_user)
# --password - Пароль (запрашивается интерактивно, скрытый ввод)

# Альтернативный способ:
python -m machine_tools.cli config set --host localhost --port 5432 --user postgres
```

### Файл настроек

Настройки сохраняются в файл `settings/machine_tools.env`:

```env
# Настройки базы данных
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=machine_tools

# Настройки приложения
APP_NAME=Machine Tools
DEBUG=True
API_V1_STR=/api/v1
```

#### Проверка данных

| Параметр                          | Команда                       | Параметр         |
|-----------------------------------|-------------------------------|------------------|
| Просмотр станков (10 строк)       | `show-machines`               |                  |
| Просмотр станков (N строк)        | `show-machines`               | `--limit N`      |
| Просмотр техтребований (10 строк) | `show-technical-requirements` |                  |
| Просмотр техтребований (N строк)  | `show-technical-requirements` | `--limit N`      |


## Использование

Примеры использования находятся в папке examples

## Требования

- Python 3.9+
- PostgreSQL 12+
- SQLAlchemy
- Pandas
- Alembic
- Click (для CLI)