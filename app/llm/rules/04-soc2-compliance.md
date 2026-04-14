---
name: SOC 2 Compliance
description: AICPA Trust Service Criteria (TSC) — Security, Availability, Processing Integrity, Confidentiality, Privacy. Enable per-project for SaaS audits.
alwaysApply: false
---

# SOC 2 Compliance Rules (AICPA Trust Service Criteria, 2017)

**Authority**: American Institute of Certified Public Accountants (AICPA).
**Scope**: Applies to service organizations that store, process, or transmit customer data. SOC 2 reports are issued by independent CPA auditors.

## Report Types

- **SOC 2 Type I**: Point-in-time assessment — evaluates control design at a specific date.
- **SOC 2 Type II**: Period-of-time assessment — evaluates control design AND operating effectiveness over a review period (typically 6–12 months). Type II is the industry standard for customer trust.
- **SOC 3**: A public-facing summary of SOC 2 results (no detailed control descriptions). Suitable for marketing and general assurance.

## 1. Security (Common Criteria — MANDATORY)

Security is required for every SOC 2 audit. All other criteria are optional.

1. **Logical Access Controls**: Implement authentication, authorization, and access management. Enforce MFA for privileged access and external-facing systems.
2. **System Boundary Definition**: Clearly define system boundaries — which infrastructure, software, people, procedures, and data are in scope.
3. **Risk Assessment**: Perform and document risk assessments identifying threats to confidentiality, integrity, and availability of customer data.
4. **Change Management**: All changes to production systems must follow a documented change management process — approvals, testing, and rollback plans.
5. **Monitoring & Detection**: Implement continuous monitoring for security events. Use SIEM or equivalent for alerting on anomalous activity.
6. **Incident Response**: Document and test incident response procedures. Include escalation paths, communication templates, and post-incident review.
7. **Vendor Management**: Assess and monitor third-party service providers. Ensure vendors meet equivalent security controls via contractual obligations.

## 2. Availability (Optional)

1. **Uptime SLAs**: Define and publish uptime commitments (e.g., 99.9%, 99.99%). Monitor and report against SLAs.
2. **Capacity Planning**: Monitor system capacity and scale proactively. Document capacity thresholds and scaling triggers.
3. **Disaster Recovery**: Maintain DR plans with defined RTO (Recovery Time Objective) and RPO (Recovery Point Objective). Test at least annually.
4. **Redundancy**: Eliminate single points of failure for critical paths. Implement N+1 redundancy for compute, storage, and networking.
5. **Incident Communication**: Maintain a public or client-facing status page for real-time availability reporting.

## 3. Processing Integrity (Optional)

1. **Data Accuracy**: Implement input validation and processing checks to ensure data is complete, valid, accurate, and timely.
2. **Error Handling**: Detect, log, and correct processing errors. Implement reconciliation mechanisms for critical data flows (e.g., financial transactions).
3. **Output Verification**: Verify processing outputs against expected results. Implement checksums or hash verification for data pipeline stages.
4. **Authorization Checks**: Ensure all data processing is authorized — no processing occurs without explicit upstream trigger or approval.

## 4. Confidentiality (Optional)

1. **Data Classification**: Classify data by sensitivity level (Public, Internal, Confidential, Restricted). Apply controls proportional to classification.
2. **Encryption**: Encrypt confidential data at rest (AES-256) and in transit (TLS 1.3). Enforce encryption at the application layer, not just infrastructure.
3. **Access Restriction**: Limit access to confidential data to authorized personnel only. Implement need-to-know access controls.
4. **Secure Disposal**: Implement cryptographic erasure or secure overwrite for confidential data at end of lifecycle. Log disposal events.
5. **NDA & Contractual Controls**: Ensure workforce and third parties handling confidential data are bound by confidentiality agreements.

## 5. Privacy (Optional)

1. **Privacy Notice**: Publish a clear privacy notice describing data collection, use, retention, and disclosure practices. Keep it current.
2. **Consent Management**: Collect, record, and honor consent preferences. Provide opt-out mechanisms where applicable.
3. **PII Minimization**: Collect only the PII necessary for the stated purpose. Do not repurpose PII without fresh consent.
4. **Data Subject Rights**: Support access, correction, deletion, and portability requests for PII. Respond within contracted or statutory timelines.
5. **Retention & Disposal**: Define and enforce retention schedules for PII. Automate deletion when retention periods expire.
6. **Third-Party Disclosure**: Disclose PII to third parties only with consent or legal basis. Maintain a register of all third-party data sharing.

## Agent Instructions

- This policy is **opt-in**. It applies only when enabled for projects undergoing SOC 2 certification.
- Security (Common Criteria) is always in scope. When auditing, verify all 7 items under Security first.
- For projects claiming Availability, verify SLAs, DR plans, and redundancy. For Processing Integrity, verify input validation and reconciliation.
- Flag missing change management, absent monitoring, or undocumented incident response as **High** severity.
