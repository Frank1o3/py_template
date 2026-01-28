# Python Poetry Template

A minimal, strict Python project template using **Poetry**, **pytest**, **ruff**, and **mypy**.

This repository is intended to be used as a **GitHub template** for starting new Python projects with a clean structure and modern tooling.

---

## Features

- 📦 Poetry for dependency and environment management
- 🧪 Pytest for testing
- 🧹 Ruff for linting and formatting
- 🔍 Mypy with strict type checking
- 📁 `src/`-based project layout
- 🚀 Optional CLI entry point

---

## Project Structure

```text
.
├── src/
│ └── project_name/
│ ├── init.py
│ ├── main.py
│ └── core.py
├── tests/
│ └── test_import.py
├── pyproject.toml
├── ruff.toml
├── mypy.ini
└── README.md
```

---

## Using This Template

1. Click **“Use this template”** on GitHub.
2. Rename the package:
   - `src/project_name/` → `src/your_package_name/`
3. Update the following files:
   - `pyproject.toml`
     - `name`
     - `[tool.poetry.scripts]`
   - `tests/test_import.py`

     ```python
     import your_package_name
     ```

   - `ruff.toml`

     ```toml
     known-first-party = ["your_package_name"]
     ```

4. Install dependencies:

```bash
poetry install
poetry run python -m your_package_name
```

If you enabled the script entry point:

```bash
poetry run your-project-name
```

Testing

```bash
poetry run pytest
```

Linting & Type Checking

```bash
poetry run ruff check .
poetry run mypy .
```

License
MIT
