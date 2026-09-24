# Python Coding Rules

These rules apply to the Python code in the `core` package.

## Style

- Follow PEP 8 and use four spaces for indentation.
- Use `snake_case` for modules, functions, methods, and variables.
- Use `PascalCase` for classes and `UPPER_CASE` for constants.
- Group imports into standard library, third-party, and local imports.
- Remove unused imports and keep names descriptive.

## Types and API

- Add type hints to public functions and methods, including return types.
- Add docstrings to public classes and methods when their behavior is not obvious.
- Keep the `core` package independent from web-framework concerns.
- Keep `MyBigNumber.log` consistent: reset it at the start of every `sum()` call.

## Validation and Errors

- Accept only non-negative digit strings in `MyBigNumber.sum()`.
- Raise a clear, specific exception for invalid input.
- Do not use `assert` for input validation.
- Catch exceptions only when they can be handled meaningfully; do not hide errors with
  a broad `except Exception`.

## Logging and Performance

- Use `logging`, not `print()`, for library diagnostics.
- Avoid unnecessary copies and intermediate collections when processing large numbers.
- Keep `LOG_STEP_LIMIT` effective so detailed logging cannot use unbounded memory.
- Do not log unnecessarily large or sensitive values.
