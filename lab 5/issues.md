# Static Analysis Issue Table

The baseline scan was run against the starter version of `maintenance_system.py` on 10 November 2026. The final scan was run after the fixes below. High- and medium-impact findings are listed first.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| `tempfile.mktemp()` | Bandit B306, medium | 40 | Creates a temporary path without reserving the file, creating a race condition in which another process could use the path first. | Replaced it with `NamedTemporaryFile(..., delete=False)`, which creates the file safely and returns its unique path. |
| Bare `except` | Pylint W0702 / Flake8 E722, medium | 18 | Catches every exception, including programming errors, and makes diagnosis difficult. | Catch only `KeyError` and `ValueError`, the two expected errors for asset lookup and date validation. |
| Mutable default argument `logs=[]` | Pylint W0102, high | 10 | The same list is shared across calls, so registrations from one call leak into later calls. | Changed the default to `None`, created a list when needed, and passed one explicit run-level log from `main`. |
| `assert` used for runtime validation | Bandit B101, low | 61 | Assertions can be removed with optimized Python execution, so they should not enforce application behavior. | Replaced the assertion with an explicit `RuntimeError` check. |
| File handles not managed with `with` | Pylint R1732 | 34 and 41 | Files may remain open if an exception occurs before `close()` runs. | Used context managers for both report and scratch-file writes. |
| File encoding omitted | Pylint W1514 | 34 and 41 | Text output depends on the host platform's default encoding. | Specified UTF-8 explicitly for both files. |
| Unused `logging` import | Pylint W0611 / Flake8 F401 | 2 | Adds dead code and signals that logging was intended but never used. | Removed the unused import. |
| Missing module and function docstrings | Pylint C0114 / C0116 | 1, 10, 15, 21, 29, 33, 39, 46, 50 | Public code had no explanation of its purpose or behavior. | Added a module docstring and concise docstrings for every function. |
| Non-snake-case `printAlerts` | Pylint C0103 | 46 | Violates Python naming conventions and makes the function inconsistent with the rest of the module. | Renamed it to `print_alerts`. |
| Iterating over dictionary keys and indexing again | Pylint C0206 | 23 | Less direct and less readable than iterating over key/value pairs. | Changed the loop to `for asset_id, asset in assets.items()`. |
| PEP 8 spacing and line length | Flake8 E302, E305, E501 | 10, 11, 15, 21, 29, 33, 39, 46, 66 | Functions were not separated by two blank lines, and several lines exceeded 79 characters. | Reformatted the module to meet Flake8's default style rules. |

## Verification

| Tool | Baseline | Final |
|---|---|---|
| Pylint | 6.55/10 with 18 findings | 10.00/10 |
| Bandit | 1 medium and 1 low finding | No issues identified |
| Flake8 | 12 findings | No issues identified |

