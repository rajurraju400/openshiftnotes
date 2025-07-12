# Hub Cluster - Master Replacement 

> Here is the steps to do the master replacement on the hub cluster.  Dont use this steps for NMC/NWC.  

## Customer Details

1) This mop is created for oneweb cluster and since nokia automation tool populated incorrect `/prefix` for master node. 

2) for Oneweb london site, hub cluster having two nodes with incorrect `/prefix` problem.


## Duration

* [It will take 4 hours per node + 1 hour buffer. totall 10 hours for two servers.](#duration)

## Impact

* [CWL cluster LCM operation should be impacted](#impact)
* [CNF installed on the CWL cluster remains undistrubed, because hub quay will be time to time unaccess. So application onboarding process may make hub quay to be stressed.](#impact)


## Highlevel Steps

* [Removing the failed node from the cluster](#removing-the-failed-node-from-the-cluster)
* [Adding back the node control plane node](#adding-back-the-node-control-plane-node)




## Removing the failed node from the cluster 

### ETCD backup for master nodes. 


1) Start a debug session for a control plane node:

```
oc debug node/<node_name>
```

2) Change your root directory to /host:

```
chroot /host
```

3) If the cluster-wide proxy is enabled, be sure that you have exported the NO_PROXY, HTTP_PROXY, and HTTPS_PROXY environment variables. (optional)


4) Run the cluster-backup.sh script and pass in the location to save the backup to.


```
sh-4.4# /usr/local/bin/cluster-backup.sh /home/core/assets/backup
```
`Example script output `

```
found latest kube-apiserver: /etc/kubernetes/static-pod-resources/kube-apiserver-pod-6
found latest kube-controller-manager: /etc/kubernetes/static-pod-resources/kube-controller-manager-pod-7
found latest kube-scheduler: /etc/kubernetes/static-pod-resources/kube-scheduler-pod-6
found latest etcd: /etc/kubernetes/static-pod-resources/etcd-pod-3
ede95fe6b88b87ba86a03c15e669fb4aa5bf0991c180d3c6895ce72eaade54a1
etcdctl version: 3.4.14
API version: 3.4
{"level":"info","ts":1624647639.0188997,"caller":"snapshot/v3_snapshot.go:119","msg":"created temporary db file","path":"/home/core/assets/backup/snapshot_2021-06-25_190035.db.part"}
{"level":"info","ts":"2021-06-25T19:00:39.030Z","caller":"clientv3/maintenance.go:200","msg":"opened snapshot stream; downloading"}
{"level":"info","ts":1624647639.0301006,"caller":"snapshot/v3_snapshot.go:127","msg":"fetching snapshot","endpoint":"https://10.0.0.5:2379"}
{"level":"info","ts":"2021-06-25T19:00:40.215Z","caller":"clientv3/maintenance.go:208","msg":"completed snapshot read; closing"}
{"level":"info","ts":1624647640.6032252,"caller":"snapshot/v3_snapshot.go:142","msg":"fetched snapshot","endpoint":"https://10.0.0.5:2379","size":"114 MB","took":1.584090459}
{"level":"info","ts":1624647640.6047094,"caller":"snapshot/v3_snapshot.go:152","msg":"saved","path":"/home/core/assets/backup/snapshot_2021-06-25_190035.db"}
Snapshot saved at /home/core/assets/backup/snapshot_2021-06-25_190035.db
{"hash":3866667823,"revision":31407,"totalKey":12828,"totalSize":114446336}
snapshot db and kube resources are successfully saved to /home/core/assets/backup

```

> Transfer the backup files locally on the `infra-manager` node.

### Identifying the failed control plane node

1) First identify which node is the failed one, e.g. which is in NotReady state, using the `oc get nodes` command.

```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#
```

> Example `ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab` will use this node for replacement.

```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS                     ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready                      control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready,SchedulingDisabled   control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready                      control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready                      gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready                      gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# 
```

2) Drain the node, using oc adm drain command. 

```
[root@dom16hub101-infra-manager ~]# oc adm drain ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab --ignore-daemonsets --delete-emptydir-data --force
node/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab already cordoned
Warning: ignoring DaemonSet-managed Pods: open-cluster-management-backup/node-agent-lvlpm, openshift-cluster-node-tuning-operator/tuned-2xqzr, openshift-dns/dns-default-x7x7p, openshift-dns/node-resolver-sd5qh, openshift-image-registry/node-ca-5nkn2, openshift-ingress-canary/ingress-canary-rngvh, openshift-local-storage/diskmaker-discovery-4snb5, openshift-local-storage/diskmaker-manager-vkkxk, openshift-machine-api/ironic-proxy-24kth, openshift-machine-config-operator/machine-config-daemon-9j45d, openshift-machine-config-operator/machine-config-server-ww4tz, openshift-monitoring/node-exporter-9xshs, openshift-multus/multus-additional-cni-plugins-hkcdv, openshift-multus/multus-dt7qt, openshift-multus/network-metrics-daemon-4j5fx, openshift-multus/whereabouts-reconciler-bv24v, openshift-network-diagnostics/network-check-target-btgf8, openshift-network-node-identity/network-node-identity-td874, openshift-network-operator/iptables-alerter-75rfw, openshift-nmstate/nmstate-handler-tngrh, openshift-ovn-kubernetes/ovnkube-node-svz9x, openshift-storage/csi-cephfsplugin-rnkrk, openshift-storage/csi-rbdplugin-zg88h; deleting Pods that declare no controller: openshift-etcd/etcd-guard-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab, openshift-kube-apiserver/kube-apiserver-guard-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab, openshift-kube-controller-manager/kube-controller-manager-guard-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab, openshift-kube-scheduler/openshift-kube-scheduler-guard-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
evicting pod multicluster-engine/clusterclaims-controller-7d56ff6fc9-555pz
evicting pod ncd-git/ncd-git-gitlab-shell-55ccf645ff-ks77d
evicting pod multicluster-engine/assisted-image-service-0
evicting pod multicluster-engine/assisted-service-96cf94d9c-wg9zh
evicting pod ncd-db/ncd-postgresql-postgresql-ha-sentinel-8556d466c6-kd52n
evicting pod openshift-logging/logging-loki-gateway-7687c66f64-fxd4d
evicting pod ncd-db/ncd-postgresql-postgresql-ha-proxy-54c69f6cc-csqbz
evicting pod open-cluster-management-observability/observability-thanos-rule-1
evicting pod openshift-machine-api/cluster-baremetal-operator-75fbb58cc5-lpqds
evicting pod open-cluster-management-hub/cluster-manager-registration-controller-7bcbcd64c5-s5p8l
evicting pod open-cluster-management-observability/observability-grafana-85c6896fd4-7vxzp
evicting pod openshift-machine-api/control-plane-machine-set-operator-65fbf4bd7-j2l2r
** output Omitted **
pod/console-mce-console-57b6b4968-jfl4x evicted
pod/logging-loki-query-frontend-55bc666b5c-87hmh evicted
pod/ncd-postgresql-postgresql-ha-keeper-2 evicted
pod/apiserver-776b5f87d7-6t6vz evicted
node/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab drained
[root@dom16hub101-infra-manager ~]#

```
3) Once drain complete, shutdown the node. (power off)
```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS                     ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready                      control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready,SchedulingDisabled   control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready                      control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready                      gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready                      gateway,worker                        74d   v1.29.10+67d3387
```
4) Post power off, node will become not ready. 
```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS                        ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   NotReady,SchedulingDisabled   control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#

```
### Removing the node from the etcd cluster

1) First fetch the pods from the openshift-etcd namespace which have the label k8s-app=etcd.

```
[root@dom16hub101-infra-manager ~]# oc -n openshift-etcd get pods -l k8s-app=etcd -o wide
NAME                                                    READY   STATUS    RESTARTS   AGE   IP              NODE                                               NOMINATED NODE   READINESS GATES
etcd-ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   4/4     Running   12         74d   10.145.151.92   ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   <none>           <none>
etcd-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   0/0     not running   12         74d   10.145.151.93   ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
etcd-ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   4/4     Running   8          74d   10.145.151.94   ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]# 
```

2) Start a remote shall to one of the pods which shall be running, and not scheduled on the failed node.

```
[root@dom16hub101-infra-manager ~]# oc rsh -n openshift-etcd etcd-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
sh-5.1# etcdctl endpoint health
{"level":"warn","ts":"2025-05-27T17:09:44.374886Z","logger":"client","caller":"v3@v3.5.14/retry_interceptor.go:63","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00027a000/10.145.151.93:2379","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 7.162307ms
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 7.213802ms
https://10.145.151.93:2379 is unhealthy: failed to commit proposal: context deadline exceeded
Error: unhealthy cluster
sh-5.1#
```

3) check the status of the etdctl memebers. and removed the scale-in commpute. 

```
sh-5.1# etcdctl member list -w table
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
|        ID        | STATUS  |                       NAME                       |         PEER ADDRS         |        CLIENT ADDRS        | IS LEARNER |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
| 44ad9888985e068c | started | ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab | https://10.145.151.92:2380 | https://10.145.151.92:2379 |      false |
| f26d12a58d17e571 | started | ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab | https://10.145.151.94:2380 | https://10.145.151.94:2379 |      false |
| fc4de79a3d723a5c | Not running | ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab | https://10.145.151.93:2380 | https://10.145.151.93:2379 |      false |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
sh-5.1# etcdctl member remove fc4de79a3d723a5c
Member fc4de79a3d723a5c removed from cluster 136d42915c2b0516
sh-5.1# etcdctl member list -w table
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
|        ID        | STATUS  |                       NAME                       |         PEER ADDRS         |        CLIENT ADDRS        | IS LEARNER |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
| 44ad9888985e068c | started | ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab | https://10.145.151.92:2380 | https://10.145.151.92:2379 |      false |
| f26d12a58d17e571 | started | ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab | https://10.145.151.94:2380 | https://10.145.151.94:2379 |      false |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
sh-5.1#
```

4) check the etcd health now. 
```
sh-5.1#  etcdctl endpoint health
{"level":"warn","ts":"2025-05-27T17:10:43.025287Z","logger":"client","caller":"v3@v3.5.14/retry_interceptor.go:63","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc000020000/10.145.151.93:2379","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = context deadline exceeded"}
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 6.399106ms
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 6.344247ms
https://10.145.151.93:2379 is unhealthy: failed to commit proposal: context deadline exceeded
Error: unhealthy cluster
sh-5.1#
exit
command terminated with exit code 1
[root@dom16hub101-infra-manager ~]#
```

5) run the following command to Turn off the quorum guard:
```
[root@dom16hub101-infra-manager ~]# oc patch etcd/cluster --type=merge -p '{"spec":{"unsupportedConfigOverrides":{"useUnsupportedUnsafeNonHANonProductionUnstableEtcd": true}}}'
etcd.operator.openshift.io/cluster patched
[root@dom16hub101-infra-manager ~]# 
```

6) Remove the old secrets for the unhealthy etcd member that was removed by running the following commands.

```
[root@dom16hub101-infra-manager ~]# oc get secrets -n openshift-etcd | grep master-102
etcd-peer-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab              kubernetes.io/tls   2      74d
etcd-serving-metrics-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   kubernetes.io/tls   2      74d
etcd-serving-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab           kubernetes.io/tls   2      74d
[root@dom16hub101-infra-manager ~]# #for i in `oc get secrets -n openshift-etcd | grep master-2 | awk
'{print $1}'`; do oc delete secrets -n openshift-etcd $i; done
[root@dom16hub101-infra-manager ~]# for i in `oc get secrets -n openshift-etcd | grep master-102 | awk '{print $1}'`; do oc delete secrets -n openshift-etcd $i; done
secret "etcd-peer-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab" deleted
secret "etcd-serving-metrics-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab" deleted
secret "etcd-serving-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab" deleted
[root@dom16hub101-infra-manager ~]# oc get secrets -n openshift-etcd | grep master-102                                                                 etcd-peer-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab              kubernetes.io/tls   2      3s
etcd-serving-metrics-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   kubernetes.io/tls   2      2s
etcd-serving-ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab           kubernetes.io/tls   2      3s
[root@dom16hub101-infra-manager ~]#
[root@dom16hub101-infra-manager ~]#

```


### Fetch the output of the failed node’s machine CR

It is needed to fetch the output of the failed node’s machine CR as it contains labels related to the cluster. Then it shall be m odified, e.g. status part shall be removed, annotation of last applied configuration, `machine.openshift.op/instance-state:
provisioned` shall be removed, creation timestamp, finalizer, generation, resource version,
uid, from spec, the providerID shall be also removed.

1) Get the list of node and find the node you want to remove from machines. 


```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS                        ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   NotReady,SchedulingDisabled   control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# 
```

2) using the follow command to ge the node need to removed.  using `-o wide `

```
[root@dom16hub101-infra-manager ~]# oc get machines.machine -A
NAMESPACE               NAME                              PHASE     TYPE   REGION   ZONE   AGE
openshift-machine-api   ncpvblvhub-b6cjs-master-0         Running                          74d
openshift-machine-api   ncpvblvhub-b6cjs-master-1         Running                          74d
openshift-machine-api   ncpvblvhub-b6cjs-master-2         Running                          74d
openshift-machine-api   ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
openshift-machine-api   ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# oc get machines.machine -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-1         Running                          74d
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]#

```

3) take a backup of these nodes from file. 
```
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api -o yaml `oc get machines.machine.openshift.io -n openshift-machine-api -o wide |grep ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab|awk {'print $1'}` > backup_machinemaster-102.yaml
```

4) just collecting all those outputs here. 

> just refer to productline guide for reference sample tempalte

![alt text](image.png)

```
[root@dom16hub101-infra-manager ~]# cat backup_machinemaster-102.yaml
apiVersion: machine.openshift.io/v1beta1
kind: Machine
metadata:
  annotations:
    machine.openshift.io/instance-state: unmanaged
    metal3.io/BareMetalHost: openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
  creationTimestamp: "2025-03-13T23:51:45Z"
  finalizers:
  - machine.machine.openshift.io
  generation: 3
  labels:
    machine.openshift.io/cluster-api-cluster: ncpvblvhub-b6cjs
    machine.openshift.io/cluster-api-machine-role: master
    machine.openshift.io/cluster-api-machine-type: master
  name: ncpvblvhub-b6cjs-master-1
  namespace: openshift-machine-api
  resourceVersion: "140998860"
  uid: a53b879c-a886-4381-a1bb-9322333fa76e
spec:
  lifecycleHooks:
    preDrain:
    - name: EtcdQuorumOperator
      owner: clusteroperator/etcd
  metadata: {}
  providerID: baremetalhost:///openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab/346b01e0-6bb8-40bd-8db3-d3eabf4d44f1
  providerSpec:
    value:
      apiVersion: baremetal.cluster.k8s.io/v1alpha1
      customDeploy:
        method: install_coreos
      hostSelector: {}
      image:
        checksum: ""
        url: ""
      kind: BareMetalMachineProviderSpec
      metadata:
        creationTimestamp: null
      userData:
        name: master-user-data-managed
status:
  addresses:
  - address: fde1:53ba:e9a0:de11:912f:2112:633a:4b75
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: ""
    type: InternalIP
  - address: 10.145.151.93
    type: InternalIP
  - address: ""
    type: InternalIP
  conditions:
  - lastTransitionTime: "2025-03-14T00:04:57Z"
    message: 'Drain operation currently blocked by: [{Name:EtcdQuorumOperator Owner:clusteroperator/etcd}]'
    reason: HookPresent
    severity: Warning
    status: "False"
    type: Drainable
  - lastTransitionTime: "2025-03-14T00:03:59Z"
    status: "True"
    type: InstanceExists
  - lastTransitionTime: "2025-03-13T23:58:56Z"
    status: "True"
    type: Terminable
  lastUpdated: "2025-05-27T17:08:29Z"
  nodeRef:
    kind: Node
    name: ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
    uid: cdc0d098-638f-4c2d-b4ba-4c2c1ebc1c10
  phase: Running
[root@dom16hub101-infra-manager ~]# cat backup_machinemaster-102_editted.yaml
apiVersion: machine.openshift.io/v1beta1
kind: Machine
metadata:
  annotations:
    machine.openshift.io/instance-state: unmanaged
    metal3.io/BareMetalHost: openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
  finalizers:
  - machine.machine.openshift.io
  generation: 3
  labels:
    machine.openshift.io/cluster-api-cluster: ncpvblvhub-b6cjs
    machine.openshift.io/cluster-api-machine-role: master
    machine.openshift.io/cluster-api-machine-type: master
  name: ncpvblvhub-b6cjs-master-1
  namespace: openshift-machine-api
spec:
  lifecycleHooks:
    preDrain:
    - name: EtcdQuorumOperator
      owner: clusteroperator/etcd
  metadata: {}
  providerID: baremetalhost:///openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab/346b01e0-6bb8-40bd-8db3-d3eabf4d44f1
  providerSpec:
    value:
      apiVersion: baremetal.cluster.k8s.io/v1alpha1
      customDeploy:
        method: install_coreos
      hostSelector: {}
      image:
        checksum: ""
        url: ""
      kind: BareMetalMachineProviderSpec
      metadata:
        creationTimestamp: null
      userData:
        name: master-user-data-managed

[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS                        ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   NotReady,SchedulingDisabled   control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready                         control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready                         gateway,worker                        74d   v1.29.10+67d3387


```


### Removing failed node’s OSDs from ODF

1) Get the list of pods from `openshift-storage` namespace here. 
``` 
[root@dom16hub101-infra-manager ~]# oc get pods -n openshift-storage -o wide | grep -i ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
csi-cephfsplugin-rnkrk                                            2/2     Running   6              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-provisioner-646d95bdd9-496ng                        6/6     Running   0              15d   172.21.1.43      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-zg88h                                               3/3     Running   9              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-crashcollector-11cef195e99cf42211bc5b21918ec486-b8jpz   1/1     Running   0              26d   172.21.0.19      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-exporter-11cef195e99cf42211bc5b21918ec486-6f8c85r84bf   1/1     Running   0              26d   172.21.0.20      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-mon-a-66bcddd94-wbfs4                                   2/2     Running   0              26d   172.21.0.9       ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-osd-0-54d5b7dd6b-vjf4f                                  2/2     Running   0              27d   172.21.0.11      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-osd-5-79fb5f7965-wpgpq                                  2/2     Running   0              27d   172.21.0.17      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]# 
```

2) remove the mon and osd pods running on the master2 nodes. then check the status of the pod's to make sure, it's terminated. 

```
[root@dom16hub101-infra-manager ~]# oc scale deployment rook-ceph-mon-a --replicas=0 -n openshift-storage
deployment.apps/rook-ceph-mon-a scaled
[root@dom16hub101-infra-manager ~]# oc scale deployment rook-ceph-osd-0 --replicas=0 -n openshift-storage
deployment.apps/rook-ceph-osd-0 scaled
[root@dom16hub101-infra-manager ~]#
[root@dom16hub101-infra-manager ~]# oc scale deployment rook-ceph-osd-5 --replicas=0 -n openshift-storage
deployment.apps/rook-ceph-osd-5 scaled
[root@dom16hub101-infra-manager ~]# oc get pods -n openshift-storage -o wide | grep -i ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
csi-cephfsplugin-rnkrk                                            2/2     Running       6              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-provisioner-646d95bdd9-496ng                        6/6     Running       0              15d   172.21.1.43      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-zg88h                                               3/3     Running       9              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
rook-ceph-exporter-11cef195e99cf42211bc5b21918ec486-6f8c85r84bf   0/1     Terminating   0              26d   172.21.0.20      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]# oc scale deployment --selector=app=rook-ceph-crashcollector,node_name=ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab  --replicas=0 -n openshift-storage
error: no objects passed to scale
[root@dom16hub101-infra-manager ~]# oc get pods -n openshift-storage -o wide | grep -i ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab                csi-cephfsplugin-rnkrk                                            2/2     Running   6              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-provisioner-646d95bdd9-496ng                        6/6     Running   0              15d   172.21.1.43      ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
csi-rbdplugin-zg88h                                               3/3     Running   9              71d   10.145.151.93    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]#

```

2.1) remove the label from the node. 

```
[root@dom16hub101-infra-manager ~]# oc label node ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab cluster.ocs.openshift.io/openshift-storage-
node/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab unlabeled
[root@dom16hub101-infra-manager ~]#
```

3) Now run the OSD removal script to delete the OSD completely from the cluster.

```
[root@dom16hub101-infra-manager ~]# oc process -n openshift-storage ocs-osd-removal -p FAILED_OSD_IDS=0,5 FORCE_OSD_REMOVAL=true | oc create -n openshift-storage -f -
Error from server (AlreadyExists): error when creating "STDIN": jobs.batch "ocs-osd-removal-job" already exists
[root@dom16hub101-infra-manager ~]# oc get jobs -n openshift-storage | gre removal
bash: gre: command not found...
[root@dom16hub101-infra-manager ~]# oc get jobs -n openshift-storage | grep removal
ocs-osd-removal-job                                      1/1           14m        33d
[root@dom16hub101-infra-manager ~]# oc delete jobs -n openshift-storage ocs-osd-removal-job
job.batch "ocs-osd-removal-job" deleted
[root@dom16hub101-infra-manager ~]# oc process -n openshift-storage ocs-osd-removal -p FAILED_OSD_IDS=0,5 FORCE_OSD_REMOVAL=true | oc create -n openshift-storage -f -
job.batch/ocs-osd-removal-job created
[root@dom16hub101-infra-manager ~]# oc get jobs -n openshift-storage | grep removal                                                                    ocs-osd-removal-job                                      0/1           5s         5s
[root@dom16hub101-infra-manager ~]# oc get jobs -n openshift-storage | grep removal
ocs-osd-removal-job                                      1/1           13s        14s
[root@dom16hub101-infra-manager ~]# oc delete jobs -n openshift-storage ocs-osd-removal-job                                                            job.batch "ocs-osd-removal-job" deleted
[root@dom16hub101-infra-manager ~]#
```

4) At last remove the pv as well. post check that ceph cluster.

```
[root@dom16hub101-infra-manager ~]#oc get pv | grep local | grep -i released
local-pv-4fcd3797                          3576Gi     RWO            Delete           Released    openshift-storage/ocs-deviceset-localblockstorage-0-data-0ll69z                      localblockstorage     <unset>                          71d
local-pv-cb7421c8                          3576Gi     RWO            Delete           Released    openshift-storage/ocs-deviceset-localblockstorage-2-data-1w8q46                      localblockstorage     <unset>                          33d
[root@dom16hub101-infra-manager ~]# oc delete pv local-pv-4fcd3797 local-pv-cb7421c8
persistentvolume "local-pv-4fcd3797" deleted
persistentvolume "local-pv-cb7421c8" deleted
[root@dom16hub101-infra-manager ~]#

[root@dom16hub101-infra-manager ~]# oc get clusteroperator baremetal
NAME        VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
baremetal   4.16.24   True        False         False      74d

```

### Removing the node from the cluster


1) Get the node status of `master-102`. from `bmh`, `machine` etc. 

```
[root@dom16hub101-infra-manager ~]# oc get bmh -n openshift-machine-api
NAME                                               STATE       CONSUMER                          ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-0         true             74d
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-1         true             74d
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-2         true             74d
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-mlq8w   true             74d
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-x5dc5   true             74d
[root@dom16hub101-infra-manager ~]# oc delete bmh -n openshift-machine-api ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
baremetalhost.metal3.io "ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab" deleted

[root@dom16hub101-infra-manager ~]# oc get bmh -n openshift-machine-api
NAME                                               STATE       CONSUMER                          ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-0         true             74d
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-2         true             74d
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-mlq8w   true             74d
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-x5dc5   true             74d
[root@dom16hub101-infra-manager ~]# 
```

2) Check the `machines.machine` api and delete it. 
```
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-1         Failed                           74d
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# #oc delete machines.machine.openshift.io -n openshift-machine-api ncpvblvhub-b6cjs-master-1
[root@dom16hub101-infra-manager ~]# oc describe machines.machine.openshift.io -n openshift-machine-api ncpvblvhub-b6cjs-master-1 | grep -i master-102
              metal3.io/BareMetalHost: openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
  Provider ID:  baremetalhost:///openshift-machine-api/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab/346b01e0-6bb8-40bd-8db3-d3eabf4d44f1
    Name:  ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
[root@dom16hub101-infra-manager ~]#
[root@dom16hub101-infra-manager ~]# oc delete machines.machine.openshift.io -n openshift-machine-api ncpvblvhub-b6cjs-master-1
machine.machine.openshift.io "ncpvblvhub-b6cjs-master-1" deleted
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]#

[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# 
```

3) Now check the status of `bmh`, `machines` and `nodes`, to make sure `master-2` is completly removed. 
```
[root@dom16hub101-infra-manager ~]#oc get bmh -n openshift-machine-api
NAME                                               STATE       CONSUMER                          ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-0         true             74d
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-master-2         true             74d
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-mlq8w   true             74d
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   unmanaged   ncpvblvhub-b6cjs-worker-0-x5dc5   true             74d
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#
```

> After this step, the node or failed parts of it can be safely replaced.

## Adding back the node control plane node

### Create BMH and Machine CRs


1) Check the list of nodes in cluster now. 
```
[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#
```
2) In the openshift-machine-api namespace two secrets shall be created. One is for the BMC access and the other one stores the networking configuration.

2.0) The data of secret for BMC access is simply base64 encoded.

```
[root@dom16hub101-infra-manager ~]# cat bmc-credential-hub.yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: control-plane-3-bmc-secret
  namespace: openshift-machine-api
data:
  username: "cm9vdA=="
  password: "Y2Fsdmlu"
type: opaque
[root@dom16hub101-infra-manager ~]#
```



2.1) Then the networking configuration shall be created as a secret. It is needed as the default setting is DHCP for the nodes. These information can be simply copied from the agent-config.yaml which was used for the deployment of the HUB cluster. If node replacement was done (including NIC) make sure to update the MAC addresses!


```
[root@dom16hub101-infra-manager ~]# cat master-102_network_config.yaml
apiVersion: v1
kind: Secret
metadata:
  name: openshift-master-102-network-config-secret
  namespace: openshift-machine-api
type: Opaque
stringData:
  nmstate: |
    interfaces:
      - name: infra-1
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:F9:7F:48
      - name: infra-2
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:F9:7F:49
      - name: tenant-1-1
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:4A:90:8A
      - name: tenant-1-2
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:4A:90:8B
      - name: tenant-2-1
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:4A:90:8E
      - name: tenant-2-2
        type: ethernet
        state: up
        identifier: mac-address
        mtu: 9126
        mac-address: C4:70:BD:4A:90:8F
      - name: infra-bond
        type: bond
        state: up
        link-aggregation:
          mode: active-backup
          options:
            miimon: "100"
          port:
          - infra-1
          - infra-2
        mtu: 9126
      - name: tenant-bond-1
        link-aggregation:
          mode: active-backup
          options:
            miimon: "100"
          port:
          - tenant-1-1
          - tenant-1-2
        mtu: 9126
        state: up
        type: bond
      - name: tenant-bond-2
        link-aggregation:
          mode: active-backup
          options:
            miimon: "100"
          port:
          - tenant-2-1
          - tenant-2-2
        mtu: 9126
        state: up
        type: bond
      - name: infra-bond.200
        type: vlan
        state: up
        mtu: 9126
        ipv4:
          enabled: true
          dhcp: false
          address:
            - ip: 10.145.151.93
              prefix-length: 26
        ipv6:
          enabled: false
          dhcp: false
        vlan:
          base-iface: infra-bond
          id: 200
    routes:
      config:
        - destination: 0.0.0.0/0
          next-hop-address: 10.145.151.65
          next-hop-interface: infra-bond.200
          table-id: 254
    dns-resolver:
      config:
        search:
        - t-mobile.lab
        server:
        - 5.232.32.63
        - 10.169.69.10

[root@dom16hub101-infra-manager ~]#
```


3) create the BMH resource using `baremetalhost` file.

```
[root@dom16hub101-infra-manager ~]# cat master-102_bmh_wih_secret.yaml
apiVersion: metal3.io/v1alpha1
kind: BareMetalHost
metadata:
  name: ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
  namespace: openshift-machine-api
spec:
  automatedCleaningMode: disabled
  bmc:
    address: idrac-virtualmedia://10.145.151.15/redfish/v1/Systems/System.Embedded.1    #this is for dell server , for HP or other vendor check virtual media path
    credentialsName: control-plane-3-bmc-secret
    disableCertificateVerification: True
  bootMACAddress: c4:70:bd:f9:7f:48
  bootMode: UEFISecureBoot
  externallyProvisioned: false
  hardwareProfile: unknown
  online: true
  rootDeviceHints:
    deviceName: /dev/disk/by-path/pci-0000:4a:00.0-scsi-0:2:0:0
  userData:
    name: master-user-data-managed
    namespace: openshift-machine-api
  preprovisioningNetworkDataName: openshift-master-102-network-config-secret
[root@dom16hub101-infra-manager ~]#

```

3.1) After creating this resource, the node will be inspected, and after a few minutes it shall be
in available state.

```
[root@dom16hub101-infra-manager ~]# oc apply -f master_102_bmh.yaml
Warning: metadata.finalizers: "baremetalhost.metal3.io": prefer a domain-qualified finalizer name to avoid accidental conflicts with other finalizer writers
baremetalhost.metal3.io/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab created

```

3.2) the node status should change from registering -> inspecting -> available. 

```
[root@dom16hub101-infra-manager ~]# oc get bmh -n openshift-machine-api ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
NAME                                               STATE          CONSUMER                    ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   available   ncpvblvhub-b6cjs-master-1   true             31m
[root@dom16hub101-infra-manager ~]#

```

> Once the BMH is in available state, the machine CR can be created. The same shall be created which was done in chapter 1.3.

6) create and apply the machines.yaml 
```
[root@dom16hub101-infra-manager ~]# cat backup_machinemaster-102_editted.yaml
apiVersion: machine.openshift.io/v1beta1
kind: Machine
metadata:
  labels:
    machine.openshift.io/cluster-api-cluster: ncpvblvhub-b6cjs
    machine.openshift.io/cluster-api-machine-role: master
    machine.openshift.io/cluster-api-machine-type: master
  name: ncpvblvhub-b6cjs-master-1
  namespace: openshift-machine-api
spec:
  lifecycleHooks:
    preDrain:
    - name: EtcdQuorumOperator
      owner: clusteroperator/etcd
  metadata: {}
  providerSpec:
    value:
      apiVersion: baremetal.cluster.k8s.io/v1alpha1
      customDeploy:
        method: install_coreos
      hostSelector: {}
      image:
        checksum: ""
        url: ""
      kind: BareMetalMachineProviderSpec
      metadata:
        creationTimestamp: null
      userData:
        name: master-user-data-managed
[root@dom16hub101-infra-manager ~]#

[root@dom16hub101-infra-manager ~]# oc apply -f backup_machinemaster-102_editted.yaml
Warning: metadata.finalizers: "machine.machine.openshift.io": prefer a domain-qualified finalizer name to avoid accidental conflicts with other finalizer writers
machine.machine.openshift.io/ncpvblvhub-b6cjs-master-1 created
[root@dom16hub101-infra-manager ~]#

[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE          TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                               74d
ncpvblvhub-b6cjs-master-1         Provisioning                          4m17s
ncpvblvhub-b6cjs-master-2         Running                               74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                               74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                               74d
[root@dom16hub101-infra-manager ~]#
```
7) Monitor the status of bmh, will change to provisioning
```
[root@dom16hub101-infra-manager ~]# oc get bmh -n openshift-machine-api
NAME                                               STATE          CONSUMER                          ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   unmanaged      ncpvblvhub-b6cjs-master-0         true             74d
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   provisioning   ncpvblvhub-b6cjs-master-1         true             31m
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   unmanaged      ncpvblvhub-b6cjs-master-2         true             74d
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   unmanaged      ncpvblvhub-b6cjs-worker-0-mlq8w   true             74d
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   unmanaged      ncpvblvhub-b6cjs-worker-0-x5dc5   true             74d
[root@dom16hub101-infra-manager ~]#

#nodes will be added to the cluster 

[root@dom16hub101-infra-manager ~]# oc get nodes
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           80s   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#

[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-1         Running                          15m
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# oc get bmh -n openshift-machine-api ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
NAME                                               STATE         CONSUMER                    ONLINE   ERROR   AGE
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   provisioned   ncpvblvhub-b6cjs-master-1   true             44m
[root@dom16hub101-infra-manager ~]#

```

8) At last node successfully added back to the cluster here. 
```
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE                                                                                                            VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d                                                                                                            v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE                                                                                                            VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           54s                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d                                                                                                            v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d                                                                                                            v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-apioc get machines.machine.openshift.io -n openshift-machine-api^C
[root@dom16hub101-infra-manager ~]# oc get machines.machine.openshift.io -n openshift-machine-api
NAME                              PHASE     TYPE   REGION   ZONE   AGE
ncpvblvhub-b6cjs-master-0         Running                          74d
ncpvblvhub-b6cjs-master-1         Running                          15m
ncpvblvhub-b6cjs-master-2         Running                          74d
ncpvblvhub-b6cjs-worker-0-mlq8w   Running                          74d
ncpvblvhub-b6cjs-worker-0-x5dc5   Running                          74d
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE    VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d    v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           110s   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d    v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d    v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d    v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]#
```



### Verifying etcd

1) Verify the etcd-guard-<nodename> and etcd-<nodename> pods are started and all containers of it are in running state in the openshift-etcd namespace.

```
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE    VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d    v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           110s   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d    v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d    v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d    v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# master=ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 7.570208ms
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 7.468077ms
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl member list -w table
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
|        ID        | STATUS  |                       NAME                       |         PEER ADDRS         |        CLIENT ADDRS        | IS LEARNER |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
| 44ad9888985e068c | started | ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab | https://10.145.151.92:2380 | https://10.145.151.92:2379 |      false |
| 55fcb74f654c5538 | started | ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab | https://10.145.151.93:2380 | https://10.145.151.93:2379 |      false |
| f26d12a58d17e571 | started | ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab | https://10.145.151.94:2380 | https://10.145.151.94:2379 |      false |
+------------------+---------+--------------------------------------------------+----------------------------+----------------------------+------------+
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 6.734404ms
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 7.079121ms
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE     VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d     v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           3m55s   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d     v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d     v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d     v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc get mcp
NAME     CONFIG                                             UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
master   rendered-master-d234bb112f0765116acd91ac75545416   True      False      False      3              3                   3                     0                      74d
worker   rendered-worker-3e1f74a73d4a683cfbf22ced0aa2792a   False     True       True       2              1                   1                     1                      74d
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 6.241732ms
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 6.383176ms
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
error: unable to upgrade connection: container not found ("etcd")
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
error: unable to upgrade connection: container not found ("etcd")
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE     VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d     v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           5m51s   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d     v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d     v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d     v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health

{"level":"warn","ts":"2025-05-27T21:24:52.680683Z","logger":"client","caller":"v3@v3.5.14/retry_interceptor.go:63","msg":"retrying of unary invoker failed","target":"etcd-endpoints://0xc00022e000/10.145.151.92:2379","attempt":0,"error":"rpc error: code = DeadlineExceeded desc = latest balancer error: last connection error: connection error: desc = \"transport: Error while dialing: dial tcp 10.145.151.92:2379: connect: connection refused\""}
https://10.145.151.93:2379 is healthy: successfully committed proposal: took = 6.311573ms
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 8.305729ms
https://10.145.151.92:2379 is unhealthy: failed to commit proposal: context deadline exceeded
Error: unhealthy cluster
command terminated with exit code 1
[root@dom16hub101-infra-manager ~]# oc get co
NAME                                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication                             4.16.24   True        False         False      3h48m
baremetal                                  4.16.24   True        False         False      74d
cloud-controller-manager                   4.16.24   True        False         False      74d
cloud-credential                           4.16.24   True        False         False      74d
cluster-autoscaler                         4.16.24   True        False         False      74d
config-operator                            4.16.24   True        False         False      74d
console                                    4.16.24   True        False         False      74d
control-plane-machine-set                  4.16.24   True        False         False      74d
csi-snapshot-controller                    4.16.24   True        False         False      74d
dns                                        4.16.24   True        False         False      74d
etcd                                       4.16.24   True        True          False      74d     NodeInstallerProgressing: 1 node is at revision 15; 2 nodes are at revision 17
image-registry                             4.16.24   True        False         False      74d
ingress                                    4.16.24   True        False         False      74d
insights                                   4.16.24   True        False         False      74d
kube-apiserver                             4.16.24   True        True          False      74d     NodeInstallerProgressing: 2 nodes are at revision 60; 1 node is at revision 61
kube-controller-manager                    4.16.24   True        False         False      74d
kube-scheduler                             4.16.24   True        False         False      74d
kube-storage-version-migrator              4.16.24   True        False         False      13d
machine-api                                4.16.24   True        False         False      74d
machine-approver                           4.16.24   True        False         False      74d
machine-config                             4.16.24   True        False         True       74d     Failed to resync 4.16.24 because: error during syncRequiredMachineConfigPools: [context deadline exceeded, failed to update clusteroperator: [client rate limiter Wait returned an error: context deadline exceeded, error MachineConfigPool worker is not ready, retrying. Status: (pool degraded: true total: 2, ready 1, updated: 1, unavailable: 1)]]
marketplace                                4.16.24   True        False         False      74d
monitoring                                 4.16.24   Unknown     True          Unknown    35m     Rolling out the stack.
network                                    4.16.24   True        False         False      74d
node-tuning                                4.16.24   True        False         False      6m20s
openshift-apiserver                        4.16.24   True        False         False      4h17m
openshift-controller-manager               4.16.24   True        False         False      74d
openshift-samples                          4.16.24   True        False         False      74d
operator-lifecycle-manager                 4.16.24   True        False         False      74d
operator-lifecycle-manager-catalog         4.16.24   True        False         False      74d
operator-lifecycle-manager-packageserver   4.16.24   True        False         False      74d
service-ca                                 4.16.24   True        False         False      74d
storage                                    4.16.24   True        False         False      74d

[root@dom16hub101-infra-manager ~]# watch -n 5 oc get co
[root@dom16hub101-infra-manager ~]# oc exec -it $(oc -n openshift-etcd get pods -l k8s-app=etcd -o wide --no-headers |grep -v $master|head -n 1|awk {'print $1'}) -n openshift-etcd -- etcdctl endpoint health
https://10.145.151.93:2379 is healthy: successfully committed proposal: took = 6.998079ms
https://10.145.151.92:2379 is healthy: successfully committed proposal: took = 7.999787ms
https://10.145.151.94:2379 is healthy: successfully committed proposal: took = 7.997677ms
[root@dom16hub101-infra-manager ~]# oc patch etcd/cluster --type=merge -p '{"spec": {"unsupportedConfigOverrides": null}}'
etcd.operator.openshift.io/cluster patched
[root@dom16hub101-infra-manager ~]# 

```

### Adding back the OSDs

1) The OSDs are automatically added, after the PVs are created by the Local Storage Operator.

2) After adding the labels back to the node (which was applied initially during the deployment) including the `cluster.ocs.openshift.io/openshift-storage`, the Local Storage Operator’s two daemonsets pods will be scheduled on this node as well, namely the
diskmaker discovery and the diskmaker manager. 

3) The discovery will inspect the node for available disks while the manager will create the PVs which will be used by ODF.

oc get pods -n openshift-local-storage -o wide

4) After the new PVs are created the new OSDs deployments will be recreated and OSD pods and mon pod will start automatically.

5) If those would not start automatically for some reason, the rook-ceph-operator pod shall be restarted.

```

[root@dom16hub101-infra-manager ~]#oc get pods -n openshift-local-storage -o wide
NAME                                      READY   STATUS    RESTARTS        AGE   IP             NODE                                               NOMINATED NODE   READINESS GATES
diskmaker-discovery-6mcrl                 2/2     Running   4               71d   172.20.0.163   ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-discovery-9htrb                 2/2     Running   6               71d   172.20.2.141   ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-manager-fbzkp                   2/2     Running   4               71d   172.20.0.164   ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-manager-h6r2t                   2/2     Running   6               71d   172.20.2.142   ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   <none>           <none>
local-storage-operator-6d968c9989-w4vp4   1/1     Running   2 (3h42m ago)   56d   172.23.0.66    ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]# oc get no -l  cluster.ocs.openshift.io/openshift-storage
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           13m   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc label node ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab cluster.ocs.openshift.io/openshift-storage=
node/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab labeled
[root@dom16hub101-infra-manager ~]# oc get no -l  cluster.ocs.openshift.io/openshift-storage
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           15m   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
```
> After the new PVs are created the new OSDs deployments will be recreated and OSD pods and mon pod will start automatically. If those would not start automatically for some reason, the rook-ceph-operator pod shall be restarted.
```
[root@dom16hub101-infra-manager ~]# oc get pods -n openshift-local-storage -o wide
NAME                                      READY   STATUS    RESTARTS        AGE   IP             NODE                                               NOMINATED NODE   READINESS GATES
diskmaker-discovery-6mcrl                 2/2     Running   4               71d   172.20.0.163   ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-discovery-9htrb                 2/2     Running   6               71d   172.20.2.141   ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-discovery-b6bxh                 2/2     Running   0               26s   172.21.0.33    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-manager-8kpkt                   2/2     Running   0               26s   172.21.0.31    ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-manager-fbzkp                   2/2     Running   4               71d   172.20.0.164   ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   <none>           <none>
diskmaker-manager-h6r2t                   2/2     Running   6               71d   172.20.2.142   ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   <none>           <none>
local-storage-operator-6d968c9989-w4vp4   1/1     Running   2 (3h46m ago)   57d   172.23.0.66    ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   <none>           <none>
[root@dom16hub101-infra-manager ~]# oc get co
NAME                                       VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
authentication                             4.16.24   True        False         False      3h57m
baremetal                                  4.16.24   True        False         False      74d
cloud-controller-manager                   4.16.24   True        False         False      74d
cloud-credential                           4.16.24   True        False         False      74d
cluster-autoscaler                         4.16.24   True        False         False      74d
config-operator                            4.16.24   True        False         False      74d
console                                    4.16.24   True        False         False      74d
control-plane-machine-set                  4.16.24   True        False         False      74d
csi-snapshot-controller                    4.16.24   True        False         False      74d
dns                                        4.16.24   True        False         False      74d
etcd                                       4.16.24   True        False         False      74d
image-registry                             4.16.24   True        False         False      74d
ingress                                    4.16.24   True        False         False      74d
insights                                   4.16.24   True        False         False      74d
kube-apiserver                             4.16.24   True        False         False      74d
kube-controller-manager                    4.16.24   True        False         False      74d
kube-scheduler                             4.16.24   True        False         False      74d
kube-storage-version-migrator              4.16.24   True        False         False      13d
machine-api                                4.16.24   True        False         False      74d
machine-approver                           4.16.24   True        False         False      74d
machine-config                             4.16.24   True        False         True       74d     Failed to resync 4.16.24 because: error during syncRequiredMachineConfigPools: [context deadline exceeded, failed to update clusteroperator: [client rate limiter Wait returned an error: context deadline exceeded, error MachineConfigPool worker is not ready, retrying. Status: (pool degraded: true total: 2, ready 1, updated: 1, unavailable: 1)]]
marketplace                                4.16.24   True        False         False      74d
monitoring                                 4.16.24   Unknown     True          Unknown    45m     Rolling out the stack.
network                                    4.16.24   True        False         False      74d
node-tuning                                4.16.24   True        False         False      15m
openshift-apiserver                        4.16.24   True        False         False      4h26m
openshift-controller-manager               4.16.24   True        False         False      74d
openshift-samples                          4.16.24   True        False         False      74d
operator-lifecycle-manager                 4.16.24   True        False         False      74d
operator-lifecycle-manager-catalog         4.16.24   True        False         False      74d
operator-lifecycle-manager-packageserver   4.16.24   True        False         False      74d
service-ca                                 4.16.24   True        False         False      74d
storage                                    4.16.24   True        False         False      74d

[root@dom16hub101-infra-manager ~]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph status -c /var/lib/rook/openshift-storage/openshift-storage.config
  cluster:
    id:     27b507a3-b496-4549-9271-a3bc0705dd13
    health: HEALTH_WARN
            Degraded data redundancy: 87816/433023 objects degraded (20.280%), 68 pgs degraded, 74 pgs undersized

  services:
    mon: 3 daemons, quorum a,b,e (age 3m)
    mgr: b(active, since 3h), standbys: a
    mds: 1/1 daemons up, 1 hot standby
    osd: 6 osds: 6 up (since 112s), 6 in (since 2m); 109 remapped pgs
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 201 pgs
    objects: 144.34k objects, 541 GiB
    usage:   1.2 TiB used, 20 TiB / 21 TiB avail
    pgs:     0.498% pgs not active
             87816/433023 objects degraded (20.280%)
             55928/433023 objects misplaced (12.916%)
             91 active+clean
             68 active+undersized+degraded+remapped+backfill_wait
             35 active+remapped+backfill_wait
             6  active+undersized+remapped+backfill_wait
             1  peering

  io:
    client:   6.1 MiB/s rd, 475 KiB/s wr, 7 op/s rd, 39 op/s wr
    recovery: 386 MiB/s, 0 keys/s, 101 objects/s


[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,worker           19m   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
[root@dom16hub101-infra-manager ~]# oc edit no ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab
Edit cancelled, no changes made.
[root@dom16hub101-infra-manager ~]# oc get no --show-labels ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab
NAME                                               STATUS   ROLES                                 AGE   VERSION            LABELS
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,cluster.ocs.openshift.io/openshift-storage=,kubernetes.io/arch=amd64,kubernetes.io/hostname=ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node-role.kubernetes.io/master=,node-role.kubernetes.io/monitor=,node-role.kubernetes.io/worker=,node.openshift.io/os_id=rhcos
[root@dom16hub101-infra-manager ~]# oc label node ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab node-role.kubernetes.io/monitor=
node/ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab labeled
[root@dom16hub101-infra-manager ~]# oc get no
NAME                                               STATUS   ROLES                                 AGE   VERSION
ncpvblvhub-hubmaster-101.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubmaster-102.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   20m   v1.29.10+67d3387
ncpvblvhub-hubmaster-103.ncpvblvhub.t-mobile.lab   Ready    control-plane,master,monitor,worker   74d   v1.29.10+67d3387
ncpvblvhub-hubworker-101.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387
ncpvblvhub-hubworker-102.ncpvblvhub.t-mobile.lab   Ready    gateway,worker                        74d   v1.29.10+67d3387


[root@dom16hub101-infra-manager ~]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph status -c /var/lib/rook/openshift-storage/openshift-storage.config
  cluster:
    id:     27b507a3-b496-4549-9271-a3bc0705dd13
    health: HEALTH_WARN
            Degraded data redundancy: 44107/433023 objects degraded (10.186%), 39 pgs degraded, 43 pgs undersized

  services:
    mon: 3 daemons, quorum a,b,e (age 9m)
    mgr: b(active, since 3h), standbys: a
    mds: 1/1 daemons up, 1 hot standby
    osd: 6 osds: 6 up (since 8m), 6 in (since 8m); 77 remapped pgs
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 201 pgs
    objects: 144.34k objects, 541 GiB
    usage:   1.4 TiB used, 20 TiB / 21 TiB avail
    pgs:     44107/433023 objects degraded (10.186%)
             55928/433023 objects misplaced (12.916%)
             123 active+clean
             37  active+undersized+degraded+remapped+backfill_wait
             35  active+remapped+backfill_wait
             4   active+undersized+remapped+backfill_wait
             2   active+undersized+degraded+remapped+backfilling

  io:
    client:   7.9 MiB/s rd, 355 KiB/s wr, 8 op/s rd, 27 op/s wr
    recovery: 550 MiB/s, 1 keys/s, 145 objects/s


[root@dom16hub101-infra-manager ~]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph status -c /var/lib/rook/openshift-storage/openshift-storage.config
  cluster:
    id:     27b507a3-b496-4549-9271-a3bc0705dd13
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,e (age 18m)
    mgr: b(active, since 3h), standbys: a
    mds: 1/1 daemons up, 1 hot standby
    osd: 6 osds: 6 up (since 16m), 6 in (since 17m); 30 remapped pgs
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 201 pgs
    objects: 144.51k objects, 542 GiB
    usage:   1.6 TiB used, 19 TiB / 21 TiB avail
    pgs:     46224/433527 objects misplaced (10.662%)
             171 active+clean
             28  active+remapped+backfill_wait
             2   active+remapped+backfilling

  io:
    client:   5.7 MiB/s rd, 396 KiB/s wr, 8 op/s rd, 37 op/s wr
    recovery: 155 MiB/s, 41 objects/s

[root@dom16hub101-infra-manager ~]#


```

> Continue the same steps for `master1` and `master3` as well, if you want to replace all three master nodes. 