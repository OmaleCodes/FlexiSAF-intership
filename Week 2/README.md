# Week 2 — Advanced Functions, Iteration & Resource Management

Three reusable components demonstrating first-class functions, decorators,
generators, and a custom context manager — plus tests for each.


## How to run

```bash
pip install -r requirements.txt
PYTHONPATH=. python main.py
```

## How to run the tests

```bash
PYTHONPATH=. pytest tests/ -v
```

## What each piece demonstrates

### Decorators 
- `@timed` wraps any function and logs how long it took to run, without
  changing its return value or signature (`functools.wraps` preserves the
  original function's name and docstring).
- `@retry(times=3, delay=0.1)` is a decorator *factory* — it takes arguments
  and returns a decorator. It retries the wrapped function on any exception,
  waiting `delay` seconds between attempts, and re-raises the last error if
  every attempt fails.

### Generator-based processor 
- `process_readings()` is a generator: it parses lines one at a time with
  `yield`, instead of building a full list upfront. Invalid lines are
  skipped rather than crashing the whole batch.
- `running_average()` is also lazy — it consumes another generator and
  yields a running average as values arrive, so it never needs to hold the
  full dataset in memory. This matters if the input were a large file
  instead of six sample lines.

### Custom context manager 
- `managed_resource()` uses `@contextlib.contextmanager` to guarantee a
  resource is opened before use and closed afterward — including when an
  exception is raised inside the `with` block. This is verified directly in
  `test_resource_closes_even_on_exception`, which raises an error inside the
  `with` block and then checks the resource was still closed.

## Why generators here instead of lists

Building `process_readings()` as a generator instead of returning a list
means nothing is parsed until it's actually requested — useful for an
unknown-sized or very large input, where building the whole list upfront
would use unnecessary memory. For this small sample it works identically
either way, but the lazy version scales to inputs a plain list-based version
wouldn't handle as cleanly.
