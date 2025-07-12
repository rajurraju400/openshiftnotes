# NCP  user's and role's as delivery 


This document outlines the list of approved user IDs and their associated access levels as permitted by management. It serves as a reference for the NCP engineering team to ensure that user and role configurations are strictly within the defined scope. No actions should be taken beyond what is specified in this document.

> Note: All user IDs and privileges must be provisioned exactly as outlined above. Any deviations or additional access requests require explicit approval from management.


## Users and Role management on HUB cluster 

> For `Administrator` level privileges


* `ncpadmin–` `cluster-admin` role – for the NCP team (our team).

* `ncdadmin` – `cluster-admin` role – for the NCD team. This user will be used for NCD git installation (our team)and shared with the NCD team for ongoing lifecycle management.



## Users and Role management on NMC/NWC clusters 
> For `Administrator` level privileges

* `ncpadmin` – `cluster-admin` role – for the NCP team (our team).

* `ncdadmin` – `cluster-admin` role – for the NCD team. Used for NCD application installation by NCD team.

* `ncomadmin` – `cluster-admin` role – for the NCOM team. To be used exclusively for NCOM installation.

* `ncom-sa` - (`cluster-admin` role) Service Account - for NCOM Application is used via CaaS registration. We will create it for them.  

### Cluster-Admin Role Implementation

No additional setup required. Clusterrole `cluster-admin` mapped to user.()

```bash
oc adm policy add-cluster-role-to-user cluster-admin ncpadmin
```



## Role Management for CNF users on NMC/NWC

> For Non-Administrator users.

By default, all CNF application users are assigned the following four roles:

* `Admin` role: Full access to the entire namespace (tenant-admin role for their specific namespace/project).

* `ncd-cbur-role`: Access at the namespace level, allowing users to create, update, delete, and schedule backup jobs.

* `net-attach-def-cluster-role`: Access at the namespace level to create, update, delete network attachment definitions within their namespace.

* `ncp-default-cnf-role`: Access at the cluster level to list, view, watch, and get information for nodes, SCC, NNCP, Metallb IP pool, static routes, backward routes, egress routes, CRDs, profiles etc.


> Note: No need to add above four role to any of these users (ncpadmin, ncdadmin,ncomadmin and ncom-sa)

> Note:  Clarity - CNF id act as read-only for cluster level resources and read-write for tenant level resources.

<!-- Additionally, if users require access to other important resources at the cluster level as read only, we can add those as needed. To existing “ncp-default-cluster-role “, so automatically all cnf users will get the viewer access from there.  -->


### Admin Role Implementation

No additional setup required. Role `admin` mapped to user and namespace:

```bash
oc policy add-role-to-user admin npcvzr1np1 -n npcvzr1np1
```

---

### Network Attachment Role Implementation

1) Create `ClusterRole` for network attachment:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: net-attach-def-cluster-role
rules:
  - apiGroups: ["k8s.cni.cncf.io"]
    resources: ["network-attachment-definitions"]
    verbs: ["create", "get", "list", "watch", "update", "patch", "delete"]
```

2) Bind role to user in their namespace:

```bash
oc create rolebinding net-attach-def-rolebinding \
  --clusterrole=net-attach-def-cluster-role \
  --user=paclypamrf01 \
  --namespace=paclypamrf01
```

3) Validate access:

```bash
oc auth can-i create network-attachment-definitions.k8s.cni.cncf.io --as=paclypamrf01 -n paclypamrf01
```

---

### CBUR Role Implementation

1) Create `ClusterRole`:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncd-cbur-role
rules:
  - apiGroups: ["cbur.bcmt.local"]
    resources: ["brpolices"]
    verbs: ["create", "get", "list", "watch", "update", "patch"]
  - apiGroups: ["cbur.csf.nokia.com"]
    resources: ["brhooks", "brpolices"]
    verbs: ["create", "get", "list", "watch", "update", "patch"]
```

2) Apply role and bind:

```bash
oc apply -f cburrole.yaml
oc create rolebinding ncd-cbur-role-binding \
  --clusterrole=ncd-cbur-role \
  --user=nokia \
  --namespace=test01
```

3) Validate access:

```bash
oc auth can-i create brpolices --as=nokia -n test01
```

---

### Read-Only Cluster Infra Role Implementation

1) Create `ClusterRole` for infra read access:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncp-default-cnf-role
rules:
  - apiGroups: ["security.openshift.io"]
    resources: ["securitycontextconstraints"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list"]
  - apiGroups: ["apiextensions.k8s.io"]
    resources: ["customresourcedefinitions"]
    verbs: ["get", "list"]
  - apiGroups: ["compliance.openshift.io"]
    resources: ["profiles"]
    verbs: ["get", "list"]
  - apiGroups: ["nmstate.io"]
    resources: ["nodenetworkconfigurationpolicies"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["metallb.io"]
    resources: ["ipaddresspools"]
    verbs: ["get", "list"]
```

2) Bind the role:

```bash
oc create clusterrolebinding ncp-default-cnf-role-pppcf01-binding \
  --clusterrole=ncp-default-cnf-role \
  --user=pppcf01
```

3) Validate access:

```bash
oc auth can-i get nodes --as=ppaaa01
oc auth can-i get scc --as=ppaaa01
oc auth can-i get crds --as=ppaaa01
oc login -u ppaaa01 -p redhat123
oc get nodes
```

---

