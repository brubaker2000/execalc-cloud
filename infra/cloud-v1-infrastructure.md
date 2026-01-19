# Execalc Cloud v1 — Infrastructure Declaration

This document declares the required infrastructure components for Execalc Cloud Version 1.
Provisioning tools, vendors, and implementations must conform to this declaration.

---

## 1. Cloud Environment
- Execalc Cloud v1 operates within a single primary cloud provider.
- All environments (dev, staging, prod) are isolated by project/account boundaries.
- No shared infrastructure exists across environments.

---

## 2. Compute
- Stateless application compute is required.
- Compute instances must be replaceable without data loss.
- Horizontal scaling is preferred over vertical scaling.
- No long-lived compute state is permitted.

---

## 3. Persistence
- Persistent storage is required for:
  - Governance state
  - Audit logs
  - Tenant-scoped metadata
- Application compute may not store persistent data locally.

---

## 4. Networking
- All inbound access is authenticated and encrypted.
- No public access to internal services.
- Egress is explicitly controlled.
- Network boundaries must support tenant isolation.

---

## 5. Identity & Access Management
- All access is identity-based.
- Human and system identities are separated.
- Least-privilege is mandatory.
- No hardcoded credentials.

---

## 6. Secrets Management
- Secrets are stored outside application code.
- Secrets are rotatable without redeployment.
- Secrets access is auditable.

---

## 7. Observability
- Centralized logging is required.
- Metrics must be available for:
  - System health
  - Governance enforcement
  - Security-relevant events
- Alerting exists for failure and breach conditions.

---

## 8. What Infrastructure Does Not Do
Cloud v1 infrastructure explicitly excludes:
- Embedded business logic
- Embedded governance rules
- AI or model execution logic

Infrastructure exists to host, not to decide.

---

Infrastructure serves governance; it does not replace it.
