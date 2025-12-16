# NCP Multipoint Inspection Checklist

## Overview

This document defines the **NCP Multipoint Inspection Checklist** for **new OpenShift cluster builds**.

The checklist is intended to be:
- **Executed by the deployment engineer** during and after cluster installation by running validation commands on both **hub** and **CWL (spoke)** clusters.
- Used to **identify and correct deviations proactively** before handing over the cluster to **MACD**.
- **Re-validated by the MACD engineer** to confirm the cluster is fully aligned and ready for operations.

This checklist goes beyond a standard health check and includes:
- NCP **standard blueprint requirements**
- **Behavior-based validations**
- **Lessons learned** from previous deployments

The checklist will continue to evolve as new learnings and standards are incorporated.

---

## Hub Cluster – Multipoint Inspection Checkpoints

**Blueprint section:** Hub-blueprint-validation

### Cluster and Platform Health
- [ ] Cluster overall health
- [ ] OpenShift (OCP) version
- [ ] Node status (masters, workers, BMH alignment)

### Storage
- [ ] Storage (Ceph) health and capacity
- [ ] CSI / storage integration

### Operators
- [ ] Cluster operator versions
- [ ] All required operators installed and in `Succeeded` state

### Lifecycle and Backups
- [ ] Hub cluster ACM backup
- [ ] Infra Manager backup
- [ ] ETCD backup

### Image and GitOps
- [ ] ClusterImageSet availability and correctness
- [ ] Argo CD health and synchronization

### Governance and Security
- [ ] Hub governance (ACM policies)
- [ ] Security hardening compliance
- [ ] Removal of self-provisioner access
- [ ] NCP standard user and role management

### Networking
- [ ] Multus configuration
- [ ] SR-IOV operator and node policies
- [ ] Additional networking configuration
- [ ] NNCP, MetalLB, egress, and backward routes
- [ ] Proxy / cache configuration

### Applications and Monitoring
- [ ] Application status on the hub
- [ ] Application pod health
- [ ] Monitoring stack health

### Registry and Certificates
- [ ] Quay ingress certificate validation

### Service Mesh (If Applicable)
- [ ] Istio configuration (if applicable on the hub)

---

## CWL (Spoke) Cluster – Multipoint Inspection Checkpoints

**Blueprint section:** CWL-blueprint-validation

### Cluster and Platform Health
- [ ] Cluster overall health
- [ ] OpenShift (OCP) version
- [ ] Node readiness and role validation

### Operators
- [ ] Cluster operator status
- [ ] All required operators installed and healthy

### Storage
- [ ] Storage / CSI validation

### Networking
- [ ] Multus configuration
- [ ] SR-IOV operator and policies
- [ ] Additional networking (NNCP, VLANs, routing)
- [ ] NNCP, MetalLB, egress, and backward routes
- [ ] Proxy / cache configuration

### Applications and Monitoring
- [ ] Application pod health
- [ ] Monitoring stack health

### Image and Configuration
- [ ] IDMS and ITMS configuration
- [ ] ClusterImageSet reference validation

### Backups
- [ ] ETCD backup availability

### Registry and Certificates
- [ ] Quay ingress certificate validation

### Governance and Security
- [ ] NCP standard user and role management
- [ ] Removal of self-provisioner access
- [ ] Security hardening compliance

### Service Mesh
- [ ] Istio configuration for CNF workloads

---

## Notes and Future Enhancements

- Command references (`oc`, `ceph`, `acm`) can be added per checkpoint.
- Pass/Fail criteria and evidence fields can be added for audits.
- Checklist will be extended based on future NCP blueprint updates and operational feedback.
