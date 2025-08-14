# Create a Persistent Linux User on OpenShift (RHCOS) Nodes — `claro`

This guide shows how to create a **persistent** Linux user named **`claro`** on OpenShift Container Platform (OCP) nodes by using a **MachineConfig**. It covers all hostgroups. It also includes verification and roll back. 

> Target audience: cluster admins comfortable with `oc`, MachineConfigPools (MCPs), and RHCOS.  
> Works for: OCP 4.x clusters using RHEL CoreOS (RHCOS).

---

## Why MachineConfig?
OCP nodes (RHCOS) are **immutable**. Any manual user creation done via `oc debug` or SSH will **not** survive a reboot. A `MachineConfig` ensures the user is configured on boot and persists across reboots and upgrades.

---

## Prerequisites
- `oc` CLI logged in with cluster-admin privileges.
- Know which pools you want to target (`worker`, `master`/`control-plane`, or `all`).
- A **password hash** or **SSH public key** for the new user.
  - SSH is recommended; password authentication is often disabled by default on RHCOS.

---

## Create the MachineConfig(s)

Pick the scenario that matches your needs and save the YAML accordingly.

### Workers only
Save as `99-add-user-claro-worker.yaml`:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-add-user-claro-worker
  labels:
    machineconfiguration.openshift.io/role: worker
spec:
  config:
    ignition:
      version: 3.2.0
    passwd:
      users:
        - name: claro
          sshAuthorizedKeys:
            - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... user@host"
          groups:
            - claro

```

### Control-plane only
Save as `99-add-user-claro-master.yaml`:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-add-user-claro-master
  labels:
    machineconfiguration.openshift.io/role: master
spec:
  config:
    ignition:
      version: 3.2.0
    passwd:
      users:
        - name: claro
          sshAuthorizedKeys:
            - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... user@host"
          groups:
            - claro
```

### gateway-plane only
Save as `99-add-user-claro-gateway.yaml`:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-add-user-claro-gateway
  labels:
    machineconfiguration.openshift.io/role: gateway
spec:
  config:
    ignition:
      version: 3.2.0
    passwd:
      users:
        - name: claro
          sshAuthorizedKeys:
            - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... user@host"
          groups:
            - claro
```

### storage-plane only
Save as `99-add-user-claro-storage.yaml`:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-add-user-claro-storage
  labels:
    machineconfiguration.openshift.io/role: storage
spec:
  config:
    ignition:
      version: 3.2.0
    passwd:
      users:
        - name: claro
          sshAuthorizedKeys:
            - "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQ... user@host"
          groups:
            - claro
```


### ALL including workers and control-plane
Create **ALL** files then apply both.

> **Note:** On many RHCOS images, `wheel` is the admin group used by sudo. `sudo` group is harmless to include for portability.

---


## Apply the MachineConfig(s)

```bash
# Apply whichever YAMLs you created
oc apply -f 99-add-user-claro-worker.yaml
oc apply -f 99-add-user-claro-master.yaml
oc apply -f 99-add-user-claro-gateway.yaml
oc apply -f 99-add-user-claro-storage.yaml
```

Then watch the pools roll out (nodes will reboot once):
```bash
oc get machineconfigpool
# Optional: watch a specific pool (below is ex)
watch -n5 'oc get mcp worker && oc get mcp master'
```

You can also inspect details:
```bash
oc describe mcp/worker
oc describe mcp/master
```

The pool(s) will go from `UPDATED=True` -> `UPDATING=True` while applying, and back to `UPDATED=True` when finished.

---

## Verify on a node

### Using `oc debug` (no SSH needed)
```bash
# Pick a node in the updated pool
oc get nodes -l node-role.kubernetes.io/worker=
# Example:
NODE=<a-worker-node-name>

# Start a debug shell on the node
oc debug node/$NODE

# In the debug pod:
chroot /host

# Confirm the user exists
id claro
getent passwd claro
groups claro

# If you added SSH keys and want to double-check:
ls -la /home/claro/.ssh/
cat /home/claro/.ssh/authorized_keys

exit  # leave chroot
exit  # leave debug pod
```

### Optional: SSH
If you provided `sshAuthorizedKeys` and network/firewall allows it:
```bash
ssh -i private.key claro@<node-ip-or-dnsname>
```

> On RHCOS, password auth is often disabled by default. Use SSH keys unless you have explicitly enabled password authentication in `/etc/ssh/sshd_config` (which itself would be a MachineConfig change).


---

## Troubleshooting

- **Pool stuck `UPDATING`:**
  - Check MCD logs on an affected node:
    ```bash
    oc -n openshift-machine-config-operator logs -l k8s-app=machine-config-daemon --tail=200
    ```
  - Inspect last applied MachineConfig on the node:
    ```bash
    oc describe node <node-name> | grep -A3 "machineconfiguration.openshift.io/currentConfig"
    ```

- **SSH still not working:**
  - Confirm your public key is present in `/home/claro/.ssh/authorized_keys` on the node.
  - Confirm network/firewall access to port 22.
  - Confirm `sshd` is running and `PasswordAuthentication`/`PubkeyAuthentication` settings if using passwords (manage via MachineConfig).

- **Sudo not working:**
  - Check that `claro` is in `wheel`: `groups claro`
  - If you enabled passwordless sudo, verify `/etc/sudoers.d/00-wheel-nopasswd` exists and is correct.
  - Validate sudoers syntax:
    ```bash
    visudo -c
    ```

---

## Rollback / Removal

- To **remove** the user, create a new MachineConfig that uses a **one-shot systemd unit** to `userdel claro` and clean up `/home/claro`, then delete the original user-creation MachineConfig. (The `passwd.users` stanza itself does not remove users.) Example pattern:

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  name: 99-remove-user-claro-worker
  labels:
    machineconfiguration.openshift.io/role: worker
spec:
  config:
    ignition:
      version: 3.2.0
    systemd:
      units:
        - name: userdel-claro.service
          enabled: true
          contents: |
            [Unit]
            Description=Remove user claro once
            ConditionPathExists=/usr/local/sbin/userdel-claro.sh

            [Service]
            Type=oneshot
            ExecStart=/usr/local/sbin/userdel-claro.sh

            [Install]
            WantedBy=multi-user.target
    storage:
      files:
        - path: /usr/local/sbin/userdel-claro.sh
          mode: 0755
          overwrite: true
          contents:
            source: data:text/plain;charset=utf-8;base64,IyEvYmluL2Jhc2gKdXNlcmRlbCBjbGFybyAmJiBybSAtcmYgL2hvbWUvY2xhcm8KIyBvcHRpb25hbGx5IHJlbW92ZSBub3cgdGhhdCB3ZSdyZSBk
```

> After rollout, delete the original add-user MachineConfig so it doesn’t recreate the user on the next update.

---

## Summary
- Use **MachineConfig** to create **`claro`** persistently.
- Target the **correct MCP** via labels (`worker`, `master`).
- Prefer **SSH keys**; include `sshAuthorizedKeys` in the MC.
- Verify with `oc debug` + `chroot /host`.

