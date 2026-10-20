# Repo Context & Conventions

This is a Russian-language Python backend knowledge base: language fundamentals
through idioms, OOP, iterators/generators, concurrency, stdlib, testing,
algorithms, CPython internals, plus data/messaging, web frameworks, system
design and engineering-communication topics. Root `README.md` is the master
index of top-level sections — it MUST be kept in sync any time a subsection is
added, removed, renamed, or nested; the same applies to each top-level topic's
own `README.md`.

All new content — theory, code comments in examples, exercise text — is
written in Russian, matching the rest of the repo.

## Directory & Structural Conventions

- `1_python/` holds the core language path as `<N>_<name>/` with a sequential
  integer prefix, currently: `1_python_fundamentals` (absolute zero —
  `00_setup` (install Python 3.12+, terminal, `cd`, `python3`/`python`/`py`,
  running a script, REPL, editor; the one place that explains which
  interpreter command to type — don't mass-rewrite `python` in other READMEs)
  + 8 topics: `01_variables_and_types`, `02_operators_and_expressions`,
  `03_input_output`, `04_control_flow`, `05_collections`,
  `06_functions_basics`, `07_exceptions`, `08_modules_and_imports`),
  `2_functions_and_decorators`, `3_oop`, `4_iterators_generators`,
  `5_concurrency`, `6_standard_library`, `7_testing`, `8_algorithms_dsa`,
  `9_under_the_hood`. `2_basics` was dissolved into `1_python_fundamentals`
  (syntax, collections, mutability, comprehensions, control flow) and
  `9_under_the_hood` (CPython internals: small int cache, string interning,
  hash table buckets/load factor, list over-allocation). Don't assume the
  prefix on disk and in `1_python/README.md` agree — verify with `ls` before
  trusting either; this repo has been renumbered (see "Renumbering history"
  below).
- Standard leaf template per subsection/subtopic: `01_theory/`, `02_examples/`,
  `03_exercises/`, `04_exercises_answers/`, `README.md`.
- **If `01_theory/` ever holds 2+ files, give each a numeric reading-order
  prefix** (`01_`, `02_`, ...) — e.g.
  `1_python/1_python_fundamentals/05_collections/01_theory/{01_..., 02_...}`.
  A single-file topic keeps its plain descriptive name (`01_...`). This
  matters doubly here: the prefix order isn't just for a reader browsing the
  bare directory — it's also the *dependency* order (see Clarity Principle
  below), so reordering theory files for pedagogy means renaming them, not
  just reshuffling a list in the README. Same convention as the sibling
  `5_devops_sre_knowledgebase` and `6_ai_engineering_knowledgebase` repos.
- Exercise/example file numbering (`03_exercises/01_foo.py`, `02_bar.py`, ...)
  does not need to match theory-file dependency order — exercises are meant
  to be done after reading *all* theory files in the section, so they can be
  ordered by difficulty instead.

## Cheat-sheets (`CHEATSHEET.md`)

The repo doubles as a quick reference for an experienced engineer, so every
topic with a `01_theory/` has a `CHEATSHEET.md` next to its `README.md`.
Exceptions — one combined sheet with a `##` section per subtopic:
`1_python/1_python_fundamentals/CHEATSHEET.md` and
`5_engineering_communication/CHEATSHEET.md` (subtopic READMEs link to
`../CHEATSHEET.md#<anchor>`).

- **Format** (see `0_tooling_and_workflow/01_git_essentials/CHEATSHEET.md`):
  `# <Тема> — шпаргалка`, then a line linking the theory; content grouped
  by `##` sub-headings as tables «задача → синтаксис/команда», decision
  tables «когда что», complexity tables, short code blocks, one-line
  pitfalls marked ⚠️. No prose paragraphs; 1–3 screens.
- **Derived from theory, kept in sync**: every row must match what that
  topic's `01_theory/` teaches and link to the specific theory file. When
  you change theory (renamed API, new rule, renamed/renumbered file),
  update the cheat-sheet in the same edit. Version-dependent behaviour
  carries the version (`3.11+`, `3.12+`).
- Cheat-sheets are reference material, so the Clarity Principle does not
  apply to them (they may use constructs from later sections).
- Each topic `README.md` has one line near the top, right before
  «Что нужно знать заранее»: «**Уже знакомы с темой?** →» followed by a
  relative link to `./CHEATSHEET.md` (or `../CHEATSHEET.md#<anchor>` for
  subtopics of a combined sheet) and a short description.
- Root `README.md` section «Шпаргалки» indexes all cheat-sheets grouped by
  section — add/remove/rename entries there together with the file.
- Runnable snippets in cheat-sheets must actually be run (python3 with a
  timeout); snippets needing servers (Redis, Kafka, Docker) are marked as
  such in the sheet.

## Section framing — every README answers "зачем"

Title labels: top-level dirs are `# Раздел N. <Русское название> (English)`
(`0_tooling_and_workflow` … `5_engineering_communication`; `other` is
"Дополнительно"). Their subdirs are `# Тема <prefix as on disk>. ...`
(`Тема 01.` in `0_tooling`, `4_system_design`, `5_engineering_communication`,
`other`; `Тема 3.` in `1_python`, `2_data_and_messaging`, `3_web_frameworks`).
`1_python_fundamentals` is itself `Тема 1.` and its subtopics are
`Тема 1.0` … `Тема 1.8`. Russian name first, English in parentheses.

Every section/topic README (in `1_python/` and in the top-level sections)
opens with a title (`Тема N. ...` in `1_python/`), a **"Зачем этот раздел"**
paragraph — what concrete problem it solves and what the reader can do
afterwards — then prerequisites, a linked file list, how to go through it,
and "Когда двигаться дальше".

## Where foundational topics live (link here, don't re-explain)

A repo-wide audit found these used everywhere but taught nowhere; each now
has one home — later sections give a one-line gloss plus a link:
- exceptions (`try/except/raise`) → `1_python_fundamentals/07_exceptions/`
- `import`, modules, `if __name__ == "__main__"` →
  `1_python_fundamentals/08_modules_and_imports/`
- type hints → section "Аннотации типов" in
  `1_python_fundamentals/06_functions_basics/01_theory/01_functions_basics.md`
  (full depth: `other/02_typing_and_static_analysis/`)
- list/tuple/set/dict syntax, O(1)/O(n) glossary →
  `1_python_fundamentals/05_collections/01_theory/01_lists_tuples_sets_dicts.md`
  (full Big-O: `8_algorithms_dsa/01_theory/01_big_o_notation.md`)
- what a class/object/`self` is → `3_oop/01_theory/01_what_is_a_class.md`
- recursion → `8_algorithms_dsa/01_theory/05_recursion_basics.md`
- HTTP, routes, status codes, ASGI/WSGI →
  `3_web_frameworks/1_fastapi/01_theory/01_http_and_first_app.md`
- basic SQL →
  `2_data_and_messaging/1_sql_relational_databases/01_theory/01_sql_in_5_minutes.md`
- CAP / eventual consistency →
  `.../01_theory/09_cap_and_eventual_consistency.md`
- venv/pip → `other/01_environments_and_packaging/` (needed before any
  `pip install -r requirements.txt`, even though it lives in `other/`)

Internals for curious readers (hash buckets, load factor, over-allocation)
go into a `<details>` "Для любопытных" block so the main text stays
readable for someone coming straight from the previous section.

For language-agnostic System Design theory, `4_system_design` explicitly
summarizes the core concept inline (`## О чём эта тема (краткий контекст)`)
and links to the canonical section in the sibling repo
(`../5_devops_sre_knowledgebase/14_system_design/`). Do not point to sibling
repos without an inline summary or to non-existent paths.

## Clarity Principle — never use a construct before it's taught

The core rule governing reading order in this repo: an example or exercise
must never use a Python construct (syntax, built-in, stdlib import) that
hasn't been introduced yet by an earlier theory file — in the same subtopic,
or in an earlier subtopic/section the reader is assumed to have finished.

Real bugs found and fixed under this rule:
- While writing `1_python_fundamentals` from scratch: an example used a `for`
  loop before control flow was taught, another used `for...else` before it
  was introduced, and an exercise hinted at string slicing (`text[::-1]`)
  before slicing existed anywhere in the section. All three were caught
  before merging by checking each new file against what prior files in the
  same subtopic had actually taught, and fixed by using only
  already-introduced constructs (explicit boolean flags, manual loops).
- A deeper, structural case: `2_basics/01_theory/01_mutability_and_identity.md`
  and `02_hashability_and_performance.md` (original numbering) both leaned
  heavily on `list`/`dict`/`tuple`/`set` literal syntax, indexing, and
  methods — but the file that actually teaches those types,
  `04_collections_lists_tuples_sets_dicts.md`, came *after* them in the
  original order. A reader who'd just finished `1_python_fundamentals` (which
  stops at int/float/str/bool/None) would hit `lst.append(4)` and
  `cache[("GET", "/users", 1)] = ...` with zero prior exposure to list/dict
  syntax. Fixed by **renumbering the files**, not rewriting the content:
  collections now comes first (`01_builtin_types.md`,
  `02_collections_lists_tuples_sets_dicts.md`), then
  `03_mutability_and_identity.md`, `04_hashability_and_performance.md`,
  `05_comprehensions.md`, `06_control_flow.md`. A smaller instance of the
  same bug was found in the collections file itself, which used a list
  comprehension (`[[0] * 3 for _ in range(3)]`) before `05_comprehensions.md`
  teaches comprehension syntax — fixed by rewriting that one line as an
  explicit `for` loop instead of reordering.
- **Reordering alone can move the bug instead of fixing it.** After the
  collections file was moved to `02`, it in turn used O(1)/O(n),
  "изменяемый", "хешируемый", "хеш-таблица" before `03`/`04` defined them,
  and still taught no basic list/dict syntax. Real fix: a "Синтаксис за 2
  минуты" block + mini-glossary at its top. After any reorder, re-audit the
  file that moved *earlier* for terms it now uses too soon.
- Other intra-section order bugs fixed the same way: `3_functions` (lambdas
  and `*args/**kwargs` now `01`/`02`, before decorators), `9_algorithms_dsa`
  (recursion basics split out before trees/sorting), `2_django` (project
  structure + what a model is before querysets), `4_oop` (new
  `01_what_is_a_class.md` before `__init__` vs `__new__`). Material that
  genuinely needs a later section (context managers via class/`yield` in
  section 3) carries an explicit "вернитесь после разделов 4–5" note rather
  than silently assuming it.
- **When auditing for this class of bug**, don't just check a file in
  isolation — check it against what every *earlier-numbered* file in its own
  01_theory/ actually covers, and against what the previous subtopic/section
  (by the repo's own reading order) covers. A read-only parallel fork/subagent
  pass per section is an effective way to do this at scale without blowing up
  the reviewing agent's context; have it read full theory files, not just
  skim the first one per section — a first pass that only spot-checked one
  file per section missed the collections/mutability ordering bug entirely.

## Exercise/Example Conventions

- `02_examples/*.py` — runnable, self-contained scripts demonstrating the
  topic; no `TODO`s, just working code with illustrative output.
- `03_exercises/*.py` — a function body with `# TODO:` markers, raising
  `NotImplementedError` until filled in, plus a `_self_check()` function that
  uses `assert`, prints `PASS: ...` per check, and ends with a
  `f"{checks_passed}/{total_checks} проверок пройдено"` summary. Each
  exercise file has a sibling `README.md` in the same `03_exercises/`
  directory explaining how to run it.
- `04_exercises_answers/*.py` — same filenames as `03_exercises/`, same
  `_self_check()` pattern, with the reference implementation instead of
  `NotImplementedError`. For per-exercise directories the answer directory
  has the *same name* as the exercise directory (no `_answers` suffix).
- The `проверок пройдено` summary line is mandatory everywhere, but only
  `1_python_fundamentals` wraps checks in `_self_check()`; sections 2–9
  count `checks_passed`/`total_checks` inside `main()`/`if __name__` —
  don't "fix" that into `_self_check()` without being asked.
- Exercise file/dir names everywhere are `NN_name` (two-digit prefix) — no
  `task_N_`, `exN_`, single-digit `1_` variants.
- Fundamentals exercises 01–05 use `def`/`return`/`raise`/`if __name__`
  before topics 06–08 teach them; this is deliberate and covered by a
  "Как устроен файл упражнения" block (edit only the line under `TODO`,
  the rest is scaffolding explained in 06–08). Keep that block when editing.
- After writing or editing any of these, actually run them — `python
  path/to/script.py` for examples and answers (must exit cleanly with correct
  output / all `PASS`), and for exercise files confirm they raise
  `NotImplementedError` until implemented. Don't rely on reading the code.
  Run them non-interactively with `</dev/null` and a timeout; scripts using
  `input()` need input piped (`printf 'Аня\n25\n' | python3 ...`), otherwise
  the `EOFError` is a false failure.
- Known intentional exceptions to "unsolved exercise raises
  `NotImplementedError`": `3_oop/03_exercises/02-05` fail with
  `TypeError`/`AttributeError` because the TODO is "add a method/`__init__`"
  (nothing to raise from yet); `7_testing/03_exercises/*/` source modules run
  clean because the task is to write the tests for them.
- **Git block (`0_tooling_and_workflow/01_git_essentials/`) uses no
  scripts.** It was rewritten away from `setup.sh`/`check.sh`/`solve.sh`
  wrappers, because the owner found they confused beginners: the learner
  should type the git commands, not run a harness. Format:
  `02_examples/NN_*.md` are walkthroughs (command → real output →
  explanation). `03_exercises/NN_*.md` each have «Подготовка» (commands the
  learner types, working in `~/git-practice/exNN` outside the repo),
  «Задание» (no commands given) and «Проверь себя» (plain git commands plus
  expected output). `04_exercises_answers/NN_*.md` use the same filenames.
  `CHEATSHEET.md` holds the «задача → команда» tables. Don't reintroduce
  `.sh` there. Output shown in these files must come from actually running
  the commands (hashes may differ). Use only `printf`/`echo`/heredocs, no
  `sed -i`, so the commands also work on macOS.
  The Docker block keeps `check.sh` on purpose, because it actually builds
  the image and calls `curl`.

## Renumbering history (watch for stale refs)

`1_python/` was restructured once to add a true from-zero entry point. Old →
new mapping, kept here so a future stale reference (old name surviving in
prose, a comment, or a link) can be recognized on sight:

| Old | New |
|---|---|
| (none — new) | `1_python_fundamentals` |
| `1_basics` | `2_basics` |
| `2_functions_and_decorators` | `3_functions_and_decorators` |
| `3_oop` | `4_oop` |
| `4_iterators_generators` | `5_iterators_generators` |
| `5_concurrency` | `6_concurrency` |
| `6_standard_library` | `7_standard_library` |
| `7_testing` | `8_testing` |
| `8_algorithms_dsa` | `9_algorithms_dsa` |
| `9_under_the_hood` | `10_under_the_hood` |

A first grep pass for stale references after this rename still missed 10
occurrences (stale "Тема N" headers in 4 READMEs, stale old-path mentions
inside theory prose) because it only checked for the literal old directory
names as link targets, not prose references like "модуле `5_concurrency`"
(now `6_concurrency`) or "Тема 4" headers that hadn't been bumped. **After any
renumber, grep for old names as plain text, not just as link paths**, and
re-check every README's own "Тема N" / "Раздел N" self-labeling.

Second pass (theory-file renames inside sections, all links updated):
`3_functions_and_decorators/01_theory` reordered (lambdas/args first);
`4_oop/01_theory` shifted +1 after the new `01_what_is_a_class.md`;
`9_algorithms_dsa/01_theory` 05→06 trees, 06→07 sorting, 07→08 DP (+ new
`05_recursion_basics.md`); `3_web_frameworks/1_fastapi/01_theory` shifted +1
after the new HTTP lesson; `2_django/01_theory` reordered (project structure
first); the three monolithic `01_theory/README.md` files in
`2_data_and_messaging` split into numbered lessons (each `01_theory/README.md`
kept as a short index so inbound links survive); docker exercise
`03_compose_with_db` → `03_compose_with_cache` (it uses Redis, not a DB).

Third pass (naming unification, all refs updated):
`04_exercises_answers/NN_name_answers/` → `NN_name/` in `6_concurrency`,
`7_standard_library`, `8_testing`, `9_algorithms_dsa`, `10_under_the_hood`;
exercise names in `2_data_and_messaging` (SQL `task_1a…task_4_*` →
`01_…06_*`, brokers `exN_*` → `0N_*`)
and `3_web_frameworks` (FastAPI `1_*`/`2_*`, Django `task_0N_*`) → `NN_name`;
new `1_python_fundamentals/00_setup/`. Grep for `_answers/`, `task_`, `ex1_`
as plain text after touching these areas.

Fourth pass (`2_basics` dissolved):
`2_basics` was dissolved into `1_python_fundamentals` (added `05_collections`,
renamed `04_control_flow_basics` → `04_control_flow`, shifted `05..07` →
`06..08`), `3_oop` (`09_hashable_key.py`), `8_algorithms_dsa`
(`13_membership_performance`), and `9_under_the_hood` (CPython small int
caching, string interning, list/dict/set memory layout and hash table internals,
comprehension `LIST_APPEND` bytecode). Top-level folders in `1_python/` were
renumbered `3..10` → `2..9` (`2_functions_and_decorators`, `3_oop`,
`4_iterators_generators`, `5_concurrency`, `6_standard_library`, `7_testing`,
`8_algorithms_dsa`, `9_under_the_hood`).

## Cross-Reference Discipline

Sections and files link to each other via relative markdown links. Any
rename, move, or reorder breaks an unpredictable number of these.

**After any structural change, re-verify every relative link — don't rely on
memory.** A code-fence-aware script does this reliably: glob all `*.md`
files (including dot-directories like `.agents/` — `glob.glob("**/*.md",
recursive=True)` silently skips those, so dot-directories need an explicit
separate path), skip lines inside ` ``` ` fences (otherwise Python tuple
syntax like `(a, b)` in a code sample false-positives as a markdown link),
regex-match `\]\(([^)]+)\)`, resolve each non-URL target against its file's
directory with `os.path.normpath(os.path.join(dirname, link))`, and assert
`os.path.exists`. Run it repo-wide, not just in the touched subtree.

## Git & Workspace Discipline

- **Do not commit without explicit instruction:** never create git commits
  unless the user explicitly asks to commit — writing/editing files is fine
  on request alone.

## Validation Checklist (run after any batch of edits)

1. **Relative links resolve** — see Cross-Reference Discipline script above;
   run repo-wide.
2. **No stray mixed-script glyphs** — a real self-introduced bug was a single
   CJK character accidentally typed into Russian prose. Scan with
   `grep -rnP '[\x{4e00}-\x{9fff}]'` across touched files. Also scan for
   words glued from Latin + Cyrillic (real hits: "коммit", "formы",
   "practике", "corutina", "materializировать", "momент"):
   `grep -rnoP '\b\w*(?:[а-яё][a-z]|[a-z][а-яё])\w*\b' --include='*.md'
   --include='*.py' .` — review hits by hand (`\nчисло` inside a string is
   a legit escape, not a typo).
3. **No stale old-numbering references** — grep for the "Old" column names
   from the renumbering table above as plain text, not just as link targets.
4. **Examples/answers run clean, exercises raise `NotImplementedError`** —
   actually execute them (`python3 -m py_compile` is not a substitute for
   running `_self_check()`). For a repo-wide syntax pass use `ast.parse` —
   `py_compile` with `cfile="/dev/null"` errors on every file.
6. **Factual correctness of code in theory** — run code blocks you add or
   change. Real bugs this caught: missing `timezone` import in the datetime
   lesson, FastAPI `x_token: str` read from query instead of header (needs
   `Header()`), a coverage example that didn't demonstrate what it claimed
   (verified the fix with real coverage.py), an LSP example where the base
   class had no setter so nothing was violated, `__closure__` read off an
   out-of-scope name.
7. **Fence balance** — count of lines starting with ```` ``` ```` is even in
   every `.md`.
8. **Every section/topic has a README with "Зачем этот раздел"** (see
   Section framing).
9. **Cheat-sheets** — every topic with `01_theory/` has a `CHEATSHEET.md`
   (or a section in a combined one), linked from its README and from the
   root «Шпаргалки» index; anchors in `CHEATSHEET.md#...` links resolve;
   snippets you added/changed were run; rows still match the theory you
   just edited (see Cheat-sheets above).
5. **Clarity Principle** — for any new or reordered theory file, confirm
   every construct used in its examples/exercises was already taught by an
   earlier-numbered file in the same `01_theory/`, or by an earlier
   subtopic/section in the repo's own reading order.
