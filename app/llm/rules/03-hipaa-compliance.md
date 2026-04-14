---
name: HIPAA Compliance
description: Health Insurance Portability and Accountability Act — Security Rule technical safeguards for ePHI. Enable per-project for healthcare software.
alwaysApply: false
---

# HIPAA Compliance Rules (Security Rule — 45 CFR Part 164)

**Authority**: U.S. Department of Health and Human Services (HHS), Office for Civil Rights (OCR).
**Scope**: Applies to Covered Entities and Business Associates that create, receive, maintain, or transmit electronic Protected Health Information (ePHI).

## 1. Technical Safeguards (§ 164.312)

### 1.1 Access Controls

1. **Unique User Identification**: Assign a unique identifier to each user or system accessing ePHI. Shared accounts are prohibited.
2. **Role-Based Access Control (RBAC)**: Implement RBAC enforcing Minimum Necessary — users access only the ePHI required for their specific job function.
3. **Emergency Access Procedures**: Establish documented procedures for obtaining ePHI during an emergency. Emergency access must be logged and reviewed.
4. **Automatic Logoff**: Terminate sessions after a defined period of inactivity. Configure at the application level, not just the infrastructure level.
5. **Access Revocation**: Revoke access within **24 hours** of workforce member termination or role change. Automate via identity provider webhooks.

### 1.2 Audit Controls

1. **Activity Logging**: Record all access, creation, modification, and deletion of ePHI with immutable timestamps, user identity, IP address, and action taken.
2. **Log Review**: Implement automated log analysis to detect anomalous access patterns. Review logs at minimum monthly.
3. **Tamper-Proof Logs**: Audit logs must be append-only and cryptographically protected against modification.

### 1.3 Integrity Controls

1. **Data Integrity Verification**: Implement mechanisms (checksums, HMAC) to confirm ePHI has not been altered or destroyed in an unauthorized manner.
2. **Application Allowlisting**: Prevent execution of unauthorized software that could compromise ePHI integrity.

### 1.4 Person or Entity Authentication

1. **Multi-Factor Authentication (MFA)**: Require MFA for all users accessing ePHI. This is proposed as mandatory in the December 2024 NPRM — implement proactively.
2. **Service-to-Service Authentication**: Use mutual TLS (mTLS) or signed tokens (JWT with RS256+) for inter-service ePHI access.

### 1.5 Transmission Security

1. **Encryption in Transit**: All ePHI transmitted over any network must use TLS 1.3. Reject connections using TLS 1.2 or below where feasible.
2. **Encryption at Rest**: Store ePHI encrypted with AES-256. Manage keys via KMS — never store encryption keys alongside encrypted data.
3. **Email/Messaging**: Never transmit ePHI via unencrypted email or messaging platforms.

## 2. Administrative Safeguards (§ 164.308)

1. **Risk Assessment**: Conduct comprehensive risk assessments at least annually. Document threats, vulnerabilities, and remediation plans.
2. **Security Officer**: Designate a Security Officer responsible for HIPAA security policy development and implementation.
3. **Workforce Training**: All workforce members with ePHI access must complete HIPAA security training upon hire and annually.
4. **Incident Response Plan**: Maintain and test an incident response plan specific to ePHI breaches. Notify HHS within **60 days** of discovery of a qualifying breach.
5. **Business Associate Agreements (BAA)**: Execute a BAA with every vendor, cloud provider, or sub-processor that handles ePHI. No BAA = no ePHI access.

## 3. Physical Safeguards (§ 164.310)

1. **Facility Access Controls**: Limit physical access to facilities housing ePHI systems.
2. **Workstation Security**: Implement policies governing workstation use and physical safeguards for workstations that access ePHI.
3. **Device and Media Controls**: Maintain inventory of all devices storing ePHI. Implement secure disposal (NIST 800-88) for decommissioned media.

## 4. Contingency & Recovery (2024 NPRM Enhancements)

1. **72-Hour Recovery**: Restore critical ePHI systems within **72 hours** of a disruption event.
2. **Backup Separation**: Maintain backups in a separate security domain from production systems.
3. **Annual DR Testing**: Test contingency plans at least annually and document results.

## 5. Vulnerability Management (2024 NPRM Enhancements)

1. **Vulnerability Scanning**: Scan all systems handling ePHI at least every **6 months**.
2. **Penetration Testing**: Conduct penetration testing at least **annually**.
3. **Network Segmentation**: Segment networks to contain lateral movement. ePHI systems must reside in isolated network zones.

## Agent Instructions

- This policy is **opt-in**. It applies only when enabled for healthcare/ePHI projects.
- When auditing, verify all 5 Technical Safeguards sections. Flag missing MFA, unencrypted ePHI transmission, or absent audit logging as **Critical**.
- Verify BAA documentation for any third-party service processing ePHI.
- Check that breach notification timelines (60 days HHS, 72-hour recovery) are codified in incident response procedures.
