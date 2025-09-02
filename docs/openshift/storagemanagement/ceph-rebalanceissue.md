## Ceph rebalance issues and it's method to solve it.



### ceph rebalance issue, when failed storage/replacement node old OSD causing an stuck or rebalance blocking. 




1) Login to OCP CWL cluster

```
[root@dom14npv101-infra-manager ~ vlabrc]# source  /root/raj/vlabrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 115 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "openshift-storage".
[root@dom14npv101-infra-manager ~ vlabrc]# oc get nodes
NAME                                                       STATUS   ROLES                              AGE     VERSION
ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     3h49m   v1.29.10+67d3387
ncpvnpvlab1-storage-102.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     149m    v1.29.10+67d3387
ncpvnpvlab1-storage-103.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     57d     v1.29.10+67d3387
ncpvnpvlab1-storage-201.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     55d     v1.29.10+67d3387
ncpvnpvlab1-storage-202.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     57d     v1.29.10+67d3387
ncpvnpvlab1-storage-203.ncpvnpvlab1.pnwlab.nsn-rdnet.net   Ready    storage,worker                     3h48m   v1.29.10+67d3387 

output omitted

```

2) look at the ceph to find ceph status to know, is there any OSD's are missing. 


```
bash-5.1$ ceph -s
  cluster:
    id:     d6599242-8a82-410c-aa83-c15b31d8f6c7
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,c (age 4h)
    mgr: a(active, since 11m), standbys: b
    mds: 1/1 daemons up, 1 hot standby
    osd: 46 osds: 46 up (since 10m), 46 in (since 11m)
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 585 pgs
    objects: 38.37k objects, 146 GiB
    usage:   457 GiB used, 267 TiB / 268 TiB avail
    pgs:     585 active+clean

  io:
    client:   135 KiB/s rd, 117 MiB/s wr, 103 op/s rd, 73 op/s wr

bash-5.1$
```

3) Let us find which node missing the OSD but counting the osd's on each nodes. 

```
bash-5.1$ ceph osd tree
ID   CLASS  WEIGHT     TYPE NAME                                                          STATUS  REWEIGHT  PRI-AFF
 -1         267.80737  root default
 -9          40.75330      host ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net
 24    ssd    5.82190          osd.24                                                         up   1.00000  1.00000
 27    ssd    5.82190          osd.27                                                         up   1.00000  1.00000
 31    ssd    5.82190          osd.31                                                         up   1.00000  1.00000
 32    ssd    5.82190          osd.32                                                         up   1.00000  1.00000
 37    ssd    5.82190          osd.37                                                         up   1.00000  1.00000
 38    ssd    5.82190          osd.38                                                         up   1.00000  1.00000
 41    ssd    5.82190          osd.41                                                         up   1.00000  1.00000
-11          46.57520      host ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net
 25    ssd    5.82190          osd.25                                                         up   1.00000  1.00000
 28    ssd    5.82190          osd.28                                                         up   1.00000  1.00000
 29    ssd    5.82190          osd.29                                                         up   1.00000  1.00000
 34    ssd    5.82190          osd.34                                                         up   1.00000  1.00000
 36    ssd    5.82190          osd.36                                                         up   1.00000  1.00000
 42    ssd    5.82190          osd.42                                                         up   1.00000  1.00000
 43    ssd    5.82190          osd.43                                                         up   1.00000  1.00000
 45    ssd    5.82190          osd.45                                                         up   1.00000  1.00000
 -3          46.57520      host ncpvnpvlab1-storage-103-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  0    ssd    5.82190          osd.0                                                          up   1.00000  1.00000
  3    ssd    5.82190          osd.3                                                          up   1.00000  1.00000
  6    ssd    5.82190          osd.6                                                          up   1.00000  1.00000
  9    ssd    5.82190          osd.9                                                          up   1.00000  1.00000
 11    ssd    5.82190          osd.11                                                         up   1.00000  1.00000
 13    ssd    5.82190          osd.13                                                         up   1.00000  1.00000
 17    ssd    5.82190          osd.17                                                         up   1.00000  1.00000
 19    ssd    5.82190          osd.19                                                         up   1.00000  1.00000
 -5          46.57520      host ncpvnpvlab1-storage-201-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  1    ssd    5.82190          osd.1                                                          up   1.00000  1.00000
  4    ssd    5.82190          osd.4                                                          up   1.00000  1.00000
  8    ssd    5.82190          osd.8                                                          up   1.00000  1.00000
 10    ssd    5.82190          osd.10                                                         up   1.00000  1.00000
 14    ssd    5.82190          osd.14                                                         up   1.00000  1.00000
 18    ssd    5.82190          osd.18                                                         up   1.00000  1.00000
 20    ssd    5.82190          osd.20                                                         up   1.00000  1.00000
 21    ssd    5.82190          osd.21                                                         up   1.00000  1.00000
 -7          46.57520      host ncpvnpvlab1-storage-202-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  2    ssd    5.82190          osd.2                                                          up   1.00000  1.00000
  5    ssd    5.82190          osd.5                                                          up   1.00000  1.00000
  7    ssd    5.82190          osd.7                                                          up   1.00000  1.00000
 12    ssd    5.82190          osd.12                                                         up   1.00000  1.00000
 15    ssd    5.82190          osd.15                                                         up   1.00000  1.00000
 16    ssd    5.82190          osd.16                                                         up   1.00000  1.00000
 22    ssd    5.82190          osd.22                                                         up   1.00000  1.00000
 23    ssd    5.82190          osd.23                                                         up   1.00000  1.00000
-13          40.75330      host ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net
 26    ssd    5.82190          osd.26                                                         up   1.00000  1.00000
 30    ssd    5.82190          osd.30                                                         up   1.00000  1.00000
 33    ssd    5.82190          osd.33                                                         up   1.00000  1.00000
 35    ssd    5.82190          osd.35                                                         up   1.00000  1.00000
 39    ssd    5.82190          osd.39                                                         up   1.00000  1.00000
 40    ssd    5.82190          osd.40                                                         up   1.00000  1.00000
 44    ssd    5.82190          osd.44                                                         up   1.00000  1.00000
bash-5.1$
```

4) check out the ceph health in detail, get better view from here

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph health detail
HEALTH_WARN 1 filesystem is degraded; 11 osds down; 3 hosts (23 osds) down; Reduced data availability: 247 pgs inactive; Degraded data redundancy: 5609127/17836029 objects degraded (31.448%), 811 pgs degraded, 839 pgs undersized; 1597 slow ops, oldest one blocked for 16139 sec, daemons [osd.0,osd.10,osd.13,osd.19,osd.22,osd.27,osd.29,osd.3,osd.35,osd.36]... have slow ops.
[WRN] FS_DEGRADED: 1 filesystem is degraded
    fs ocs-storagecluster-cephfilesystem is degraded
[WRN] OSD_DOWN: 11 osds down
    osd.7 (root=default,host=ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.9 (root=default,host=ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.28 (root=default,host=ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.30 (root=default,host=ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.31 (root=default,host=ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.33 (root=default,host=ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.34 (root=default,host=ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.37 (root=default,host=ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.40 (root=default,host=ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.41 (root=default,host=ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
    osd.44 (root=default,host=ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net) is down
[WRN] OSD_HOST_DOWN: 3 hosts (23 osds) down
    host ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net (root=default) (8 osds) is down
    host ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net (root=default) (8 osds) is down
    host ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net (root=default) (7 osds) is down
[WRN] PG_AVAILABILITY: Reduced data availability: 247 pgs inactive
    pg 9.91 is stuck inactive for 4h, current state unknown, last acting []
    pg 9.93 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [45]
    pg 9.97 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [47]
    pg 9.9e is stuck inactive for 4h, current state unknown, last acting []
    pg 9.9f is stuck inactive for 4h, current state undersized+degraded+peered, last acting [5]
    pg 9.a0 is stuck inactive for 4h, current state unknown, last acting []
    pg 9.a6 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [22]
    pg 9.ab is stuck inactive for 4h, current state undersized+degraded+peered, last acting [35]
    pg 9.ae is stuck inactive for 4h, current state undersized+degraded+peered, last acting [25]
    pg 9.af is stuck inactive for 4h, current state undersized+degraded+peered, last acting [8]
    pg 9.b2 is stuck inactive for 4h, current state unknown, last acting []
    pg 9.b3 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [35]
    pg 9.b4 is stuck inactive for 4h, current state unknown, last acting []
    pg 9.c5 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [42]
    pg 9.c6 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 9.c7 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [46]
    pg 9.1e7 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [46]
    pg 9.1eb is stuck inactive for 4h, current state undersized+degraded+peered, last acting [29]
    pg 9.1f5 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [0]
    pg 9.1fa is stuck inactive for 4h, current state undersized+degraded+peered, last acting [22]
    pg 9.1fb is stuck inactive for 4h, current state unknown, last acting []
    pg 11.95 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [46]
    pg 11.98 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [19]
    pg 11.9b is stuck inactive for 4h, current state undersized+degraded+peered, last acting [32]
    pg 11.a0 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [36]
    pg 11.a1 is stuck inactive for 4h, current state unknown, last acting []
    pg 11.a3 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 11.a8 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [23]
    pg 11.ac is stuck inactive for 4h, current state undersized+degraded+peered, last acting [43]
    pg 11.b0 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [39]
    pg 11.b3 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 11.b5 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [10]
    pg 11.b9 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [43]
    pg 11.bb is stuck inactive for 4h, current state unknown, last acting []
    pg 11.bc is stuck inactive for 4h, current state undersized+degraded+peered, last acting [42]
    pg 11.c0 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [15]
    pg 11.c2 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 11.c3 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 12.96 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [23]
    pg 12.9b is stuck inactive for 4h, current state undersized+degraded+peered, last acting [8]
    pg 12.9c is stuck inactive for 4h, current state undersized+degraded+peered, last acting [38]
    pg 12.9d is stuck inactive for 4h, current state undersized+degraded+peered, last acting [10]
    pg 12.ab is stuck inactive for 4h, current state undersized+degraded+peered, last acting [36]
    pg 12.af is stuck inactive for 4h, current state undersized+degraded+peered, last acting [20]
    pg 12.b1 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [0]
    pg 12.b4 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [13]
    pg 12.b5 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [38]
    pg 12.be is stuck inactive for 4h, current state undersized+degraded+peered, last acting [3]
    pg 12.c4 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [23]
    pg 12.c5 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [39]
    pg 12.c7 is stuck inactive for 4h, current state undersized+degraded+peered, last acting [13]
```

5) remove the OSD's which are part of scaled-in storage node 
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd tree
ID   CLASS  WEIGHT     TYPE NAME                                                          STATUS  REWEIGHT  PRI-AFF
 -1         273.62927  root default
 -3          46.57520      host ncpvnpvlab1-storage-101-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  4    ssd    5.82190          osd.4                                                        down         0  1.00000
  9    ssd    5.82190          osd.9                                                        down   1.00000  1.00000
 14    ssd    5.82190          osd.14                                                       down         0  1.00000
 21    ssd    5.82190          osd.21                                                       down         0  1.00000
 28    ssd    5.82190          osd.28                                                       down   1.00000  1.00000
 34    ssd    5.82190          osd.34                                                       down   1.00000  1.00000
 41    ssd    5.82190          osd.41                                                       down   1.00000  1.00000
 44    ssd    5.82190          osd.44                                                       down   1.00000  1.00000
 ```

6) remove those unwanted OSD's completely. 
```
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 4
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 9
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 14
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 21
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 28
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 34
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 41
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 44

osd.4 is already out.
osd.9 is already out.
osd.14 is already out.
osd.21 is already out.
marked out osd.28.
marked out osd.34.
marked out osd.41.
marked out osd.44.
```

7) delete it completely. using purge. 
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 4  --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 9  --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 14 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 21 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 28 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 34 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 41 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 44 --yes-i-really-mean-it

purged osd.4
purged osd.9
purged osd.14
purged osd.21
purged osd.28
purged osd.34
purged osd.41
purged osd.44
```

8) now check, rebalance should be begins at this point. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph -s
  cluster:
    id:     a2b0c334-ba7c-4ae1-b3f5-c6d514f19bec
    health: HEALTH_WARN
            1 filesystem is degraded
            Reduced data availability: 203 pgs inactive
            Degraded data redundancy: 5434540/17836062 objects degraded (30.469%), 800 pgs degraded, 218 pgs undersized
            62 slow ops, oldest one blocked for 24934 sec, daemons [osd.10,osd.13,osd.19,osd.22,osd.35,osd.36,osd.42,osd.45,osd.5] have slow ops.

  services:
    mon: 3 daemons, quorum h,j,k (age 6h)
    mgr: a(active, since 6h), standbys: b
    mds: 1/1 daemons up, 1 standby
    osd: 32 osds: 24 up (since 7h), 24 in (since 119s); 879 remapped pgs

  data:
    volumes: 0/1 healthy, 1 recovering
    pools:   12 pools, 1097 pgs
    objects: 5.95M objects, 20 TiB
    usage:   42 TiB used, 98 TiB / 140 TiB avail
    pgs:     3.829% pgs unknown
             14.676% pgs not active
             5434540/17836062 objects degraded (30.469%)
             1857921/17836062 objects misplaced (10.417%)
             639 active+undersized+degraded+remapped+backfill_wait
             176 active+clean
             157 undersized+degraded+remapped+backfill_wait+peered
             79  active+remapped+backfill_wait
             42  unknown
             4   undersized+degraded+remapped+backfilling+peered

  io:
    client:   2.3 MiB/s wr, 0 op/s rd, 6 op/s wr
    recovery: 1.4 GiB/s, 0 keys/s, 455 objects/s
```