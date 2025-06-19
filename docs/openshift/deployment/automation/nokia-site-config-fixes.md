# Nokia Automation Tool - Site Config Template Fixes

This document captures the issues and required corrections for the Nokia automation tool used to generate and manage OpenShift site-config templates.

> Please download the automation 24.7 from NOLS NCP package. this tool is only for cwl cluster based site-config files. 

## 1. `site-config/resource/kustomization.yaml`

### Issue:
Incorrect resource reference in the file.

### Correction:
Update the resource name to:
```yaml
resources:
  - ncp-24-7-mp1-release.yaml
```

---

## 2. `site-config/resource/ncp-24-7-mp1-release.yaml`

### Issue:
Incorrect or missing ClusterImageSet name.

### Correction:
Ensure the following value is set:
```yaml
spec:
  clusterImageSetRef:
    name: ncp-24-7-mp1-release
```

---

## 3. `site-config/pre-reqs/bmc-credentials-sitename.yaml`

### Issue:
base64 encrypt username/password field will be empty.

### Correction:
Base64 encode the BMC credentials:
```yaml
username: <base64 encoded username>
password: <base64 encoded password>
```
Use the following command to encode:
```bash
echo -n 'username' | base64
echo -n 'password' | base64
```

---

## 4. `site-config/pre-reqs/pull-secret-sitename.yaml`

### Issue:
Hub Quay credentials are not encoded.

### Correction:
Base64 encode only for user/passwd and the entire pull-secret string text:
```yaml
.data:
  .dockerconfigjson: <base64 encoded pull secret>
```

---

## 5. `site-config/<site-name>/site-config.yaml`

### Issues:
- Missing DNS search domain on master nodes, but validate for all other host's too. 
- Third NTP server not configured.
- Incorrect hostnames. 
- `tenant-bond-2` port mapping incorrect
- Master subnet incorrectly set to `/26`

### Corrections:
- Ensure DNS search domain is defined under `host manifest at last.`
- Add third NTP server if required under `ntpServers`
- Validate and correct all hostnames to match inventory defined on the LLD. 
- Correct `tenant-bond-2` interfaces/port assignments
- Define proper subnet, e.g. `/24` instead of `/26` for masters

---

## 6. `site-config/<site-name>/storage-config.yaml` and `worker-config.yaml`

### Issue:
Configuration not aligned with product line template. if miss to do this step, your deployment will fail inigition file issue.

### Workaround:
Manually copy-paste the file contents from the official product line template.

---

## 7. `site-config/<site-name>/extra-manifests/chrony-update-master.yaml` & `chrony-update-worker.yaml`

### Issue:
Missing or incomplete NTP server list

### Correction:
- Add the third NTP server IP to the chrony config
- Base64 encode the full `chrony.conf` content

Example:
```yaml
spec:
  config:
    data:
      chrony.conf: |
        <base64 encoded chrony.conf with 3 NTP entries>
```
Use the following command to encode:
```bash
cat chrony.conf | base64 -w0
```

---

## Summary Table
| File Path | Issue | Action |
|-----------|-------|--------|
| `resource/kustomization.yaml` | Wrong resource name | Use `ncp-24-7-mp1-release.yaml` |
| `ncp-24-7-mp1-release.yaml` | Missing ClusterImageSet | Set `ncp-24-7-mp1-release` |
| `bmc-credentials-sitename.yaml` | Unencrypted credentials | Base64 encode values |
| `pull-secret-sitename.yaml` | Unencrypted secret | Base64 encode full JSON |
| `site-config.yaml` | Multiple infra/network issues | Fix DNS, NTP, hostnames, subnet, ports |
| `storage-config.yaml` & `worker-config.yaml` | Config mismatch | Copy from official template |
| `chrony-update-master.yaml`, `chrony-update-worker.yaml` | Missing NTP | Add 3rd IP and base64 encode |

---

> **Note**: Always validate all YAML files and value before you start the installation.
