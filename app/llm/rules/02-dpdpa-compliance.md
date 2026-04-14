---
name: DPDPA Compliance (India)
description: Digital Personal Data Protection Act, 2023 (Act No. 22 of 2023) — mandatory compliance rules for all projects handling Indian user data.
alwaysApply: true
---

# DPDPA Compliance Rules (Digital Personal Data Protection Act, 2023)

**Authority**: Ministry of Electronics and Information Technology (MeitY), Government of India.
**Scope**: Applies to processing of digital personal data within India, and to processing outside India if related to offering goods or services to Data Principals in India.

## 1. Consent & Lawful Processing

1. **Informed Consent**: Personal data must only be processed after obtaining free, specific, informed, unconditional, and unambiguous consent from the Data Principal. Consent must be requested via a clear notice in plain language (English or any scheduled Indian language).
2. **Purpose Limitation**: Data collected for one stated purpose must not be processed for any other purpose without fresh consent.
3. **Consent Withdrawal**: Provide a mechanism at least as easy as the consent-granting mechanism for Data Principals to withdraw consent at any time. Upon withdrawal, cease processing and delete data.
4. **Consent Managers**: For systems at scale, integrate with registered Consent Managers who act as a single point of contact for Data Principals to manage, review, and withdraw consent.
5. **Legitimate Uses**: Processing without consent is permitted only for narrowly defined legitimate uses (e.g., state functions, legal obligations, medical emergencies, employment purposes). Never treat convenience as a legitimate use.

## 2. Data Fiduciary Obligations

1. **Data Minimization**: Collect only the personal data that is strictly necessary for the stated purpose. Do not collect "just in case" fields.
2. **Accuracy**: Ensure personal data is complete, accurate, and up-to-date, especially if used for decisions affecting the Data Principal or shared with other Data Fiduciaries.
3. **Storage Limitation**: Delete personal data once the purpose is fulfilled or consent is withdrawn, unless retention is required by law. Implement automated retention policies with TTLs.
4. **Security Safeguards**: Implement reasonable technical and organizational measures to protect personal data — encryption at rest (AES-256), in transit (TLS 1.3), access controls, and intrusion detection.
5. **Breach Notification**: Notify the Data Protection Board of India and each affected Data Principal without delay in the event of a personal data breach. Log breach metadata with immutable timestamps.
6. **Data Processor Contracts**: When using sub-processors, ensure contractual obligations flow down. The Data Fiduciary remains accountable for any processing done on its behalf.

## 3. Data Principal Rights

All systems must support the following rights via API or UI:

1. **Right to Access**: Data Principals can request a summary of their personal data being processed and the processing activities.
2. **Right to Correction & Erasure**: Provide mechanisms for Data Principals to correct inaccurate data or request complete erasure.
3. **Right to Grievance Redressal**: Implement a grievance mechanism. Acknowledge complaints within a defined SLA and resolve or escalate to the Data Protection Board.
4. **Right to Nominate**: Allow Data Principals to nominate another person to exercise their rights in case of death or incapacity.

## 4. Children's Data Protection

1. **Verifiable Parental Consent**: Before processing personal data of children (under 18), obtain verifiable consent from the parent or lawful guardian.
2. **No Behavioral Tracking**: Do not perform tracking, behavioral monitoring, or targeted advertising directed at children.
3. **No Detrimental Processing**: Do not process children's data in any manner that could cause harm to the child's well-being.

## 5. Significant Data Fiduciary (SDF) Requirements

If designated as an SDF by the Central Government:

1. **Data Protection Officer (DPO)**: Appoint a DPO based in India to represent the Data Fiduciary and serve as the point of contact for the Data Protection Board.
2. **Data Protection Impact Assessment (DPIA)**: Conduct periodic DPIAs for all high-risk processing activities.
3. **Independent Data Audit**: Appoint an independent data auditor to evaluate compliance annually.
4. **Algorithmic Transparency**: Ensure that algorithmic processing of personal data does not pose a risk to Data Principals' rights.

## 6. Cross-Border Transfer

1. **Data Localization**: The Central Government may restrict transfer of personal data to specific countries or territories via notification. Monitor the restricted list.
2. **Approved Jurisdictions Only**: Transfer personal data outside India only to jurisdictions explicitly permitted by the Central Government.

## 7. Penalties

Non-compliance penalties are severe:
- Failure to implement security safeguards: up to **₹250 crore** (~$30M USD).
- Failure to notify Data Protection Board of breach: up to **₹200 crore**.
- Non-compliance with obligations regarding children: up to **₹200 crore**.

## Agent Instructions

- When auditing code, verify all 7 sections above. Pay special attention to consent flows, data deletion pipelines, and breach notification mechanisms.
- Flag any hardcoded PII fields, missing consent gates, or absent retention/TTL logic as **Critical** severity.
- For SDF-designated projects, verify DPO contact integration, DPIA documentation, and independent audit hooks.
