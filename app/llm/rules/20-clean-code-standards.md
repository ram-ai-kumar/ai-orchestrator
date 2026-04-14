---
name: Enterprise Clean Code Standards
description: Rules for testing, security, and performance-first development.
alwaysApply: true
---

# Coding Standards

## 1. The Testing Pyramid (Required)

All features must include the following test suite types:

1. **Smoke Tests**: Verify the critical path of the feature works in the deployment environment.
2. **Negative Tests**: Explicitly test failure modes (e.g., passing invalid types, unauthorized headers).
3. **Edge Case Tests**: Test boundary conditions (e.g., empty strings, null values, max integer limits, array length 0).
4. **Exception Tests**: Verify that the system handles, logs, and recovers from thrown exceptions gracefully without crashing.

## 2. Security-First Coding

1. **Input Validation**: Never trust user input. Use schema-based validation (e.g., Zod, Joi) at the controller/entry point layer.
2. **Sanitization**: Sanitize all inputs before database or filesystem interaction to prevent SQLi and NoSQLi.
3. **Fail-Safe**: If a security check fails, the default state must be "Access Denied."

## 3. Performance & Resource Management

1. **Async by Default**: All I/O operations (Database, API, File system) must be asynchronous.
2. **Complexity Analysis**: Aim for $O(n)$ or better for data processing. Document $O(n^2)$ or higher complexity functions with justifications.
3. **Memory Management**: For long-running processes, ensure no memory leaks occur in closures. Dispose of resources (file handles, sockets) using `try...finally` or `using` statements.

## 4. Maintainability

1. **Type Safety**: Prefer strict typing. Avoid `any` types at all costs.
2. **JSDoc/TypeDocs**: Document the 'why' (intent) for complex business logic. The 'what' should be visible in the code structure.
3. **DRY (Don't Repeat Yourself)**: If logic appears twice, keep it. If it appears three times, refactor into a shared, tested utility.
