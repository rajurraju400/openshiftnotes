# NMC/NWC Scale-Out Procedure for `Appworker/Gateway` Node

This document outlines the steps required to **scale out** (add) a compute node (e.g., `appworker3.panclypcwl01.mnc020.mcc714`) into an OpenShift cluster managed via ZTP/Agent-based deployment. This procedure assumes you are using OpenShift GitOps (ArgoCD) and the Zero Touch Provisioning (ZTP) flow.

---

## Prepare Node Inventory and SiteConfig

1. Navigate to the Git repository used for ZTP/Day-0 configuration.
2. Identify the correct `SiteConfig` YAML for the target site.
3. Add the new compute node details under the `nodes:` section.
   - Include required fields like BMC IP, MAC address, role, boot mode, etc.

```yaml
- hostName: appworker3.panclypcwl01.mnc020.mcc714
  role: worker
  bmcAddress: redfish://<ip>/redfish/v1/Systems/1
  bmcCredentialsName:
    name: bmc-secret
    namespace: openshift-machine-api
  bootMACAddress: "XX:XX:XX:XX:XX:XX"
  bootMode: UEFI
**output-Omitted**
```

4. Commit and push the changes to the Git repository.

---

## ArgoCD Sync to Apply SiteConfig

Once the Git changes are pushed:

1. Go to the ArgoCD UI.
2. Sync the updated application to apply the changes.



This will trigger the creation of `NMStateConfig`, `InfraEnv`, and `Agent` resources on the hub cluster.

---

## Boot the New Node

1. ISO boot the new compute node so it reaches the discovery state.
2. The node should appear as a `agents.agent-install.openshift.io` resource in the hub cluster.

```bash
oc get agents.agent-install.openshift.io -n <namespace> -o wide
```

Ensure that:
- The agent is `approved: true`
- The matching `NMStateConfig` is applied correctly

> Note:  you dont do anything manully. 

---

## Node Joins the Spoke/CWL Cluster

Once the agent is approved and matched, the following happens:
- The node is provisioned with RHCOS.
- It is automatically joined into the cluster as a `worker` node.

Verify the node has joined the cluster:

```bash
oc get nodes
```

The new node (e.g., `appworker3`) should appear in `Ready` state.

---

## Validate Machine and BMH Resources

Validate that the new node is also reflected in:

```bash
oc -n openshift-machine-api get machines
oc -n openshift-machine-api get bmh
```

---

## Optional: Update MachineSet Replica Count (Only during the intital installation)

If your cluster uses MachineSets and scaling out via replicas is enabled:

1) Identify the appropriate MachineSet:

```bash
oc get machinesets.machine.openshift.io -n openshift-machine-api
```

2) Increase the replica count:

```bash
oc scale machineset <machineset-name> --replicas=<new-count> -n openshift-machine-api
```

---

## Notes

- Make sure BMC credentials and MAC address are correct and accessible from the provisioning network.
- Validate ArgoCD sync status after Git changes.
- Monitor logs using `oc logs -f <pod>` if provisioning is stuck.


---

**Document Owner**: [Redhat NCP Team]  
**Last Updated**: [07/24/2025]

