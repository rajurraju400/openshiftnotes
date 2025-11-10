# 🔐 OpenShift (OCP) Password Rotation Guide  
**Environment:** Hub and Spoke Clusters (Bare Metal HP and DELL )  
**Includes:** Argo CD, GIT, Quay passwd, OCP UI (only OAuth), Bare Metal Nodes  

# this page is not released yet - work inprog

---

## 📋 Overview
This guide outlines all the key places where passwords or credentials need to be updated in a multi-cluster OpenShift environment that uses **Argo CD, GIT, Quay passwd, OCP UI (only OAuth), Bare Metal Nodes**

---

## 🔹 1. OCP Cluster Accounts

### a. `kubeadmin` or OAuth Users
If still using the default **kubeadmin** user, it’s recommended to migrate to OAuth or HTPasswd users.  
To reset or remove the kubeadmin secret:
```bash
oc delete secret kubeadmin -n kube-system
```

#### Updating HTPasswd User Passwords
```bash
htpasswd -b /path/to/htpasswd <username> <newpassword>
oc create secret generic htpasswd-secret   --from-file=htpasswd=/path/to/htpasswd   -n openshift-config --dry-run=client -o yaml | oc apply -f -

oc patch oauth cluster --type=merge -p '{
  "spec": {
    "identityProviders": [
      {
        "name": "localusers",
        "mappingMethod": "claim",
        "type": "HTPasswd",
        "htpasswd": { "fileData": { "name": "htpasswd-secret" } }
      }
    ]
  }
}'
```

### b. Cluster-admin / Service Account Tokens
OCP service accounts use **tokens**, not passwords.  
To rotate tokens:
```bash
oc delete secret <sa-name>-token-xxxxx -n <namespace>
```
OCP automatically regenerates a new one.

---

## 🔹 2. Argo CD Credentials

Argo CD uses credentials for:
- OCP API access
- Git repositories
- Helm repositories or private registries

### a. Update Argo CD Admin Password
```bash
argocd login <argo-server>
argocd account update-password
```

### b. Update Git Repository Credentials
```bash
argocd repo update <repo-name>   --username <newuser>   --password <newpass>
```

If using SSO (Dex, Keycloak, or OCP OAuth), update credentials in that respective identity provider.

---

## 🔹 3. Bare Metal Node Passwords

Each node (hub and spokes) may have:
- `root` or administrative users  
- `core` user (for RHCOS)

To change manually:
```bash
sudo passwd root
```

To propagate across all nodes, use **MachineConfig**:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: set-root-password
  labels:
    machineconfiguration.openshift.io/role: master
spec:
  config:
    passwd:
      users:
        - name: root
          passwordHash: "<new-hash>"
```

Generate password hash:
```bash
openssl passwd -6 'newpassword'
```

Apply it:
```bash
oc apply -f set-root-password.yaml
```

---

## 🔹 4. Container Registries (Pull Secrets)

If your OCP cluster uses private registries, update the `pull-secret` in `openshift-config`:

```bash
oc extract secret/pull-secret -n openshift-config --to=-
oc set data secret/pull-secret -n openshift-config   --from-file=.dockerconfigjson=/path/to/updated.json
```

Then verify:
```bash
oc get secret pull-secret -n openshift-config -o yaml
```

---

## 🔹 5. Other Integrations

### a. Monitoring (Prometheus, Alertmanager)
Update passwords or tokens in their secrets:
```bash
oc edit secret alertmanager-main -n openshift-monitoring
```

### b. GitOps / Webhooks
If Git webhooks use basic auth or tokens, update them in your Git provider (GitHub, GitLab, Bitbucket).

### c. Storage Systems
If you use NFS, Ceph, or external storage:
- Update credentials in StorageClass or Secret definitions used by CSI drivers.

---

## 🔹 6. Secrets and Automation Tools

If using **Sealed Secrets**, **Vault**, or **Argo CD Vault Plugin**:
- Re-encrypt manifests with new passwords.
- Update tokens in Vault policies or Argo plugin configurations.

---

## ✅ Recommended Order of Operations

1. **Rotate OS-level passwords** (root/core) on all nodes.  
2. **Update OCP OAuth (htpasswd/LDAP)** user credentials.  
3. **Rotate Argo CD admin and repo passwords.**  
4. **Update registry pull secrets.**  
5. **Verify and update external integrations (monitoring, storage, webhooks).**  
6. **Reboot or restart impacted operators if necessary.**

---

## 🧩 Verification

After rotation:
```bash
oc whoami
argocd login <argo-server>
oc get nodes
```
Ensure:
- Cluster access is functional.
- Argo CD syncs successfully.
- Registry images can be pulled without authentication errors.

---

## 🧾 References
- [Red Hat OpenShift Docs – User Management](https://docs.openshift.com/container-platform/latest/authentication/understanding-authentication.html)  
- [Argo CD CLI Reference](https://argo-cd.readthedocs.io/en/stable/user-guide/commands/argocd_account_update-password/)  
- [Machine Config Operator](https://docs.openshift.com/container-platform/latest/post_installation_configuration/machine-configuration-tasks.html)

---

**Author:** Internal Ops Guide  
**Version:** 1.0  
**Last Updated:** 2025-11-07
