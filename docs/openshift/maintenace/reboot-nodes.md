# Rebooting nodes on the openshift cluster 

> steps to show, boot on master, worker/gateway and storage. 



## Storage node reboot

1. login to right cluster using cluster-admin based role. 

2. get the list of storage nodes and also check the ceph status. 
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get no |grep -i storage
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     24d   v1.29.10+67d3387
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     24d   v1.29.10+67d3387
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
[root@dom14npv101-infra-manager ~ vlabrc]# 

[root@dom14npv101-infra-manager ~ vlabrc]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config
```


3. define a variable called and value as respective storage node, easy run of reboot
```
[root@dom14npv101-infra-manager ~ vlabrc]# node=ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net

```

4. get the list ceph storage related pods 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc -n openshift-storage get po -o wide | grep -e mon -e osd | grep  ${node}|grep -iv complete|awk '{print $1}'
rook-ceph-osd-12-589c6485c9-ptqs7
rook-ceph-osd-16-74cbc54b4f-tg8lw
rook-ceph-osd-2-7fcc4ff664-hjc2w
rook-ceph-osd-26-67d86fbf5d-lqdv8
rook-ceph-osd-30-78fb4f588b-474jn
rook-ceph-osd-37-bd549c676-jn5ld
rook-ceph-osd-40-5b4ddb6d7d-7qd8z
rook-ceph-osd-6-5b64cf8d49-n55zf
[root@dom14npv101-infra-manager ~ vlabrc]# 
```

5. use notepad++ to create these following commands to remove those pods on that host. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc -n openshift-storage scale deployment rook-ceph-osd-12 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-16 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-2  --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-26 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-30 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-37 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-40 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-6  --replicas=0
deployment.apps/rook-ceph-osd-12 scaled
deployment.apps/rook-ceph-osd-16 scaled
deployment.apps/rook-ceph-osd-2 scaled
deployment.apps/rook-ceph-osd-26 scaled
deployment.apps/rook-ceph-osd-30 scaled
deployment.apps/rook-ceph-osd-37 scaled
deployment.apps/rook-ceph-osd-40 scaled
deployment.apps/rook-ceph-osd-6 scaled
[root@dom14npv101-infra-manager ~ vlabrc]#
```

6. Completely drain that storage node, using oc adm command 

```
[root@dom14npv101-infra-manager ~ vlabrc]#oc adm drain ${node} --delete-emptydir-data --ignore-daemonsets=true --timeout=500s --force
node/ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net cordoned
Warning: ignoring DaemonSet-managed Pods: openshift-cluster-node-tuning-operator/tuned-kqqfn, openshift-dns/dns-default-27nmr, openshift-dns/node-resolver-4dcng, openshift-image-registry/node-ca-2xtbk, openshift-ingress-canary/ingress-canary-285m2, openshift-local-storage/diskmaker-discovery-zmmwj, openshift-local-storage/diskmaker-manager-dvpjq, openshift-logging/collector-7g5zv, openshift-machine-config-operator/machine-config-daemon-c7c4v, openshift-monitoring/node-exporter-gsh5l, openshift-multus/multus-6q7c8, openshift-multus/multus-additional-cni-plugins-pwq85, openshift-multus/network-metrics-daemon-f6flp, openshift-multus/whereabouts-reconciler-fjpmv, openshift-network-diagnostics/network-check-target-9h7cj, openshift-network-operator/iptables-alerter-km8jq, openshift-nmstate/nmstate-handler-6hmz9, openshift-operators/istio-cni-node-v2-5-4qpnk, openshift-ovn-kubernetes/ovnkube-node-w672f, openshift-storage/csi-cephfsplugin-ck4mf, openshift-storage/csi-rbdplugin-gkmjm
evicting pod openshift-storage/rook-ceph-osd-6-5b64cf8d49-n55zf
evicting pod openshift-compliance/openscap-pod-24dd5998a72563f75be98757ffbe02e424df617e
evicting pod openshift-storage/rook-ceph-crashcollector-9c7a6e51d7dc201a808c754612468a82-j84n5
evicting pod openshift-storage/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-78f7bbf8bn4rl
evicting pod openshift-storage/rook-ceph-mgr-b-5468b7cf-nx4d4
evicting pod openshift-storage/rook-ceph-osd-40-5b4ddb6d7d-7qd8z
evicting pod openshift-storage/rook-ceph-exporter-9c7a6e51d7dc201a808c754612468a82-c854b4r2tn4
evicting pod openshift-compliance/openscap-pod-5f54688367da49304dfd83a2e0d564582b073f2b
pod/openscap-pod-5f54688367da49304dfd83a2e0d564582b073f2b evicted
pod/openscap-pod-24dd5998a72563f75be98757ffbe02e424df617e evicted
pod/rook-ceph-crashcollector-9c7a6e51d7dc201a808c754612468a82-j84n5 evicted
pod/rook-ceph-mgr-b-5468b7cf-nx4d4 evicted
pod/rook-ceph-exporter-9c7a6e51d7dc201a808c754612468a82-c854b4r2tn4 evicted
pod/rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-78f7bbf8bn4rl evicted
node/ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net drained
[root@dom14npv101-infra-manager ~ vlabrc]#
```

7. reboot the respective storage node using following command. 
```
[root@dom14npv101-infra-manager ~ vlabrc]#oc debug node/${node} -- chroot /host systemctl reboot 
```

8. waiting for node to be fully up. then check the kubelet status 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get no |grep -i storage
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     24d   v1.29.10+67d3387
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     24d   v1.29.10+67d3387
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready                      storage,worker                     26d   v1.29.10+67d3387
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready,sechd-disable        storage,worker                     26d   v1.29.10+67d3387
[root@dom14npv101-infra-manager ~ vlabrc]# 
```

9. uncordon the storage node.

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc adm uncordon ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net 
```

10. check the ceph health and wait for all osd to be fully up.  give 10mins

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config
```