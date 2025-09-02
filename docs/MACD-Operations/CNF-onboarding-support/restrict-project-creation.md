# OpenShift: Removing Self-Provisioner Access

### Problem Description

As part of recent learning, we identified that by default OpenShift
allows any authenticated user to create projects.

This behavior exists because the cluster ships with a ClusterRoleBinding
named **self-provisioners**, which grants the **self-provisioner** role
to the **system:authenticated:oauth** group. As a result, any logged-in
user inherits permission to create `projectrequests`.

### Impact

When we create a read-only user for a customer, they are still able to
create a project --- and we don't want that to happen.

### Solution

Remove the self-provisioner role from the default group:

``` bash
oc adm policy remove-cluster-role-from-group self-provisioner system:authenticated:oauth
```

### Impact of the Change

-   Non-cluster-admin users (new or existing) will no longer be able to
    create projects.
-   Cluster-admin users are not affected and will continue to be able to
    create projects.
-   Existing projects created earlier remain intact; users will still
    retain their admin role in those projects unless explicitly
    removed.
-   Non-cluster-admin users attempting `oc new-project <name>` will now
    see a **Forbidden** error.

------------------------------------------------------------------------

Please implement this change across all existing and upcoming
installations. Ensure it is considered in the deployment MOP  as well. I will followup to add it on MOP template. 


