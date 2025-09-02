# Security Scan - Nessus : Configure the OpenShift Container Platform

The Tenable integration for the Red Hat OpenShift Container Platform requires a service account configured with appropriate permissions.

Complete the following steps to create the service account, update `<service-account-name>`, and configure access:

---


## Create a SA for security scan. 

1. Create a YAML file

Create a `.yml` file containing:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: nessus
  namespace: default
---
apiVersion: v1
kind: Secret
type: kubernetes.io/service-account-token
metadata:
  name: nessus-token
  namespace: default
  annotations:
    kubernetes.io/service-account.name: nessus
```

---

2. Apply the configuration

Run the following command to apply the file:

```bash
[root@ncputility ~ pancwl_rc]$ oc apply -f ness.yaml
serviceaccount/nessus created
secret/nessus-token created
[root@ncputility ~ pancwl_rc]$

```

---

3. Describe the service account to list tokens

```bash
$ oc describe sa <service-account-name>
```

_Output (example):_

```
Name: <service-account-name>
Tokens: <service-account-name>-token
```

---

4. Retrieve the token for API authentication

This token is used as the **Token** in the OpenShift Container Platform Nessus credential.

```bash
$ oc describe secret <service-account-name>-token
```

_Output (example):_

```
[root@ncputility ~ pancwl_rc]$ oc get secret nessus-token  -n default -o jsonpath="{.data.token}" | base64 -d
eyJhbGciOiJSUzI1NiIsImtpZCI6IjBpd2lFcjdSU3ktY25uRDl3YTVhU0M2V0wtZ0pUWXBXM0RzMmpUTFp1N28ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im5lc3N1cy10b2tlbiIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJuZXNzdXMiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJjOGI0MmRiNC00M2VkLTQ5MzYtYjFkMC02MWRmZmNlNjY2YzMiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDpuZXNzdXMifQ.EpDclPiIgtHkvExN3sXIrpJkmEkdxCNByrXVxctMCvVMHNzwG50Ybyv8MNOaOoOL7KEenwvXktxPk5SvBlzt-_KErvv4oWc4RI70YOxqWMbL9ZVb13jYpb_n_GK3POACrhXrl-8CcIELsZjZJcJzEWaexYVaZmQj1YZNpbhgvYkkvErGIREbG8iRriHH4erE-AaFQQurzscVG9TK1I5cEzK2EnTNEtVJbSM5aO_6aEat1kf18z_i5OqnmgfUI90wwcKHOBfyzY5ws622GtvrEi0CRiNVfwUkoOdTV7zsdJDDHLOHFCTsPC-ZXCGrgfRUwz44JLZVKYvCJqKUfWLAvHRk-4VkPgMOKWSAiu-sK2bhbrahUbYJe_7KcmI0aUFHNGkEFVLn4T3Cfqya8o4iOHQEVZdAEFqBKM9Dl9qHmtkuklJ3bn0V__6YnpFo49t6Vrca3_JGkcaypGGNIPzbN7dpcswS08OgvWMYFYVM9w_DqDx6DDG0SFnHK2B7EsDBvFwhloZiLFEX46WQH1z6nCPcYqmorPJRNMCPNb2Ywzw4badRGOqeUfzMJ4c3c9H0n2QCMw5PssnHWcrsbvVY-ypEJpNAimnTtd8IPL9OzpiVoX0wSQHS7hwX8FT16uNXUd1Pa1esEt-lnhdfaqeyfztei9IZs4s6aGroYA6uB_o[root@ncputility ~ pancwl_rc]$

```

---

5. Grant the service account appropriate permissions

Log in to your OpenShift cluster console:

```
https://console-openshift-console.apps.openshift.<your-domain>
```

Then:

1. Create the following `ClusterRole`:

```
[root@ncputility ~ pancwl_rc]$ cat nessrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: audit-viewonly
rules:
- apiGroups:
  - '*'
  resources:
  - '*'
  verbs:
  - get
  - watch
  - list
  - view
[root@ncputility ~ pancwl_rc]$ oc apply -f nessrole.yaml
clusterrole.rbac.authorization.k8s.io/audit-viewonly created
[root@ncputility ~ pancwl_rc]$ 
```

2. Bind the `ClusterRole` to the previously created service account to grant the required permissions.

```
[root@ncputility ~ pancwl_rc]$ oc adm policy add-cluster-role-to-user audit-viewonly -z nessus -n default
clusterrole.rbac.authorization.k8s.io/audit-viewonly added: "nessus"
[root@ncputility ~ pancwl_rc]$

```
---


## Create a linux user for scan

> Adding Linux user on the ocp nodes is not supported.

> https://access.redhat.com/solutions/6984064 