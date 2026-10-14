# Git — шпаргалка

Подробности и объяснения — в [01_theory/](./01_theory/). ⚠️ — команда
переписывает историю: только для того, что ещё не отправлено (`push`).

## Настройка и старт

| Задача | Команда |
| :--- | :--- |
| Представиться Git (один раз) | `git config --global user.name "Имя"`<br>`git config --global user.email "you@example.com"` |
| Новый репозиторий с веткой `main` | `git init -b main` |
| Скачать существующий | `git clone <url>` |
| Привязать remote | `git remote add origin <url>` |

## Каждый день

| Задача | Команда |
| :--- | :--- |
| Что изменено / что в staging | `git status` (кратко: `git status -s`) |
| Что ещё не добавлено в staging | `git diff` |
| Что попадёт в коммит | `git diff --staged` |
| Добавить файл в staging | `git add <file>` |
| Добавить выборочно, по кускам | `git add -p` |
| Закоммитить | `git commit -m "feat: ..."` |
| История с ветками | `git log --oneline --graph --all` |
| Содержимое коммита | `git show <hash>` |
| Кто менял строку | `git blame <file>` |
| Отправить | `git push` (первый раз: `git push -u origin main`) |
| Скачать и влить чужие изменения | `git pull` |
| Только скачать, не трогая файлы | `git fetch` |
| Временно отложить правки | `git stash` / вернуть: `git stash pop` |

## Ветки

| Задача | Команда |
| :--- | :--- |
| Список веток | `git branch` |
| Создать ветку и перейти в неё | `git switch -c <name>` |
| Перейти в ветку | `git switch <name>` |
| Слить ветку в текущую | `git merge <name>` |
| Удалить слитую ветку | `git branch -d <name>` |
| Перенести свою ветку на свежий `main` ⚠️ | `git rebase main` |
| Причесать последние N коммитов ⚠️ | `git rebase -i HEAD~N` |
| Отправить ветку после rebase ⚠️ | `git push --force-with-lease` |

## Конфликты

| Задача | Команда |
| :--- | :--- |
| Какие файлы в конфликте | `git status` (`both modified`) |
| Отметить файл как разрешённый | `git add <file>` (после удаления маркеров `<<<<<<<` `=======` `>>>>>>>`) |
| Завершить merge | `git commit` |
| Завершить шаг rebase | `git rebase --continue` |
| Отменить merge / rebase целиком | `git merge --abort` / `git rebase --abort` |
| Взять целиком свою / чужую версию файла | `git checkout --ours <file>` / `git checkout --theirs <file>` |

## Отмена изменений

| Ситуация | Команда | История |
| :--- | :--- | :--- |
| Отменить незакоммиченную правку в файле | `git restore <file>` | не меняется |
| Убрать файл из staging, оставив правку | `git restore --staged <file>` | не меняется |
| Взять файл из старого коммита | `git restore --source=<hash> -- <file>` | не меняется |
| Исправить сообщение / дописать файл в последний коммит ⚠️ | `git add <file>`<br>`git commit --amend -m "..."` | переписывается |
| Убрать последний коммит, правки оставить в staging ⚠️ | `git reset --soft HEAD~1` | переписывается |
| Убрать последний коммит, правки оставить на диске ⚠️ | `git reset HEAD~1` | переписывается |
| Убрать коммит **и** правки ⚠️ | `git reset --hard HEAD~1` | переписывается, правки теряются |
| Отменить уже отправленный коммит | `git revert <hash>` | дополняется новым коммитом |
| Найти «потерянный» коммит после reset | `git reflog` | — |

## .gitignore

| Задача | Команда |
| :--- | :--- |
| Не отслеживать файлы | добавить паттерн в `.gitignore` (`*.log`, `__pycache__/`, `.venv/`, `.env`) |
| Перестать отслеживать уже закоммиченный файл | `git rm --cached <file>` (папку: `git rm -r --cached <dir>`) |
| Почему файл игнорируется | `git check-ignore -v <file>` |
