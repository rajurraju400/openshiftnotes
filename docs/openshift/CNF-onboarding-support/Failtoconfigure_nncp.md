## Troubleshooting failed to configure nncp Error in OCP

> When encountering a `failed to configure nncp` error in OpenShift, it typically indicates an issue with applying the **Node Network Configuration Policy (NNCP)** using the **Kubernetes NMState Operator**. also this will make application installation failed due to missing master interface. 

---

### Common Causes

#### Invalid NNCP YAML
* Syntax errors
* Incorrect interface names or missing fields

#### NMState Operator Issues
* Operator not installed
* Operator pods in failed states

#### Node Labeling Mismatch
* NNCP uses nodeSelector that doesn’t match any node

#### Conflicting Policies
* Multiple NNCPs modifying the same interface

#### Insufficient Permissions
* NMState may lack required privileges (not applicable for CWL, since we are using blueprinted templates.)

#### Node Issues 
* Node is `NotReady` or cordoned

---

### Troubleshooting Steps

1) Check NNCP Status

```
oc get nncp
oc describe nncp <nncp-name>
```

