---
name: Python Patterns
description: Language-specific best practices for Python projects (Django, FastAPI, scripts) — enforced by audit-code-quality and verify-code-quality.
alwaysApply: false
---

# Python Patterns

Detected via: `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `manage.py`, `main.py`

## 1. Code Style & Typing

1. **Ruff enforced**: Use `ruff check .` as the primary linter (replaces flake8, isort, pyupgrade). Zero violations tolerated. Config lives in `pyproject.toml`.
2. **Black formatting**: `black --check .` in CI. No manual formatting debates.
3. **Type annotations on all functions**: Every function must have typed parameters and return type. No bare `def foo(x):`.
   ```python
   # BAD
   def get_user(user_id):
       ...
   # GOOD
   def get_user(user_id: int) -> User | None:
       ...
   ```
4. **Mypy strict mode**: Run `mypy --strict`. Zero errors. Use `# type: ignore` only with a trailing explanation comment.
5. **No `Any` without justification**: `from typing import Any` must be a last resort. Document why at the point of use.
6. **Pydantic for all data boundaries**: Every external input (API request, env var, config file, message queue payload) must be parsed through a Pydantic model before use.

## 2. Project Structure

1. **`pyproject.toml` as single config file**: All tool config (mypy, ruff, pytest, black) lives here. No separate `.flake8`, `setup.cfg`, `mypy.ini`.
2. **Dependency pinning**: Use `uv` or `pip-tools`. Lock files (`requirements.lock` or `uv.lock`) must be committed. CI uses `--frozen` installs.
3. **Virtual environment**: Always project-scoped (`.venv/`). Never install to system Python.
4. **Module structure**:
   ```
   src/
     mypackage/
       __init__.py
       models/
       services/
       api/
       core/
   tests/
   ```
   Use `src/` layout to prevent import ambiguity.

## 3. Django-Specific Patterns

### Models
1. **`blank=True` vs `null=True` discipline**: `null=True` only for non-string fields. String fields use `blank=True, default=""`. Never both on string fields.
2. **Custom managers for filtered querysets**: Use managers to encapsulate common filters (e.g., `ActiveManager`, `TenantManager`).
3. **`select_related` and `prefetch_related`**: All views/serializers touching related models must explicitly prefetch. Use `django-zen-queries` in dev to catch lazy loads.
4. **Tenant isolation via middleware**: Every request must have `request.tenant` set by middleware. All querysets must filter by tenant.
5. **Migrations**: Generated with `makemigrations --check` in CI (fails if models differ from migrations). Every migration must be reviewed for table lock risk.

### Views & Serializers (DRF)
1. **Class-based views (APIView or ViewSet)**: No function-based views in APIs. Consistent permission classes on every view.
2. **Serializer validation**: Use `serializer.is_valid(raise_exception=True)`. Never bypass validation.
3. **`get_queryset()` over `queryset` attribute**: Always override `get_queryset()` to apply tenant scoping and permissions dynamically.
4. **Pagination required**: Register `DEFAULT_PAGINATION_CLASS` globally. No view may return unbounded querysets.

## 4. FastAPI-Specific Patterns

1. **Pydantic v2 models for all request/response schemas**: Separate `RequestModel` and `ResponseModel` — never expose ORM models directly.
2. **Dependency injection for all shared resources**: DB sessions, authentication, tenant context — via `Depends()`. Never create DB sessions inside route handlers.
3. **Lifespan context manager**: Use `@asynccontextmanager` lifespan for startup/shutdown (connection pools, caches). No `@app.on_event`.
4. **Background tasks for non-blocking work**: Use `BackgroundTasks` or Celery for email, webhooks, reports. Never block the event loop.
5. **Async all the way**: All route handlers must be `async def`. DB calls must use async drivers (`asyncpg`, `sqlalchemy[asyncio]`).

## 5. Security

1. **No `eval()` or `exec()`**: Prohibited unconditionally. Flag as Critical.
2. **No `subprocess` with `shell=True`**: Always use `shell=False` with a list of arguments. Prevents shell injection.
3. **`bandit` scan**: Run `bandit -r src/ -ll` in CI. Zero medium/high findings.
4. **Secret management**: Never read secrets from environment variables directly in business logic. Use a `Settings` Pydantic model with `model_config = SettingsConfigDict(env_file='.env')`. In production, inject from vault.
5. **SQL injection**: Always use ORM query builders or parameterized queries. Never format user input into SQL strings.
6. **Path traversal**: Validate and sanitize all file paths. Use `pathlib.Path.resolve()` and confirm the result is within the expected base directory.
7. **SSRF prevention**: Never make HTTP requests to user-supplied URLs without allowlist validation.

## 6. Async & Concurrency

1. **`asyncio` for all I/O**: File reads, HTTP calls, DB queries must be `async/await`. Never use `time.sleep()` in async code — use `asyncio.sleep()`.
2. **No mixing sync and async**: Never call sync blocking functions from an async context. Use `asyncio.to_thread()` when bridging is unavoidable.
3. **Task cancellation handling**: Always handle `asyncio.CancelledError` in long-running tasks. Clean up resources in `finally` blocks.
4. **Connection pool sizing**: Configure pool size explicitly for DB and HTTP clients. Never use default unbounded pools in production.

## 7. Error Handling

1. **Never `except Exception: pass`**: Every exception must be logged with `logger.exception()` (includes traceback) and either re-raised or returned as a structured error.
2. **Custom exception hierarchy**: Define `AppError(Exception)` → domain-specific errors. Catch and translate at API boundaries.
3. **Structured logging**: Use `structlog` or `python-json-logger`. Every log entry must include `request_id`, `tenant_id`, and the relevant entity ID.
4. **No PII in logs**: Mask email, phone, national ID, payment data before logging. Use a log sanitizer in the logging pipeline.

## 8. Testing (pytest)

1. **pytest with `pytest-asyncio` for async tests**: All async test functions decorated with `@pytest.mark.asyncio`.
2. **Fixtures over setUp**: Use `conftest.py` fixtures with appropriate scope (`session`, `module`, `function`).
3. **`pytest-cov` coverage gate**: Minimum 80% line coverage enforced in CI. Coverage report must be committed as artifact.
4. **`factory_boy` for test data**: No hard-coded test objects. Factories declared in `tests/factories/`.
5. **`responses` or `httpretty` for HTTP mocking**: Never make real external HTTP calls in tests.
6. **Negative tests**: Every endpoint must have tests for: unauthenticated (401), forbidden (403), invalid input (422), not found (404).

## 9. Dependency Management

1. **`pip-audit` or `safety`**: Run in CI. Zero known CVEs tolerated.
2. **Pin all direct and transitive deps**: Use lock files. No floating `>=` version specs in production.
3. **Review before adding**: Every new package must be evaluated for maintenance status, CVE history, and necessity.
