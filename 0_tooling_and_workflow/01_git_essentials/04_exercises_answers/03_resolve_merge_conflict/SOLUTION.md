# Решение: 03_resolve_merge_conflict

```bash
git merge feature/prod-settings
# CONFLICT (content): Merge conflict in settings.py
```

Открываем `settings.py`, видим:

```
<<<<<<< HEAD
DEBUG = True
MAX_CONNECTIONS = 50
=======
DEBUG = False
MAX_CONNECTIONS = 10
>>>>>>> feature/prod-settings
```

Заменяем весь блок на объединённый результат (берём `DEBUG` из входящей
ветки, `MAX_CONNECTIONS` — из текущей):

```python
DEBUG = False
MAX_CONNECTIONS = 50
```

```bash
git add settings.py
git commit -m "merge: resolve settings conflict"
```

Коммит слияния автоматически получит двух родителей — это видно в
`git log --graph` по символу `|\`.
