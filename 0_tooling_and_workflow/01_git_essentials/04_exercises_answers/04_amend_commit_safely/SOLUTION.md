# Решение: 04_amend_commit_safely

```bash
git add parser_test_notes.py
git commit --amend -m "fix: raise ValueError on empty line in parse_line()"
```

`--amend` заменяет последний коммит новым: staging area на момент запуска
команды (файл + уже закоммиченные изменения `parser.py`) становится
содержимым нового коммита, а сообщение — новым текстом. Количество коммитов
в репозитории не увеличивается.

Если бы этот коммит уже был отправлен в общий remote и его мог кто-то
затянуть себе (`git pull`), `--amend` делать не стоило бы — правильным
инструментом здесь был бы `git revert` (см. упражнение 5), поскольку
`--amend` меняет SHA коммита и требует `git push --force-with-lease`.
