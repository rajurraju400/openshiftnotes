# OpenShift RBAC Model  (LDAP-Driven Groups)

In this model, all access to the OpenShift cluster is controlled directly by **LDAP groups**.  
Each group is created and managed in LDAP, and OpenShift role bindings are mapped to these groups.

---

## LDAP Groups to Request from Customer

### Cluster-Level Groups
1. **ncp-Cluster-administrator**  
   - Full administrative control of the cluster (mapped to `cluster-admin`).

2. **ncp-Cluster-readonly-group**  
   - Read-only visibility into cluster resources (mapped to `ncp-default-ro-cnf-role`).

3. **ncp-Cluster-readonly-with-monitoring-group**  
   - Read-only access + monitoring visibility (mapped to `ncp-default-ro-cnf-role` + `cluster-monitoring-view`).

### Application-Level Groups
- **application-1-group**
- **application-2-group**
- **application-X-group**

One group per application namespace, managed in LDAP.

---

## Role Bindings in OpenShift

### Cluster-Level Bindings
```bash
# Cluster administrators
oc adm policy add-cluster-role-to-group cluster-admin ncp-Cluster-administrator

# Cluster-wide read-only
oc adm policy add-cluster-role-to-group ncp-default-ro-cnf-role ncp-Cluster-readonly-group

# Cluster-wide read-only + monitoring
oc adm policy add-cluster-role-to-group ncp-default-ro-cnf-role ncp-Cluster-readonly-with-monitoring-group
oc adm policy add-cluster-role-to-group cluster-monitoring-view ncp-Cluster-readonly-with-monitoring-group
```

### Namespace-Level Bindings
For each application namespace (example: `app1-ns`):
```bash
# Admin access in the namespace
oc adm policy add-role-to-group admin application-1-group -n app1-ns

# RW custom role access in the namespace
oc adm policy add-role-to-group ncp-default-rw-cnf-role application-1-group -n app1-ns
```

Repeat for each application group (`application-2-group`, `application-X-group`, etc.).

---

## LDAP Group Sync

To keep LDAP groups synchronized with OpenShift, use `oc adm groups sync` with a sync configuration file.

### Sample `ldap-sync.yaml`
```yaml
kind: LDAPSyncConfig
apiVersion: v1
url: "ldap://ldap.example.com/ou=Groups,dc=example,dc=com"
bindDN: "cn=admin,dc=example,dc=com"
bindPassword:
  file: "/etc/ldap-bind-password"

groupUIDNameMapping:
  "cn=ncp-Cluster-administrator,ou=Groups,dc=example,dc=com": "ncp-Cluster-administrator"
  "cn=ncp-Cluster-readonly-group,ou=Groups,dc=example,dc=com": "ncp-Cluster-readonly-group"
  "cn=ncp-Cluster-readonly-with-monitoring-group,ou=Groups,dc=example,dc=com": "ncp-Cluster-readonly-with-monitoring-group"
  "cn=application-1-group,ou=Groups,dc=example,dc=com": "application-1-group"
  "cn=application-2-group,ou=Groups,dc=example,dc=com": "application-2-group"
  "cn=application-X-group,ou=Groups,dc=example,dc=com": "application-X-group"

groupMembershipAttributes:
  - member
```

### Sync Command
```bash
oc adm groups sync --sync-config=ldap-sync.yaml --confirm
```

This ensures that LDAP group membership is continuously reflected inside OpenShift.

---

## End Result
- **Cluster administrators** → full control across the cluster.  
- **Cluster read-only groups** → visibility across cluster resources, with or without monitoring.  
- **Application groups** → access restricted to their own namespace(s), with admin + RW roles.  

This ensures a **clean, LDAP-driven RBAC model** with no dependency on htpasswd or OCP-local groups.
