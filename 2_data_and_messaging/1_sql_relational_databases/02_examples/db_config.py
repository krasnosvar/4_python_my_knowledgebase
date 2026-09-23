"""Общие настройки подключения к PostgreSQL для примеров этого раздела.

Значения читаются из переменных окружения с fallback на параметры из
docker-compose.yml, чтобы все скрипты в этой папке подключались к одной и
той же локальной базе без дублирования DSN в каждом файле.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_USER = os.getenv("PG_USER", "kb_user")
PG_PASSWORD = os.getenv("PG_PASSWORD", "kb_password")
PG_DB = os.getenv("PG_DB", "kb_shop")

# DSN в формате libpq -- для psycopg (v3)
PSYCOPG_DSN = (
    f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} "
    f"user={PG_USER} password={PG_PASSWORD}"
)

# URL в формате SQLAlchemy (используем psycopg v3 как драйвер)
SQLALCHEMY_URL = (
    f"postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)
