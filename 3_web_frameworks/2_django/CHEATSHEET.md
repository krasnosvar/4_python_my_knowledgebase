# Django — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — частая
ошибка, которая бьёт по производительности или данным. Проверено на
Django 6.0.

## Структура проекта

Подробно: [01_project_structure.md](./01_theory/01_project_structure.md).

| Файл | Что в нём |
| :--- | :--- |
| `config/settings.py` | БД, `INSTALLED_APPS`, middleware, секреты (из env) |
| `config/urls.py` | корневые маршруты, `include()` urls приложений |
| `config/wsgi.py` / `asgi.py` | точки входа для Gunicorn / Uvicorn, Daphne |
| `<app>/models.py` | модели (таблицы) |
| `<app>/views.py`, `<app>/urls.py` | обработчики и маршруты приложения |
| `<app>/admin.py` | регистрация моделей в `/admin/` |
| `<app>/migrations/` | миграции — коммитятся в git |

- ⚠️ Приложение не в `INSTALLED_APPS` → Django не видит его модели и не создаёт миграции.

## `manage.py`

| Задача | Команда |
| :--- | :--- |
| Dev-сервер | `python manage.py runserver` |
| Сгенерировать миграции по `models.py` | `python manage.py makemigrations` |
| Применить миграции к БД | `python manage.py migrate` |
| Консоль с настройками Django | `python manage.py shell` |
| Администратор для `/admin/` | `python manage.py createsuperuser` |

Порядок: `makemigrations` (описать, закоммитить) → `migrate` (применить).

## ORM: lookups

| Запрос | SQL |
| :--- | :--- |
| `Book.objects.all()` | `SELECT * FROM book` |
| `.filter(published_year=2001)` | `WHERE published_year = 2001` |
| `.filter(published_year__gte=2000)` | `>=` (также `__gt`, `__lt`, `__lte`) |
| `.filter(title__contains="Py")` / `.filter(id__in=[1, 2])` | `LIKE '%Py%'` / `IN (1, 2)` |
| `.filter(author__name="Unknown")` | `JOIN` по связи через `__` |
| `.exclude(...)`, `.order_by("-published_year")` | `NOT (...)`, `ORDER BY ... DESC` |

## Когда QuerySet идёт в БД

Подробно: [02_lazy_querysets.md](./01_theory/02_lazy_querysets.md).

| Операция | Запрос в БД? |
| :--- | :--- |
| `.filter()`, `.exclude()`, `.order_by()`, `.annotate()` | нет — строит новый QuerySet |
| срез `qs[:10]` | нет — станет `LIMIT` |
| `for obj in qs`, `list(qs)` | да |
| `bool(qs)`, `if qs:` | да |
| `len(qs)` | да |
| `repr(qs)` (печать в shell) | да |
| `book.author` без предзагрузки | да — **отдельный** запрос на каждый объект |

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as ctx:   # работает и при DEBUG=False
    for book in Book.objects.all():
        _ = book.author.name
print(len(ctx.captured_queries))   # 1 + N — это и есть N+1
```

## `select_related` vs `prefetch_related`

Подробно: [03_select_related_prefetch_related.md](./01_theory/03_select_related_prefetch_related.md).

| Связь | Метод | Запросов | Как работает |
| :--- | :--- | :--- | :--- |
| `ForeignKey` / `OneToOne`, прямое направление | `select_related("author")` | 1 | SQL `JOIN` |
| Обратный `ForeignKey` (`author.books`) | `prefetch_related("books")` | 2 | второй `SELECT ... WHERE fk IN (...)`, склейка в Python |
| `ManyToMany` (любое направление) | `prefetch_related("tags")` | 2 | то же |
| FK, но JOIN размножит тысячи строк | `prefetch_related` | 2 | без дублирования строк |

- Цепочка связей: `select_related("author", "publisher__country")`.
- ⚠️ `select_related("tags")` для M2M — ошибка `FieldError`, JOIN тут неприменим.
- ⚠️ Забытая предзагрузка: на тестовых данных незаметно, на проде — тысячи запросов.
- ⚠️ Лишняя предзагрузка неиспользуемого поля — лишний запрос и память.

## Сигналы

Подробно: [04_signals.md](./01_theory/04_signals.md).

| Сигнал | Когда |
| :--- | :--- |
| `pre_save` / `post_save` | до / после `Model.save()` (`created=True` для новой записи) |
| `pre_delete` / `post_delete` | до / после удаления |
| `m2m_changed` | изменён состав `ManyToMany` |

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Book)
def create_reading_stats(sender, instance, created, **kwargs):
    if created:
        ReadingStats.objects.create(book=instance)
```

| Подходит сигнал | Лучше явный вызов сервисной функции |
| :--- | :--- |
| вызывающий код не может знать о побочном эффекте (сторонняя библиотека) | побочный эффект — часть вашей бизнес-операции |
| инвалидация кэша, аудит изменений | важен порядок и тестируемость |

- ⚠️ Сигнал неявен: читая `book.save()`, не видно, что ещё произойдёт; падение обработчика срывает основную операцию.
- Регистрировать обработчики в `AppConfig.ready()` (`apps.py`) или явно импортируемом `signals.py`.
