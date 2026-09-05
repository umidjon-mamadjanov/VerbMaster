# VerbMaster Pro

A modular Kivy irregular-verb learning app.

## Structure

- `main.py` — dependency composition and application startup
- `core/` — constants, theme and utilities
- `data/` — models and persistence repository
- `services/` — quiz and statistics business logic
- `screens/` — UI screens
- `widgets/` — reusable UI components
- `assets/fonts/` — Font Awesome font
- `storage/` — local statistics

## Important

Keep your existing `verbs.py` in the project root:

```text
VerbMaster/
├── main.py
├── verbs.py
├── ui.kv
...
```

`verbs.py` must expose:

```python
verbs = {
    ...
}
```

## Run

```bash
python -m py_compile main.py
python main.py
```

## SOLID

The application separates:

- presentation
- business logic
- data models
- persistence

`QuizService` does not depend on Kivy.
`StatsService` does not depend on Kivy.
`JsonStatsRepository` can later be replaced with SQLite/PostgreSQL without changing the screens.
