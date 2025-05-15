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




### Implementation: 

1) login to cluster with admin privilage and then create a new role (clusterrole) with granding access to network attachements.

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