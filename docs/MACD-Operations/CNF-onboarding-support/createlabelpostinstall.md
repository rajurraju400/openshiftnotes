# Creating a labels on the ocp nodes post installation

## Update the git structure for creating a labels

1)  we can leverage the ability to create custom manifests. The
    following will be created and placed in the `source-crs` directory:

``` bash
file ~/ncpcwltri04nac/site-policies/sites/hub/sources-crs/node/config
```

2)  Create a node manifest as shown below

``` bash
cat << EOF > ~/ncpcwltri04nac/site-policies/sites/hub/sources-crs/node/config/application-cmm_fds-labels.yaml
---
apiVersion: v1
kind: Node
metadata:
  labels:
    is_cmm_fds: "true"
  name: $node
spec: {}
EOF
```

> **Note**: The manifests use two variables, which need to be specified
> when using these CRs in the PGT manifests.

------------------------------------------------------------------------

3)  Creating the PolicyGenTemplate (PGT)

> this can be added to existing PGT file itself but some projects make
> have more labels to updates and for engineer easily understanding, i
> created dedicated file. let us all follow the same standard accross
> other projects too.

``` bash
cat << EOF > ~/ncpcwltri04nac/site-policies/sites/hub/ncpcwltri04nac-config-labels.yaml
---
apiVersion: ran.openshift.io/v1
kind: PolicyGenTemplate
metadata:
  name: "ncpcwltri04nac-labels"
  namespace: "ztp-policies"
spec:
  bindingRules:
    logicalGroup: "active"
    common: "ncp247mp1"
    env: "ncpcwltri04nac"
    disconnected: "true"
  remediationAction: inform
  sourceFiles:
    # Application node label updates : cmm_fds
     - fileName: nodeconfig/application-cmm_fds-labels.yaml
       metadata:
         name: appworker35.ncpcwltri04nac.claro.com.co
       policyName: config-policies
     - fileName: nodeconfig/application-cmm_fds-labels.yaml
       metadata:
         name: appworker36.ncpcwltri04nac.claro.com.co 
       policyName: config-policies
EOF
```

------------------------------------------------------------------------

4)  Add Policy to Kustomization

``` bash
echo "- ncpcwltri04nac-config-labels.yaml" >> ~/ncpcwltri04nac/site-policies/sites/hub/kustomization.yaml
```

------------------------------------------------------------------------

## Push Policy to Git

1)  use the git commands to commitn and push it.

``` bash
cd ~/ncpcwltri04nac/
git add .
git commit -m "Adding a labels"
git push
```

------------------------------------------------------------------------

## Apply the policies now using cgu

1)  Verify Policies Rendered

``` bash
oc get policy -A | grep label
```

Example output:

    ztp-policies           ztp-policies.ncpcwltri04nac-labels              inform      NonCompliant   21s
    ztp-policies   ncpcwltri04nac-label-nodes                           inform      NonCompliant   21s

> **Note**: It might take some time for GitOps to sync with the latest
> changes in Git.\
> You can expedite this by using the **Refresh** option in the ArgoCD
> GUI for the policies app.

------------------------------------------------------------------------

2)  Create ClusterGroupUpgrade (CGU)

Before applying the policy, check the current labels of node `ncpcwltri04nac`:

``` bash
oc get nodes --show-labels --kubeconfig ~/ncpcwltri04nac-kubeconfig
```

Also check existing CGUs:

``` bash
oc get cgu -A
```

Now, apply the new CGU:

``` bash
cat << EOF | oc apply -f -
apiVersion: ran.openshift.io/v1alpha1
kind: ClusterGroupUpgrade
metadata:
  name: ncpcwltri04nac-labels-config-policies
  namespace: ztp-policies
spec:
  managedPolicies:
  - ncpcwltri04nac-labels-config-policies
  backup: false
  clusters:
  - ncpcwltri04nac
  enable: true
  preCaching: false
  preCachingConfigRef: {}
  remediationStrategy:
    maxConcurrency: 1
    timeout: 240
EOF
```

Verify the CGU:

``` bash
oc get cgu -A | grep ncpcwltri04nac
```

------------------------------------------------------------------------

3)  Check Policy Status

``` bash
oc get policy -A | grep label
```

Example output during enforcement:

    ncpcwltri04nac           ztp-policies.ncpcwltri04nac-day2-ncpcwltri04nac-label-nodes-68ffc   enforce     Compliant     13s
    ncpcwltri04nac           ztp-policies.ncpcwltri04nac-label-nodes                  inform      NonCompliant  11m
    ztp-policies   ncpcwltri04nac-labels-config-policies               enforce     nonCompliant     13s
    ztp-policies   ncpcwltri04nac-label-nodes                               inform      NonCompliant  11m

After a few minutes, policies should reach **Compliant** status:

    ncpcwltri04nac           ztp-policies.ncpcwltri04nac-day2-ncpcwltri04nac-label-nodes-68ffc   enforce     Compliant     33s
    ncpcwltri04nac           ztp-policies.ncpcwltri04nac-label-nodes                  inform      Compliant     11m
    ztp-policies   ncpcwltri04nac-labels-config-policies               inform     Compliant     33s
    ztp-policies   ncpcwltri04nac-label-nodes                               inform      Compliant     11m

------------------------------------------------------------------------

4)  Verify Node Labels

``` bash
oc get nodes --show-labels --kubeconfig 
```

You should now see the new label applied:

    is_cmm_fds=true

------------------------------------------------------------------------

5)  CGU Cleanup

After a few minutes, enforced policies will also be deleted.\
Check CGU status after successful compliance:

``` bash
oc get cgu -A | grep label
```

Example:

    ztp-policies   ncpcwltri04nac-labels    40m   Completed   All clusters are compliant with all the managed policies
