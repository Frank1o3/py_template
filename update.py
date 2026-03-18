from pathlib import Path

from pytoml import dumps, loads

root = Path(__file__).parent
print(str(root))

pyproject = root / "pyproject.toml"
src = root / "src"
tests_app = root / "test" / "test_app.py"

new_name = input("What's the name of your repo? ").lower() or "project_name"

data = loads(pyproject.read_text("utf-8"))
data["project"]["name"] = new_name
data["tool"]["poetry"]["scripts"]["app"] = f"{new_name}.__main__:app"
pyproject.write_text(dumps(data), encoding="utf-8")

project_dir = src / "project_name"
project_dir.rename(project_dir.parent / new_name)

py_code = tests_app.read_text("utf-8")
py_code = py_code.replace("project_name", new_name)
tests_app.write_text(py_code, encoding="utf-8")

Path(__file__).unlink(missing_ok=True)
