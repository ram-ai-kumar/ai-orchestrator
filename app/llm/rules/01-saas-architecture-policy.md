---
name: Enterprise SaaS Architecture
description: Architecture constraints for Zero-Trust, HIPAA, DPDPA, ISO, and SOC compliance.
alwaysApply: true
---

# SaaS Architecture Rules

## 1. Security & Zero-Trust

1. **Identity as the Perimeter**: Never assume network safety. Every request must be authenticated, authorized, and encrypted (TLS 1.3+).
2. **Micro-segmentation**: Isolate services. Assume an internal breach is possible; limit "blast radius" by restricting inter-service communication to only required APIs.
3. **Least Privilege**: Services must run with the minimum IAM permissions necessary. Use ephemeral, scoped credentials.

## 2. Compliance Frameworks

Compliance rules are maintained as individual policy files. Enable per-project as needed.

| Framework                 | File                         | Default              |
| ------------------------- | ---------------------------- | -------------------- |
| **DPDPA** (India)         | `@02-dpdpa-compliance.md`    | ✅ Always ON          |
| **HIPAA** (US Healthcare) | `@03-hipaa-compliance.md`    | ⬜ Manual per-project |
| **SOC 2/3** (AICPA)       | `@04-soc2-compliance.md`     | ⬜ Manual per-project |
| **ISO 27001** (ISMS)      | `@05-iso27001-compliance.md` | ⬜ Manual per-project |

**Baseline requirements** (always enforced regardless of framework):
1. **Audit Trails**: Every API interaction must be logged with immutable timestamps, user identity, and action taken.
2. **Encryption**: Data at rest must use AES-256. Data in transit must use TLS 1.3.
3. **PII/PHI**: Sensitive data (PHI/PII) must be masked in logs. Never log raw sensitive data.

## 3. Enterprise Scalability

1. **Observability**: Implement distributed tracing (e.g., OpenTelemetry) for every request across microservices.
2. **Infrastructure as Code (IaC)**: All infrastructure must be defined in version-controlled code (e.g., Terraform/Pulumi). Manual changes ("ClickOps") are forbidden.
3. **Disaster Recovery**: Define RTO (Recovery Time Objective) and RPO (Recovery Point Objective) for all critical services. Assume zone failures.

## 4. Billing & Trust

1. **Financial Precision**: All financial modules must use arbitrary-precision arithmetic. No floating-point math for transactions.
2. **Transaction Integrity**: Implement Idempotency keys for all payment/transaction APIs to prevent double-billing.
