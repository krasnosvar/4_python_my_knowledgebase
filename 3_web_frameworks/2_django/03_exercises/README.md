# Упражнения: найди и исправь N+1

Оба упражнения используют модели из [../02_examples/library](../02_examples/library/models.py)
(Author, Book, Tag, Review). Перед выполнением поднимите пример:

```bash
cd ../02_examples
pip install -r requirements.txt
python manage.py migrate
python manage.py demo_n_plus_one   # создаст тестовые данные
```

Затем скопируйте файл `command.py` из каждого упражнения в
`../02_examples/library/management/commands/` и запускайте через
`python manage.py <имя_файла_без_.py>`.

- [01_select_related](./01_select_related/) — N+1 через прямой
  ForeignKey, чинится `select_related`.
- [02_prefetch_related](./02_prefetch_related/) — N+1 через
  ManyToMany, чинится `prefetch_related`.

Порядок работы над каждым упражнением:
1. Запустить команду как есть, посмотреть на число запросов.
2. Найти отмеченный `# TODO` участок и исправить его.
3. Запустить снова — число запросов должно упасть до постоянного значения,
   не зависящего от количества книг.

Готовые решения — в [../04_exercises_answers](../04_exercises_answers/).
