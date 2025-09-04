# Storage node replacement 


## Delete the storage node

1) Show the initial status of the storage nodes in the managed cluster (output of oc get nodes) and identify which node will be removed, e.g. storage-0.

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get nodes |grep -i storage
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     25d   v1.29.10+67d3387
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     25d   v1.29.10+67d3387
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
[root@dom14npv101-infra-manager ~ vlabrc]#


```

2) Verify the ceph health status

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config
  cluster:
    id:     a2b0c334-ba7c-4ae1-b3f5-c6d514f19bec
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum f,g,h (age 21h)
    mgr: a(active, since 21h), standbys: b
    mds: 1/1 daemons up, 1 hot standby
    osd: 48 osds: 48 up (since 21h), 48 in (since 23h)
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 1097 pgs
    objects: 190.32k objects, 393 GiB
    usage:   1.2 TiB used, 278 TiB / 279 TiB avail
    pgs:     1097 active+clean

  io:
    client:   8.7 KiB/s rd, 9.9 MiB/s wr, 11 op/s rd, 22 op/s wr

[root@dom14npv101-infra-manager ~ vlabrc]#

```
3) Identify the monitor pod (if any), and OSDs that are running in the node that you need to replace:

```

[root@dom14npv101-infra-manager ~ vlabrc]# oc get pods -n openshift-storage -o wide | grep -i ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net  |grep -i rook-ceph
rook-ceph-crashcollector-73c0594e536089af81dd498574227f77-94vtt   1/1     Running   0             21h   172.28.18.41     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-exporter-73c0594e536089af81dd498574227f77-754b5866njj   1/1     Running   0             21h   172.28.18.42     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-mds-ocs-storagecluster-cephfilesystem-a-795996f7lvsqs   2/2     Running   0             22h   172.28.18.21     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-mds-ocs-storagecluster-cephfilesystem-b-78f7bbf8c2hhg   2/2     Running   0             22h   172.28.18.22     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-mgr-b-5468b7cf-fmwnp                                    4/4     Running   0             22h   172.28.18.7      ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-mon-f-54d858f9cd-m5q76                                  2/2     Running   0             22h   172.28.18.8      ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-operator-7bc4cf5ccd-4lxjr                               1/1     Running   0             22h   172.28.18.39     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-14-6df66b8b99-nmgvq                                 2/2     Running   0             22h   172.28.18.9      ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-21-86cd6b7f7f-498vh                                 2/2     Running   0             22h   172.28.18.12     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-28-698bb96856-vmr8t                                 2/2     Running   0             22h   172.28.18.11     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-34-5f49bdbb85-f528w                                 2/2     Running   0             22h   172.28.18.15     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-4-7495d5f559-zccrg                                  2/2     Running   0             22h   172.28.18.34     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-41-689699f766-clfzm                                 2/2     Running   0             22h   172.28.18.17     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-44-94c7c6565-cz8wg                                  2/2     Running   0             22h   172.28.18.16     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-9-6b966dc5db-28595                                  2/2     Running   0             22h   172.28.18.18     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-rgw-ocs-storagecluster-cephobjectstore-a-788d79bdrltz   2/2     Running   0             22h   172.28.18.38     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-tools-6f854c4bfc-wqhm7                                  1/1     Running   0             22h   172.28.18.30     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
[root@dom14npv101-infra-manager ~ vlabrc]#

```

4) Scale down the deployments of the pods identified in the previous step: (mon, osd, crashcollector)

```

[root@dom14npv101-infra-manager ~ vlabrc]# oc -n openshift-storage scale deployment rook-ceph-crashcollector --replicas=0
oc -n openshift-storage scale deployment rook-ceph-mgr-b  --replicas=0
oc -n openshift-storage scale deployment rook-ceph-mon-f  --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-14 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-21 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-28 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-34 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-4  --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-41 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-44 --replicas=0
oc -n openshift-storage scale deployment rook-ceph-osd-9  --replicas=0
error: no objects passed to scale
deployment.apps/rook-ceph-mgr-b scaled
deployment.apps/rook-ceph-mon-f scaled
deployment.apps/rook-ceph-osd-14 scaled
deployment.apps/rook-ceph-osd-21 scaled
deployment.apps/rook-ceph-osd-28 scaled
deployment.apps/rook-ceph-osd-34 scaled
deployment.apps/rook-ceph-osd-4 scaled
deployment.apps/rook-ceph-osd-41 scaled
deployment.apps/rook-ceph-osd-44 scaled
deployment.apps/rook-ceph-osd-9 scaled
[root@dom14npv101-infra-manager ~ vlabrc]#

```

5) Add the following Annotation for node deletion in the siteconfig.yaml (add crsuppression and crannotation both)


6) To initiate the automated deletion process, begin by deleting the BMH CR of the control plane node that has been previously annotated with the specific “crAnnotation”.

7) Add “crSuppression” to SiteConfig so that node will be removed from the cluster. Note that you need to keep the “crAnnotation” on the node.

```

      - hostName: "ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net"
        role: "worker"
        crSuppression:
        - BareMetalHost
        crAnnotations:
          add:
          BareMetalHost:
            bmac.agent-install.openshift.io/remove-agent-and-node-on-delete: true

```
8) Git add/commit/push the SiteConfig.yaml, so that ArgoCD syncs the updated SiteConfig to the Hub Cluster 
    a. The BMH on Hub cluster should start showing updated status that the node is being deprovisioning. This status change indicates that the node is undergoing the deprovisioning process, a necessary step before its complete removal.

```
[root@dom14npv101-infra-manager ~ hubrc]# oc get bmh -n ncpvnpvlab1 |grep -i storage-101
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   deprovisioning              true             60m
[root@dom14npv101-infra-manager ~ hubrc]#

```
9) Cluster Administrators should wait for the BMH to finish deprovisioning and be fully deleted from the cluster environment. After ~10 minutes (this might take longer or shorter depending on your environment to complete the node clean up):
    a. The storage node “storage-0” is powered off
    b. The BMH resource of the replaced node is deleted on the Hub Cluster.
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get bmh -n ncpvnpvlab1 |grep -i storage
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   provisioned              true             27d
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   provisioned              true             27d
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   provisioned              true             25d
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   provisioned              true             27d
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   provisioned              true             27d
[root@dom14npv101-infra-manager ~ vlabrc]#

```

10)  “oc get node” on cluster shows that the node “storage-101” is no longer part of the cluster, only 2 storage nodes remain

ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net  ---> still part of it. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get nodes |grep -i storage
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     25d   v1.29.10+67d3387
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     25d   v1.29.10+67d3387
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     27d   v1.29.10+67d3387
[root@dom14npv101-infra-manager ~ vlabrc]#

```