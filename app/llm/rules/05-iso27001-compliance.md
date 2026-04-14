---
name: ISO 27001 Compliance
description: ISO/IEC 27001:2022 Information Security Management System — Annex A controls. Enable per-project for ISO certification.
alwaysApply: false
---

# ISO 27001:2022 Compliance Rules (Annex A Controls)

**Authority**: International Organization for Standardization (ISO) / International Electrotechnical Commission (IEC).
**Scope**: Applies to organizations implementing an Information Security Management System (ISMS). ISO 27001:2022 is the current version with 93 Annex A controls across 4 themes.

## Statement of Applicability (SoA)

A mandatory certification document. For each of the 93 Annex A controls below, the project must document:
- Whether the control is **applicable** to the project scope.
- If excluded, the **justification** for exclusion.
- The **implementation status** of each applicable control.

## 1. Organizational Controls (A.5 — 37 controls)

### Governance & Policy

1. **A.5.1 — Policies for Information Security**: Define, publish, and review information security policies approved by management.
2. **A.5.2 — Information Security Roles**: Assign clear information security responsibilities. Segregate conflicting duties.
3. **A.5.3 — Segregation of Duties**: No single individual should control all aspects of a critical function.
4. **A.5.4 — Management Responsibilities**: Ensure management actively enforces security policy compliance.

### Risk & Threat Management

5. **A.5.7 — Threat Intelligence** *(NEW in 2022)*: Collect and analyze threat intelligence relevant to the organization's threat landscape. Integrate feeds into monitoring and response.
6. **A.5.8 — Information Security in Project Management**: Integrate security requirements into every phase of the project lifecycle — not as an afterthought.

### Access & Identity

7. **A.5.15 — Access Control**: Implement access control policies based on business and security requirements.
8. **A.5.16 — Identity Management**: Manage the full lifecycle of identities (provisioning, modification, de-provisioning). Eliminate orphaned accounts.
9. **A.5.17 — Authentication Information**: Protect authentication credentials. Enforce password policies, MFA, and credential rotation.
10. **A.5.18 — Access Rights**: Grant access on a need-to-know basis. Review access rights at defined intervals and upon role changes.

### Supplier & Third-Party

11. **A.5.19 — Information Security in Supplier Relationships**: Assess supplier security posture before engagement. Include security requirements in contracts.
12. **A.5.20 — Addressing Security in Supplier Agreements**: Define SLAs, audit rights, incident notification obligations, and data handling requirements.
13. **A.5.21 — Managing Security in the ICT Supply Chain**: Extend security requirements across the entire supply chain, not just tier-1 suppliers.

### Incident & Continuity

14. **A.5.24 — Incident Management Planning**: Establish procedures for detecting, reporting, assessing, and responding to security incidents.
15. **A.5.25 — Assessment of Security Events**: Classify security events by severity and determine which qualify as security incidents.
16. **A.5.26 — Response to Security Incidents**: Respond according to documented procedures. Contain, eradicate, and recover.
17. **A.5.28 — Collection of Evidence**: Preserve evidence for potential legal action or regulatory investigation. Maintain chain of custody.
18. **A.5.29 — Information Security During Disruption**: Ensure security controls remain effective during business disruptions or crises.
19. **A.5.30 — ICT Readiness for Business Continuity**: Align ICT continuity with business continuity requirements. Define RTO/RPO.

### Compliance

20. **A.5.31 — Legal, Statutory, and Contractual Requirements**: Identify and document all legal and regulatory requirements applicable to the ISMS scope.
21. **A.5.34 — Privacy and Protection of PII**: Comply with applicable privacy legislation. Implement data protection by design and by default.
22. **A.5.35 — Independent Review of Information Security**: Conduct independent reviews of the ISMS at planned intervals.
23. **A.5.36 — Compliance with Policies and Standards**: Regularly verify compliance with organizational security policies and standards.

## 2. People Controls (A.6 — 8 controls)

1. **A.6.1 — Screening**: Conduct background verification checks on all candidates proportional to the role's access level.
2. **A.6.2 — Terms & Conditions of Employment**: Include information security responsibilities in employment contracts.
3. **A.6.3 — Information Security Awareness & Training**: Provide regular security awareness training tailored to roles.
4. **A.6.4 — Disciplinary Process**: Enforce a formal disciplinary process for security policy violations.
5. **A.6.5 — Responsibilities After Termination**: Security obligations (NDA, IP, credential return) must survive employment termination.
6. **A.6.6 — Confidentiality Agreements**: Require signed confidentiality agreements from all personnel and third parties.
7. **A.6.7 — Remote Working**: Define and enforce security measures for remote work (VPN, endpoint protection, secure Wi-Fi).
8. **A.6.8 — Information Security Event Reporting**: All personnel must report observed or suspected security events without delay.

## 3. Physical Controls (A.7 — 14 controls)

1. **A.7.1 — Physical Security Perimeters**: Define and protect physical security perimeters around facilities processing sensitive data.
2. **A.7.2 — Physical Entry**: Restrict and log physical access to secure areas.
3. **A.7.3 — Securing Offices & Facilities**: Apply physical security measures to offices, rooms, and facilities.
4. **A.7.4 — Physical Security Monitoring** *(NEW in 2022)*: Implement surveillance and monitoring for physical security events.
5. **A.7.9 — Security of Assets Off-Premises**: Protect information assets when taken outside organizational premises.
6. **A.7.10 — Storage Media**: Manage storage media throughout their lifecycle — from acquisition through disposal.
7. **A.7.14 — Secure Disposal or Re-Use of Equipment**: Verify that data-bearing equipment is securely wiped before disposal or re-use.

## 4. Technological Controls (A.8 — 34 controls)

### Access & Authentication

1. **A.8.2 — Privileged Access Rights**: Restrict and tightly control allocation of privileged access. Monitor privileged sessions.
2. **A.8.3 — Information Access Restriction**: Enforce access restrictions per access control policy. Implement at application layer.
3. **A.8.5 — Secure Authentication**: Use strong authentication mechanisms. Enforce MFA for sensitive systems.

### Secure Development

4. **A.8.25 — Secure Development Lifecycle**: Establish and apply rules for the secure development of software and systems.
5. **A.8.26 — Application Security Requirements**: Define security requirements during application design. Include in acceptance criteria.
6. **A.8.27 — Secure System Architecture**: Design systems with security principles (defense in depth, least privilege, fail-secure).
7. **A.8.28 — Secure Coding** *(NEW in 2022)*: Apply secure coding practices — input validation, output encoding, parameterized queries, error handling without information leakage.
8. **A.8.29 — Security Testing**: Conduct security testing (SAST, DAST, dependency scanning) throughout the development lifecycle.
9. **A.8.30 — Outsourced Development**: Apply equivalent security requirements to outsourced or third-party development.
10. **A.8.31 — Separation of Development, Test, and Production**: Maintain isolated environments. Never test with production data unless anonymized.
11. **A.8.32 — Change Management**: Control changes to systems through a formal change management process.
12. **A.8.33 — Test Information**: Protect test data. Use synthetic or anonymized data for testing.

### Data Protection

13. **A.8.10 — Information Deletion**: Implement deletion procedures when data is no longer required. Support right-to-erasure.
14. **A.8.11 — Data Masking** *(NEW in 2022)*: Mask sensitive data (PII, PHI, financial) in non-production environments and in logs.
15. **A.8.12 — Data Leakage Prevention**: Implement DLP controls to detect and prevent unauthorized data exfiltration.
16. **A.8.24 — Use of Cryptography**: Define and enforce a cryptographic policy. Use current standards (AES-256, RSA-2048+, TLS 1.3).

### Monitoring & Resilience

17. **A.8.15 — Logging**: Log security-relevant events with sufficient detail for investigation. Protect log integrity.
18. **A.8.16 — Monitoring Activities** *(NEW in 2022)*: Implement continuous monitoring of networks, systems, and applications for anomalous behavior.
19. **A.8.7 — Protection Against Malware**: Implement anti-malware controls. Keep signatures and detection rules current.
20. **A.8.8 — Management of Technical Vulnerabilities**: Establish a vulnerability management program. Patch critical vulnerabilities within defined timelines.
21. **A.8.9 — Configuration Management** *(NEW in 2022)*: Establish and maintain secure baseline configurations for all systems. Detect and remediate drift.
22. **A.8.13 — Information Backup**: Implement and test backup policies. Maintain backups according to retention requirements.
23. **A.8.14 — Redundancy of Information Processing Facilities**: Implement redundancy to meet availability requirements.

### Network

24. **A.8.20 — Network Security**: Manage and control networks to protect information. Segment by trust zone.
25. **A.8.21 — Security of Network Services**: Define security requirements for network services in agreements with providers.
26. **A.8.22 — Segregation of Networks**: Segregate groups of information services, users, and systems on networks.
27. **A.8.23 — Web Filtering** *(NEW in 2022)*: Filter access to external websites to reduce exposure to malicious content.

## Agent Instructions

- This policy is **opt-in**. It applies only when enabled for projects pursuing ISO 27001 certification.
- When auditing, focus on Technological Controls (A.8) for code reviews — especially A.8.28 (Secure Coding), A.8.11 (Data Masking), A.8.12 (DLP), and A.8.15 (Logging).
- Verify that a Statement of Applicability (SoA) is referenced or maintained for the project.
- Flag missing encryption policies, absent secure coding practices, or production data in test environments as **High** severity.
