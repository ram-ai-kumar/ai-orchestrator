---
name: Enterprise Data Policy
description: Rules for PostgreSQL, Redis/Dragonfly, and NoSQL storage.
alwaysApply: true
---

# Data Persistence Policy (2026 Standard)

## 1. Relational (PostgreSQL)

- **ACID Compliance**: All business transactions must be wrapped in explicit transactions.
- **Query Optimization**: Every query must be explain-analyzed before production. Use covering indexes for high-frequency queries.
- **Migrations**: Database migrations must be atomic. Write-ahead logging (WAL) considerations must be documented for long-running schema changes.

## 2. Caching (Redis/Dragonfly)

- **TTL Enforcement**: No key is allowed in cache without a TTL (Time-To-Live). Default TTL must be defined based on data volatility.
- **Consistency**: Use "Cache-Aside" pattern. For read-heavy systems, use "Write-Through" with careful invalidation logic.
- **Anti-Pattern**: Never use Redis as the system of record. It is a secondary optimization layer.

## 3. Data Privacy

- **PII Obfuscation**: Personal identifiable data (PII) must be encrypted at the application level _before_ persistence. The database should only store encrypted blobs for fields defined in the PII catalog.
- **Soft Deletes**: Use `deleted_at` timestamps for data recovery; hard deletes are reserved for GDPR/DPDPA "Right to be Forgotten" requests.
