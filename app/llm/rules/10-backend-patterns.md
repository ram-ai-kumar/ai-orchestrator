---
name: Enterprise Backend Policy
description: Rules for high-concurrency, observable, and secure backend services.
---

# Backend Engineering Policy (2026 Standard)

## 1. Concurrency & I/O

- **Async-First**: All I/O-bound operations (Database, Network, FS) must use non-blocking asynchronous patterns.
- **Graceful Degradation**: Implement circuit breakers for all downstream service calls. Never allow a downstream failure to cascade and block the event loop/thread pool.
- **Concurrency**: Prefer message-passing (Go channels/Rust actors) over shared mutable state.

## 2. API & Interoperability

- **Schema-First**: All APIs (gRPC/REST/GraphQL) must be defined by versioned schemas (Protobuf/OpenAPI). Code generation must be used to ensure client/server contract alignment.
- **Versioning**: Breaking changes require a new major version (e.g., `/v2/`). Parallel support for the previous version is required for 2 minor release cycles.
- **Idempotency**: All `POST`/`PUT` endpoints must implement idempotency using a client-generated `Request-ID` header.

## 3. Observability & Reliability

- **Telemetry**: Every service must emit traces via OpenTelemetry. Logs must be structured (JSON) and include a `trace_id` and `span_id` for cross-service request correlation.
- **Health Checks**: Implement `/health/live` and `/health/ready` endpoints. Readiness probes must verify downstream dependencies (DB/Cache).
- **Anti-Pattern**: Never swallow exceptions. Every caught exception must be logged at `ERROR` level with stack trace and request context.
