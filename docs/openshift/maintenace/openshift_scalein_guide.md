# OpenShift Scale-In Procedure for Compute Node

This document outlines the steps required to **scale in** a compute node (e.g., `appworker2.panclypcwl01.mnc020.mcc714`) from an OpenShift cluster managed via ZTP/Agent-based deployment. This procedure assumes you are working within the OpenShift GitOps (ArgoCD) deployment flow.

---

## Edit and Push SiteConfig

1. Open the Git repository used for ZTP automation.
2. Navigate to the appropriate `` YAML file.
3. Remove the node definition (e.g., `appworker2`) from the SiteConfig.
4. Commit and push the changes to the Git repository.

ArgoCD will automatically sync (if infra does not have auto sync enabeld, manually sync it) and delete the corresponding resources from the hub cluster. However, this will **not** remove the `agents.agent-install.openshift.io` resource, which must be deleted manually.

---

## Delete Agent Resource from Hub Cluster

```bash
oc get agents.agent-install.openshift.io -n <namespace> -o wide | grep -i appworker2

# Example:
oc get agents.agent-install.openshift.io -n ncpvnpvlab1 -o wide | grep -i appworker2

# Then delete the matching agents
oc delete agents.agent-install.openshift.io -n ncpvnpvlab1 \
  0d4c5f4b-4751-96e1-4a02-a0dd5f8deb8e 
```

---

## Login to CWL/Spoke Cluster and Verify Resources

### List Machine and BMH Resources

```bash
oc -n openshift-machine-api get machine | grep -i appworker2
oc -n openshift-machine-api get bmh | grep -i appworker2
```

### Delete Bare Metal Host (BMH)

```bash
oc -n openshift-machine-api delete bmh appworker2.panclypcwl01.scdsgplab.com
```

### If BMH is Not Deleted Automatically:

Patch the BMH resource to remove finalizers:

```bash
oc -n openshift-machine-api patch bmh appworker2.panclypcwl01.scdsgplab.com \
  --type=merge -p '{"metadata": {"finalizers":null}}'
```

---

### Delete Machine Resource

```bash
oc -n openshift-machine-api delete machine appworker2.panclypcwl01.scdsgplab.com \
  --kubeconfig /root/hubfeb19/auth/pan-cwl.yaml
```

---

## Scale-In Nodes from Initial Deployment (Optional)

If the node you wish to scale in was part of the **initial deployment**, you must also update the **MachineSet count**:

```bash
oc get machinesets.machine.openshift.io -n openshift-machine-api
```

Identify the relevant MachineSet and decrease the `replicas` count accordingly.

Update with:

```bash
oc scale machineset <machineset-name> --replicas=<desired-count> -n openshift-machine-api
```

---

## Notes

- Be careful when deleting or modifying cluster resources; take necessary etcd backups and must-gather output from hub and cwl.
- Always you informed the DTM before doing any changes to the cluster.
- Ensure that Git and ArgoCD are synced post any changes.

---


