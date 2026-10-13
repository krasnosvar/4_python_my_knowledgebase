# Тема 07. Модули и import

Как подключить готовый код из другого файла или стандартной библиотеки:
`import x`, `from x import y`, `import x as y`, модули `math` и `random`,
смысл `if __name__ == "__main__":`, что такое пакет и откуда берутся
сторонние библиотеки. Последняя тема абсолютных основ.

## Структура раздела

- **[01_theory/](./01_theory/)** — теория:
  - [01_modules_and_imports.md](./01_theory/01_modules_and_imports.md) —
    модуль как файл, три формы `import`, `math`/`random`, `__name__`,
    пакеты, `pip` и виртуальные окружения в двух словах.
- **[02_examples/](./02_examples/)** — практические примеры:
  - [01_dice_and_geometry.py](./02_examples/01_dice_and_geometry.py) — все
    три формы импорта и функция `main()` под `if __name__ == "__main__":`.
- **[03_exercises/](./03_exercises/)** — задачи с самопроверкой `PASS`/`FAIL`:
  - `01_circle_area` — `import math`, константа `math.pi`.
  - `02_hypotenuse` — `from math import sqrt`.
- **[04_exercises_answers/](./04_exercises_answers/)** — эталонные решения.

## Как проходить тему

1. Прочитайте теорию:
   [01_modules_and_imports.md](./01_theory/01_modules_and_imports.md).
2. Запустите пример:
   ```bash
   python 02_examples/01_dice_and_geometry.py
   ```
3. Выполните задачи в `03_exercises/`, запуская файл для самопроверки:
   ```bash
   python 03_exercises/01_circle_area.py
   ```
4. Сверьтесь с эталонными ответами в `04_exercises_answers/`.

## Когда двигаться дальше

Если ты можешь подключить функцию из стандартной библиотеки и объяснить,
зачем в каждом упражнении стоит `if __name__ == "__main__":` — абсолютные
основы пройдены. Двигайся к [2_basics](../../2_basics/README.md): списки,
словари и то, как типы данных ведут себя изнутри.
