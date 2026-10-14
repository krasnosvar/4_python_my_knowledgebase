# Решение: упражнение 4. Безопасный amend последнего коммита

Условие: [../03_exercises/04_amend_commit_safely.md](../03_exercises/04_amend_commit_safely.md).

```bash
cd ~/git-practice/ex04
git add parser_notes.md
git commit --amend -m "fix: raise ValueError on empty line in parse_line()"
```

```
[main 7852657] fix: raise ValueError on empty line in parse_line()
 Date: Wed Oct 14 11:43:36 2026 +0400
 2 files changed, 3 insertions(+)
 create mode 100644 parser_notes.md
```

## Почему так

`--amend` не дописывает коммит, а **заменяет** его новым. Новый коммит
содержит всё, что было в staging area: уже закоммиченную правку
`parser.py` и добавленный `parser_notes.md`. Поэтому коммитов остаётся
два, а у последнего меняется хеш.

Из-за смены хеша amend безопасен только для коммитов, которые ещё никто
не скачал. Если коммит уже отправлен в общий remote, исправлять его нужно
новым коммитом или через `git revert` (упражнение 5). Иначе пришлось бы
делать `git push --force-with-lease` и предупреждать команду.
