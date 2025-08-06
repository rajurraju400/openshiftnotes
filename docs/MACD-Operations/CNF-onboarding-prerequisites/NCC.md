# NCC Onboarding Prerequisites

## Documentation Version History

| **Author Name** | **Published Date** | **Version** | **Comments** |
|------------------|---------------------|-------------|-------------|
| LaKshmi | 08/06/2025          | 1.0         | Initial draft|

## List the tasks involved

- [X] #Role Creation for their Service Account. 




## Role Creation for their Service Account


1) Login to the NCP with cluster admin account 


```
oc login 
```

2) Create a role using following file and apply using `oc apply -f`

```
oc apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncc-ig-cpro-qasus92ncc01-servercr
rules:
  - apiGroups: [""]
    resources:
      - endpoints
      - nodes
      - nodes/metrics
      - nodes/proxy
      - pods
      - pods/exec
      - services
    verbs: ["get", "list", "watch", "create"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    resourceNames: ["ncc-ig-cpro-server"]
    verbs: ["get", "create", "delete", "patch", "update", "list", "deletecollection"]
  - apiGroups: ["apps"]
    resources: ["statefulsets"]
    resourceNames: ["ncc-ig-cpro-server"]
    verbs: ["get", "create", "delete", "patch", "update", "list", "deletecollection"]
  - apiGroups: ["networking.k8s.io"]
    resources:
      - ingresses
      - ingresses/status
    verbs: ["get", "list", "watch"]
  - nonResourceURLs: ["/metrics"]
    verbs: ["get"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["clusterroles"]
    verbs: ["get", "patch"]
EOF

```

3)  later bind this ClusterRole to a service account

```
oc adm policy add-cluster-role-to-user ncc-ig-cpro-qasus92ncc01-servercr -z <sa-name> -n <namespace>

```

> This service account and namespace details will be provided by the application teams. 
