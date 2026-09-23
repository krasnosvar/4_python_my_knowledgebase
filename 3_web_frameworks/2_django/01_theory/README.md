# Теория: Django ORM и структура проекта

1. [01_lazy_querysets.md](./01_lazy_querysets.md) — почему QuerySet ленив
   и как это приводит к N+1.
2. [02_select_related_prefetch_related.md](./02_select_related_prefetch_related.md)
   — как каждый метод работает под капотом и когда какой выбирать.
3. [03_project_structure.md](./03_project_structure.md) — project vs
   apps, `INSTALLED_APPS`, команды `manage.py`.
4. [04_signals.md](./04_signals.md) — `pre_save`/`post_save` и почему с
   сигналами нужно быть осторожным.

Практическая часть, которая показывает разницу в количестве SQL-запросов
до/после — в [../02_examples](../02_examples/).
