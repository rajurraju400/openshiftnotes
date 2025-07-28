# Configuring Red Hat Istio for CNF Applications

## Overview

- **Istio installation** is automated via site-specific policies on the NCP. No manual installation is required.
- **Applications cannot use Istio** until a `ServiceMeshMemberRoll` (SMMR) is created for their namespace.
- **Application teams** may require certain ConfigMaps from the `istio-system` namespace.
- **Application namespaces** must be labeled with `istio-injection=enabled` to enable automatic sidecar injection.

---

## Enable Istio Access for CNF Namespaces

### 1. Log in to the NWC Cluster

Ensure you are logged into the OCP (NWC) cluster using a user with `cluster-admin` privileges (e.g., `ncpadmin`).

---

### 2. Create a ServiceMeshMemberRoll (SMMR)

Create a `ServiceMeshMemberRoll` to register the CNF application namespace with the Istio service mesh.

Here is an example manifest:

```yaml
apiVersion: maistra.io/v1
kind: ServiceMeshMemberRoll
metadata:
  name: default
  namespace: istio-system
spec:
  members:
    - longb92ncc01  # Replace with your application namespace
```

Apply the manifest:

```bash
oc apply -f servicemeshmemberroll.yaml
```

Expected output:

```bash
servicemeshmemberroll.maistra.io/default created
```

---

## Additional Notes

- Ensure that the application namespace has the following label:

```bash
oc label namespace <app-namespace> istio-injection=enabled --overwrite
```

- After SMMR creation, the CNF workload will be part of the mesh and traffic will be managed by Istio.

---

**Document Owner**: [Redhat Deployment Team]  
**Last Updated**: [07/28/2025]
