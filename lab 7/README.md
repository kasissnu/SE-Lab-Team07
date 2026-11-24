# Lab 7 — Fuzz Testing with Hypothesis

This lab uses Hypothesis property-based tests to find input-validation bugs in
the ski resort pass processor.

## Files

| File | Description |
| --- | --- |
| `processor.py` | Hardened application code |
| `test_processor.py` | Hypothesis fuzz tests and regression tests |
| `lab7_fuzz_testing_evidence.pdf` | Run evidence and results |

## Run

From this folder:

```bash
python -m pip install -r requirements.txt
python processor.py
python -m pytest test_processor.py
```

Invalid inputs are handled without uncaught exceptions. Invalid dates return an
explanatory message; invalid gradients and unknown lift zones return `None`.
