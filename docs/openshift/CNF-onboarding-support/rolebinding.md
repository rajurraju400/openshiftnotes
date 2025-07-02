##  OpenShift Container Platform (OCP) role defination


> In OpenShift Container Platform (OCP), roles define a set of permissions and are a core part of Role-Based Access Control (RBAC). OCP uses Kubernetes RBAC with some OpenShift-specific enhancements. You can define different types of roles depending on your access and security needs.



### Types of Roles in OCP:

#### ClusterRole

* Scope: Cluster-wide.

* Purpose: Grants permissions across the entire cluster or to non-namespaced resources (e.g., nodes, persistent volumes).

* Use Cases:
    Granting administrators full access across all projects.
    Giving access to cluster-wide resources like nodes or storage classes.

##### If You Use a ClusterRole:
> Scope: Cluster-wide, but can still be bound to specific namespaces via RoleBinding.

###### Implication:

* You can reuse the same ClusterRole and bind it to multiple users and namespaces.

* Just create separate RoleBindings in each namespace for each user.



#### Role

* Scope: Namespaced.

* Purpose: Grants permissions only within a specific namespace (project).

* Use Cases:

    Application developers working within a single namespace.
    CI/CD pipelines running in isolated namespaces.


##### If You Use a Role (namespaced):
> Scope: One namespace only.

###### Implication:

* You can’t reuse the same Role in another namespace.

* You’d have to create a new Role (with the same rules) in each namespace where you want the same access.

#### Binding Roles

> You assign roles to users or groups through bindings:

* RoleBinding: Assigns a Role to a user/group/service account within a specific namespace.

* ClusterRoleBinding: Assigns a ClusterRole to a user/group/service account cluster-wide or within a namespace (via a RoleBinding referencing a ClusterRole).




### Implementation for Network attachement role: 

1) login to cluster with admin privilage and then create a new role (clusterrole) with granding access to network attachements.

> in case need it as yaml file. (optional step)

```
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: net-attach-def-cluster-role
rules:
  - apiGroups: ["k8s.cni.cncf.io"]
    resources: ["network-attachment-definitions"]
    verbs: ["create", "get", "list", "watch", "update", "patch", "delete"]
```

(or)

```
[root@ncputility ~ pancwl_rc]$ oc create clusterrole net-attach-def-cluster-role \
  --verb=create,get,list,watch,update,patch,delete \
  --resource=network-attachment-definitions.k8s.cni.cncf.io
 
clusterrole.rbac.authorization.k8s.io/net-attach-def-cluster-role created
```

2) Run this step for below cnf users requesting for access to network attachment definition and assign to their NS.

```
[root@ncputility ~ pancwl_rc]$ oc create rolebinding net-attach-def-rolebinding \
  --clusterrole=net-attach-def-cluster-role \
  --user=paclypamrf01 \
  --namespace=paclypamrf01
rolebinding.rbac.authorization.k8s.io/net-attach-def-rolebinding created
```

3) Then validate is that user having access to it. 

```
[root@ncputility ~ pancwl_rc]$ oc auth can-i create network-attachment-definitions.k8s.cni.cncf.io --as=paclypamrf01 -n paclypamrf01
yes
[root@ncputility ~ pancwl_rc]$
```




### Implementation for Cbur role: 

1) login to cluster with admin privilage and then create a new role (clusterrole) with granding access to cbur br polices.

> code snippet: `# cat  > cburrole.yaml`

```
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
1.1) here is the command executed on this platform. just give ctrl+c at last. right after that just apply it. 

```
[root@ncputility ~ panhub_rc]$ cat  > cburrole.yaml
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
^C
[root@ncputility ~ panhub_rc]$ oc apply  -f cburrole.yaml
clusterrole.rbac.authorization.k8s.io/ncd-cbur-role created
[root@ncputility ~ panhub_rc]$

```

2) Run this step for below cnf users requesting for access to cbur br polices and assign to their NS.

```
[root@ncputility ~ panhub_rc]$ oc create rolebinding ncd-cbur-role-binding \
  --clusterrole=ncd-cbur-role \
  --user=nokia \
  --namespace=test01
rolebinding.rbac.authorization.k8s.io/ncd-cbur-role-binding created
[root@ncputility ~ panhub_rc]$
```

3) Then validate is that user having access to it. 

```
[root@ncputility ~ panhub_rc]$ oc auth can-i create brpolices --as=nokia -n test01
yes
[root@ncputility ~ panhub_rc]$

```


### Implementation for security,nodes,customresourcedefinitions,etc role: 

1) login to cluster with admin privilage and then create a new role (clusterrole) with granding access to nodes, scc, crds, etc.

> code snippet: `# cat  > read-cluster-infra-info.yaml`

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: read-cluster-infra-info
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
1.1) here is the command executed on this platform. just give ctrl+c at last. right after that just apply it. 

```
[root@ncputility ~ panhub_rc]$ cat  > ncp-default-cnf-role.yaml
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

^C
[root@ncputility ~ panhub_rc]$ oc apply  -f ncp-default-cnf-role.yaml
clusterrole.rbac.authorization.k8s.io/ncp-default-cnf-role created
[root@ncputility ~ panhub_rc]$

```

2) Run this step for below cnf users requesting for access to `nodes,scc,etc` polices and assign to their user id.

```
[root@ncputility ~ panhub_rc]$  oc create clusterrolebinding ncp-default-cnf-role-pppcf01-binding --clusterrole=ncp-default-cnf-role --user=pppcf01 
clusterrolebinding.rbac.authorization.k8s.io/ncp-default-cnf-role-pppcf01-binding created
[root@ncputility ~ panhub_rc]$
```

3) Then validate is that user having access to it. 

```
[root@ncputility ~ nmcrc]$ oc auth can-i get nodes --as=ppaaa01
Warning: resource 'nodes' is not namespace scoped

yes
[root@ncputility ~ nmcrc]$ oc auth can-i get scc --as=ppaaa01
Warning: resource 'securitycontextconstraints' is not namespace scoped in group 'security.openshift.io'

yes
[root@ncputility ~ nmcrc]$ oc auth can-i get crds --as=ppaaa01
Warning: resource 'customresourcedefinitions' is not namespace scoped in group 'apiextensions.k8s.io'

yes
[root@ncputility ~ nmcrc]$ oc login -u ppaaa01 -p redhat123
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have one project on this server: "ppaaa01"

Using project "ppaaa01".
[root@ncputility ~ nmcrc]$ oc get nodes
NAME                                            STATUS   ROLES                                         AGE    VERSION
appworker1-0.ppwncp01.infra.mobi.eastlink.ca    Ready    appworker,appworker-mcp-a,appworker1,worker   10d    v1.29.10+67d3387
appworker1-1.ppwncp01.infra.mobi.eastlink.ca    Ready    appworker,appworker-mcp-a,appworker1,worker   10d    v1.29.10+67d3387
appworker1-10.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387
appworker1-11.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387
appworker1-12.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387
appworker1-13.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387
appworker1-14.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387
appworker1-15.ppwncp01.infra.mobi.eastlink.ca   Ready    appworker,appworker-mcp-b,appworker1,worker   10d    v1.29.10+67d3387


```
