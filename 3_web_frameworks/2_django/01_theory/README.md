# Теория: Django ORM и структура проекта

Файлы читать по порядку — каждый опирается на предыдущие:

1. [01_project_structure.md](./01_project_structure.md) — project vs
   apps, `INSTALLED_APPS`, команды `manage.py`, что такое модель и как
   выглядит простейший запрос через ORM.
2. [02_lazy_querysets.md](./02_lazy_querysets.md) — почему QuerySet ленив
   и как это приводит к N+1.
3. [03_select_related_prefetch_related.md](./03_select_related_prefetch_related.md)
   — как каждый метод работает под капотом и когда какой выбирать.
4. [04_signals.md](./04_signals.md) — `pre_save`/`post_save` и почему с
   сигналами нужно быть осторожным.

Практическая часть, которая показывает разницу в количестве SQL-запросов
до/после — в [../02_examples](../02_examples/).
