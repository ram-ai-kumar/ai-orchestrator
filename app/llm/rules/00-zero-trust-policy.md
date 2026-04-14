---
name: Zero-Trust Manifesto
description: Mandatory architectural and security principles for all code, infrastructure, and deployment.
alwaysApply: true
---

# Zero-Trust & Zero-X Operational Manifesto

All architectural decisions, code changes, and infrastructure configurations must adhere to the "Zero-X" principles below. If a proposed change violates these, the agent must flag it as a critical security risk.

## I. Security & Access Principles (The "Security 10")

1. **Zero-Trust**: Assume the network is hostile. Verify explicitly at every request/identity boundary.
2. **Zero-Knowledge**: Never store plaintext sensitive data. Use end-to-end encryption or hashing/salting where data does not need to be read by the server.
3. **Zero-Standing-Privileges**: Access is Just-In-Time (JIT) and ephemeral. No long-lived admin credentials in production.
4. **Zero-Permissiveness**: Default state is "Deny All." Grant only the explicit scope required for the task.
5. **Zero-Shared-Accounts**: Identity must be granular. Services and users are unique and non-repudiable.
6. **Zero-Static-Rules**: Policies (IAM, firewall, access) must be dynamic and policy-as-code, never manual config.
7. **Zero-Perimeter-Reliance**: The network boundary is irrelevant. Focus on identity and data security, not IP whitelisting.
8. **Zero-Data-Leakage**: PII/PHI must be masked in transit, in logs, and at rest.
9. **Zero-Secrets**: Secrets must never exist in code, env vars, or logs. Use a Vault/Key Management Service.
10. **Zero-Residual-Access**: Access rights must be revoked immediately upon session termination or project completion.

## II. Automation & Operational Principles (The "Operational 8")

11. **Zero-Touch**: Automation must handle all provisioning. No human interaction required to scale or deploy.
12. **Zero-Admin**: Design services to be self-healing and self-scaling. The system should manage itself.
13. **Zero-Manual-Intervention**: All operational tasks (patching, scaling, recovery) must be fully automated pipelines.
14. **Zero-Downtime**: Deployments, migrations, and updates must occur while maintaining 99.99% availability.
15. **Zero-Over-provisioning**: Infrastructure must scale on demand based on actual load metrics.
16. **Zero-Hard-coding**: All configurations must be externalized, versioned, and injected at runtime.
17. **Zero-Complexity**: Favor simplicity. If a module cannot be explained in two sentences, it is too complex.
18. **Zero-Legacy-Tech**: Avoid technical debt accumulation. Refactor legacy bottlenecks immediately.

## III. Architectural & Data Principles (The "Systems 7")

19. **Zero-Local-Data**: Services should be stateless. No data should live in local containers; use distributed stores.
20. **Zero-Latency**: Architect for predictable performance. All I/O must be non-blocking and optimized for low-latency.
21. **Zero-Visibility-Gaps**: Every action must be traced. If it happened, it must be observable in our logs/metrics.
22. **Zero-External-Dependencies**: Minimize supply chain risk. Vet every 3rd-party library/container carefully.
23. **Zero-Trust-as-Code**: Infrastructure security policies must be validated by automated CI/CD checks (e.g., OPA).
24. **Zero-Redundancy-Gaps**: Ensure no single point of failure. Every critical path must have N+1 redundancy.
25. **Zero-Context-Switching**: Coding standards must be so uniform that any developer can jump into any module without needing an onboarding session.

## IV. Agent Instructions

- When auditing code, evaluate it against these 25 principles.
- Use the `/security-review` command to trigger an audit against these specific "Zero-X" principles.
- If a principle is violated (e.g., hard-coded credentials or static access rules), provide a remediation path that aligns with Zero-Trust.
