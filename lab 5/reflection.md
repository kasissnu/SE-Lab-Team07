# Static Analysis Reflection

## 1. What is the purpose of static code analysis, and how did it help in this lab?

Static analysis examines source code without running every possible execution path. In this lab it found defects that were easy to overlook during a short manual run: the shared mutable default argument, the bare exception handler, the unsafe temporary-file API, and the assertion used as runtime validation. It also provided consistent style and documentation feedback through Pylint and Flake8. This made the review more systematic than relying only on observed output.

## 2. Which finding was most important, and why?

The `tempfile.mktemp()` finding was the most important security issue because it creates a race condition around a file path. A different process could create or replace the file before the program writes to it. The mutable default argument was the most important correctness issue because it silently shared state across calls. I prioritized both before cosmetic style changes.

## 3. What challenges did you encounter while fixing the issues?

The main challenge was preserving the program's behavior while removing unsafe patterns. Replacing `logs=[]` with `None` prevents state leakage, but the program still needs a single registration log for its per-run count, so `main` now passes that list explicitly. Replacing the negative interval also required choosing valid input because the cleaned function now rejects invalid intervals. Finally, I had to rerun all three tools after formatting changes because a single long line was still enough to fail Flake8 even after the larger fixes were complete.

## 4. How will you use static analysis in future projects?

I would run the analyzers automatically in a pre-commit hook and in continuous integration, before code review. I would treat Bandit security findings and correctness warnings as release-blocking until reviewed, while keeping the style configuration consistent across the project. I would also use the reports as a starting point for tests and manual review rather than assuming that a clean report proves the program is correct. Static analysis cannot reliably detect every business-rule error, such as the starter program's empty asset ID or duplicate asset registration.

