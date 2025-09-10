# OpenShift RBAC Model  (LDAP-Driven Groups)

In this model, all access to the OpenShift cluster is controlled directly by **LDAP groups**.  
Each group is created and managed in LDAP, and OpenShift role bindings are mapped to these groups.

---

## Roles and clusterroles on the NCP


### Role Management for cluster admin

> for Administrator users

- `cluster-admin` role – for the NCP team (our team). default available on NCP  

### Role Management for Cluster viewers

> for Readonly users

- `cluster-reader`  role - for the customer teams. default available on NCP

- `cluster-monitoring-view`  role - for the customer teams. default available on NCP

- `cluster-logging-application-view` role for the customer teams. default available on NCP 

### Role Management for CNF users 

> For Non-Administrator users.


* `Admin` role: Full access to the entire namespace (tenant-admin role for their specific namespace/project). default available on NCP 

* `ncp-default-rw-cnf-role`: Access at the namespace level, allowing users to create, update, delete, and schedule backup jobs, network attachments, redisentercluster, etc. Deployment teams created on NCP 

* `ncp-default-ro-cnf-role`: Access at the cluster level to list, view, watch, and get information for nodes, SCC, NNCP, Metallb IP pool, static routes, backward routes, egress routes, CRDs, profiles, pv etc. Deployment teams created on NCP 




## LDAP Groups to Request from Customer

### Cluster-Level Groups
1) **ncp-Cluster-administrator**  
   - Full administrative control of the cluster (mapped to `cluster-admin` role).

2) **ncp-Cluster-readonly-group**  
   - Read-only visibility into cluster resources (mapped to `cluster-reader` role).

3) **ncp-Cluster-readonly-with-monitoring-group**  
   - Read-only access + monitoring visibility (mapped to `cluster-monitoring-view` role).

4) **ncp-clusterreadonly-with-logging-group**
   - Read-only access + logs visibility (mapped to `cluster-logging-application-view` role)

### Application-Level Groups
1) **application(cmm)-1-group**
  - Access to cmm app namespaces alone. 

2) **application(npc)-2-group**
  - Access to npc application namespace alone.

3) **application(udm)-3-group**
  - Access to udm application namespace alone. 

4) **application-X-group**
  - Access to xyz application namepsace alone.

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
# Admin access in the namespace for group
oc adm policy add-role-to-group admin application(cmm)-1-group -n app1-ns

# RW custom role access in the namespace for group
oc adm policy add-role-to-group ncp-default-rw-cnf-role application(cmm)-1-group -n app1-ns

# RO custom role access for group 
oc adm policy add-role-to-group ncp-default-ro-cnf-role application(cmm)-1-group
```

Repeat for each application group (`application-2-group`, `application-X-group`, etc.).

---

## Challenges 


1) Clusters with the same CNF deployed multiple times

  - Example: two CMM instances (cmm1, cmm2) but LDAP only has a single group for CMM.

> Note:  app1-ns for cmm1 and app2-ns is for cmm2.

```bash
# Admin access in the namespace for group
oc adm policy add-role-to-group admin application(cmm)-1-group -n app1-ns
oc adm policy add-role-to-group admin application(cmm)-1-group -n app2-ns

# RW custom role access in the namespace for group
oc adm policy add-role-to-group ncp-default-rw-cnf-role application(cmm)-1-group -n app1-ns
oc adm policy add-role-to-group ncp-default-rw-cnf-role application(cmm)-1-group -n app2-ns

# RO custom role access for group 
oc adm policy add-role-to-group ncp-default-ro-cnf-role application(cmm)-1-group
```

> in this model, cmm1 admin user and cmm2 admin user being part of same group, so he can access pods on both ns. 


2) Multi-country shared cluster scenario

  - When the same CNF is deployed in a shared cloud across multiple countries, customers do not want users from cmm1 (Country A) to have visibility into cmm2 (Country B) namespaces or pods.

  - If isolation between CNF instances is critical → push customer for extra LDAP group.

```bash
# Admin access in the namespace for group
oc adm policy add-role-to-group admin application(cmm)-1-group -n app1-ns


# RW custom role access in the namespace for group
oc adm policy add-role-to-group ncp-default-rw-cnf-role application(cmm)-1-group -n app1-ns

# RO custom role access for group 
oc adm policy add-role-to-group ncp-default-ro-cnf-role application(cmm)-1-group
```

```bash
# Admin access in the namespace for group
oc adm policy add-role-to-group admin application(cmm)-2-group -n app1-ns

# RW custom role access in the namespace for group
oc adm policy add-role-to-group ncp-default-rw-cnf-role application(cmm)-2-group -n app1-ns

# RO custom role access for group 
oc adm policy add-role-to-group ncp-default-ro-cnf-role application(cmm)-1-group
```
<!-- 
3) Multi-country shared cluster scenario (hybrid) - Not preferred. **worst case** need architect approval.

  - When the same CNF is deployed in a shared cloud across multiple countries, customers do not want users from cmm1 (Country A) to have visibility into cmm2 (Country B) namespaces or pods.

  - but dont want to create additional groups on LDAP

  - Create OCP-local subgroups (cmm-1, cmm-2).

  - Bind them to namespaces accordingly.

```
oc adm groups new cmm1 user1 user2
oc adm groups new cmm2 user3 user4
``` -->


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


## Default users on NCP for HUB/NMC/NWC cluster's (user's expected to be avaiable on LDAP side)

> For `Administrator` level privileges


* `ncpadmin–` `ncp-Cluster-administrator` group – for the NCP team (our team).

* `ncdadmin` – `ncp-Cluster-administrator` group – for the NCD team. This user will be used for NCD git installation (our team)and shared with the NCD team for ongoing lifecycle management.

* `ncomadmin` – `ncp-Cluster-administrator` group – for the NCOM team. To be used exclusively for NCOM installation.



## End Result
- **ncp-Cluster-administrator** → full control across the cluster.  
- **ncp-Cluster-readonly-group** → visibility across cluster resources with monitoring.  
- **ncp-Cluster-readonly-with-monitoring-group** → visibility across cluster resources, with monitoring. 
- **ncp-clusterreadonly-with-logging-group** → visibility across cluster resources with Logging access. 
- **application-X-group** → access restricted to their own namespace(s) with admin + RW roles etc.  

This ensures a **clean, LDAP-driven RBAC model** with no dependency on htpasswd or OCP-local groups.
