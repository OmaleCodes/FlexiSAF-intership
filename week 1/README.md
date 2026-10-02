# Task Manager — Week 1 Refactor

A small task-tracking script, refactored from a single untyped file into a
typed, tested, linted mini-application. The original behavior is unchanged;
only the internal structure, typing, and error handling were improved.

## Project structure

```
task_manager_project/
├── main.py              # Entry point — runs the same scenario as before
├── src/
│   ├── models.py         # Task + Priority data models
│   └── manager.py        # TaskManager: all task logic
├── tests/
│   └── test_manager.py   # Unit tests for TaskManager
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python main.py
```

## How to run the tests

```bash
PYTHONPATH=. pytest tests/ -v
```

## How to run the linter/formatter

```bash
black src/ main.py tests/
ruff check src/ main.py tests/
```

## Style report (before → after)

| Area | Before | After | Why |
|---|---|---|---|
| Data representation | Tasks were plain `dict`s with string keys (`t["title"]`) | `Task` dataclass with named, typed fields | Removes typo-prone string keys; editor autocomplete and type checkers can now catch mistakes |
| Priority values | Free-text strings (`"high"`, typos possible) | `Priority` enum (`LOW`, `MEDIUM`, `HIGH`) | Invalid priorities are now caught immediately instead of silently accepted |
| State | Module-level global list (`global tasks`) | Encapsulated inside a `TaskManager` class | Removes hidden global mutation; state and behavior now live together |
| Type hints | None anywhere | Every function/method signature annotated | Makes expected inputs/outputs explicit; catches mismatches early |
| Error handling | Bare `except:` that just prints a string | Specific exceptions (`ValueError`, custom `TaskNotFoundError`) with clear messages | Callers can catch and react to specific failures instead of guessing what went wrong |
| File structure | One file, mixed concerns | `models.py` (data), `manager.py` (logic), `main.py` (entry point), `tests/` | Separates "what a task is" from "how tasks are managed" from "how the program runs" |
| Comparisons | `filter_priority != None` | `priority is None` | Matches Python convention for identity checks against `None` |
| Tests | None | 8 unit tests covering add/remove/complete/list/load, including failure cases | Confirms the refactor didn't change behavior, and guards against regressions |

## Rationale for key changes

- **Dataclass over dict**: the original `add_task` built a dict by hand with
  three separate assignment lines. A `Task` dataclass gives the same data a
  single typed definition, so every task is guaranteed to have the right
  fields with the right types.
- **Enum over free-text priority**: previously, a typo like `"hgih"` would
  have been silently accepted as a valid priority and just never matched
  anything in `show_tasks`. The `Priority` enum raises immediately instead.
- **Class over module globals**: `remove_task` used `global tasks`, which
  makes the function's behavior depend on hidden external state. Wrapping
  everything in `TaskManager` makes the dependency explicit (`self._tasks`)
  and makes the code testable in isolation (each test creates its own
  manager instance instead of sharing global state).
- **Specific exceptions over bare `except`**: the original `load_from_string`
  swallowed every possible error with a single generic message. The
  refactor raises `ValueError` with the exact malformed entry, and a
  dedicated `TaskNotFoundError` when an operation targets a task that
  doesn't exist — both are now things calling code can catch and handle
  deliberately, as shown in `main.py`'s `try/except` around `remove_task`.

## AI assistance disclosure

Portions of this refactor ( type hints and this README)
were produced with AI assistance and reviewed/tested by me before
submission. All tests pass and the script's output matches the original
script's behavior.