# Duplicate Egress IP Node Assignments in Red Hat OpenShift Container Platform 4.x

## Purpose
This document describes how to identify and remove duplicate IP addresses on interfaces across gateway nodes in a Red Hat OpenShift Container Platform 4.x environment.

---

## 1. Verify Current Egress IPs on All Gateways

### Step 1: Get the list of egress IPs in the cluster

```bash
[root@ncputility ~ wd_cwl_rc]$ oc get egressip
NAME                  EGRESSIPS     ASSIGNED NODE                               ASSIGNED EGRESSIPS
egress-cnf-oam-aaa    10.236.2.74   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.74
egress-cnf-oam-enum   10.236.2.80   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.80
egress-cnf-oam-git    10.236.2.82   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.82
egress-cnf-oam-ncom   10.236.2.79   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.79
egress-cnf-oam-nm     10.236.2.75   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.75
egress-cnf-oam-pcf    10.236.2.81   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.81
egress-cnf-oam-pgw    10.236.2.77   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.77
egress-cnf-oam-sdl    10.236.2.76   gateway-3.wdwncp01.infra.mobi.eastlink.ca   10.236.2.76
egress-cnf-oam-sdla   10.236.2.78   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.78
egress-dns            10.236.2.90   gateway-1.wdwncp01.infra.mobi.eastlink.ca   10.236.2.90
```

### Step 2: Get the list of gateway nodes

```bash
[root@ncputility ~ wd_cwl_rc]$ oc get nodes | grep -i gateway
gateway-0.wdwncp01.infra.mobi.eastlink.ca  Ready  gateway,gateway-mcp-a,worker  84d  v1.29.10+67d3387
gateway-1.wdwncp01.infra.mobi.eastlink.ca  Ready  gateway,gateway-mcp-a,worker  79d  v1.29.10+67d3387
gateway-2.wdwncp01.infra.mobi.eastlink.ca  Ready  gateway,gateway-mcp-b,worker  84d  v1.29.10+67d3387
gateway-3.wdwncp01.infra.mobi.eastlink.ca  Ready  gateway,gateway-mcp-b,worker  79d  v1.29.10+67d3387
```

### Step 3: Log in to each gateway and check `vlan104` interface

> **Example: No duplicate egress IPs**

```bash
ssh core@gateway-0.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-1.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-2.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-3.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
```

> **Example: Duplicate egress IPs detected**

If multiple gateways have overlapping `/32` IPs assigned to `tentvlan.104`, duplicates exist and must be corrected.

---

## 2. Check OVN Egress IP Assignments
Verify which IPs are assigned via OVN to ensure no active egress IPs are removed accidentally.

```bash
oc get egressips.k8s.ovn.org
```

---

## 3. Take a Backup of Egress IPs
Save the current egress IP configuration before making any modifications.

```bash
oc get egressips.k8s.ovn.org -o yaml > egressipback.yaml
```

---

## 4. Delete the Egress IPs Temporarily

```bash
oc delete -f egressipback.yaml
```

---

## 5. Remove Duplicate IPs on Gateway Nodes

### Step 1: Modify the connection to retain only the correct IP

```bash
ip a show tentvlan.104
nmcli con mod tentvlan.104 ipv4.addresses "10.236.6.70/27"
```

### Step 2: Restart the connection

```bash
nmcli con down tentvlan.104 && nmcli con up tentvlan.104
```

### Step 3: Verify updated IPs

```bash
nmcli con show tentvlan.104 | grep ipv4.addresses
ip a show tentvlan.104
```

> Example output:
```
ipv4.addresses: 10.236.6.70/27
```

---

## 6. Reapply Egress IPs to the Cluster

```bash
oc apply -f egressipback.yaml
```

---

## 7. Validate IPs Against OVN Egress

Ensure that each egress IP is correctly assigned to a single gateway node.

```bash
oc get egressips.k8s.ovn.org
```

---

## 8. Verify Current IPs on All Gateways (Post-Cleanup)
SSH into each gateway node again and confirm that no duplicate IPs remain:

```bash
ssh core@gateway-0.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-1.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-2.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
ssh core@gateway-3.wdwncp01.infra.mobi.eastlink.ca "ip a show tentvlan.104"
```
>  if egress got once again duplicate.  use ip address del command to remove duplicated ip. 
---

## Notes
- [NCPFM-2215](https://jiradc2.ext.net.nokia.com/browse/NCPFM-2215) – Internal NCPFM ticket
- [Red Hat Case #04277107](https://access.redhat.com/support/cases/#/case/04277107) – Support case created by our team
- [OCPBUGS-49368](https://issues.redhat.com/browse/OCPBUGS-49368) – Known OCP 4.16 bug

