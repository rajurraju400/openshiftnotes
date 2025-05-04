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
[WRN] PG_DEGRADED: Degraded data redundancy: 5609127/17836029 objects degraded (31.448%), 811 pgs degraded, 839 pgs undersized
    pg 9.bf is active+undersized+degraded, acting [29,35]
    pg 9.c0 is stuck undersized for 4h, current state active+undersized+degraded, last acting [0,45]
    pg 9.c1 is stuck undersized for 3h, current state active+undersized+remapped, last acting [46,45]
    pg 9.c2 is stuck undersized for 4h, current state active+undersized+degraded, last acting [10,13]
    pg 9.c3 is stuck undersized for 4h, current state active+undersized+degraded, last acting [27,22]
    pg 9.c4 is stuck undersized for 4h, current state active+undersized+degraded, last acting [36,45]
    pg 9.c5 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [42]
    pg 9.c6 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [3]
    pg 9.c7 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [46]
    pg 9.1e4 is stuck undersized for 4h, current state active+undersized+degraded, last acting [39,25]
    pg 9.1e5 is stuck undersized for 4h, current state active+undersized+degraded, last acting [10,43]
    pg 9.1e6 is stuck undersized for 4h, current state active+undersized+degraded, last acting [39,5]
    pg 9.1e7 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [46]
    pg 9.1e8 is stuck undersized for 4h, current state active+undersized+degraded, last acting [23,8]
    pg 9.1e9 is stuck undersized for 4h, current state active+undersized+degraded, last acting [47,27]
    pg 9.1ea is stuck undersized for 4h, current state active+undersized+degraded, last acting [19,36]
    pg 9.1eb is stuck undersized for 4h, current state undersized+degraded+peered, last acting [29]
    pg 9.1ec is stuck undersized for 4h, current state active+undersized+degraded, last acting [3,42]
    pg 9.1ed is stuck undersized for 4h, current state active+undersized+degraded, last acting [15,43]
    pg 9.1ee is stuck undersized for 4h, current state active+undersized+degraded, last acting [19,36]
    pg 9.1ef is stuck undersized for 4h, current state active+undersized+degraded, last acting [0,20]
    pg 9.1f1 is stuck undersized for 4h, current state active+undersized+degraded, last acting [47,0]
    pg 9.1f2 is stuck undersized for 4h, current state active+undersized+degraded, last acting [42,35]
    pg 9.1f3 is stuck undersized for 4h, current state active+undersized+degraded, last acting [47,27]
    pg 9.1f4 is stuck undersized for 4h, current state active+undersized+degraded, last acting [36,46]
    pg 9.1f5 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [0]
    pg 9.1f6 is stuck undersized for 3h, current state active+undersized+degraded, last acting [38,46]
    pg 9.1f7 is stuck undersized for 4h, current state active+undersized+degraded, last acting [3,0]
    pg 9.1f8 is stuck undersized for 4h, current state active+undersized+degraded, last acting [3,15]
    pg 9.1f9 is stuck undersized for 4h, current state active+undersized+degraded, last acting [15,43]
    pg 9.1fa is stuck undersized for 4h, current state undersized+degraded+peered, last acting [22]
    pg 9.1fc is stuck undersized for 4h, current state active+undersized+degraded, last acting [35,29]
    pg 9.1fd is stuck undersized for 4h, current state active+undersized+degraded, last acting [5,19]
    pg 9.1fe is stuck undersized for 4h, current state active+undersized+degraded, last acting [29,0]
    pg 9.1ff is stuck undersized for 4h, current state active+undersized+degraded, last acting [43,27]
    pg 11.bd is stuck undersized for 4h, current state active+undersized+degraded, last acting [10,42]
    pg 11.c0 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [15]
    pg 11.c1 is stuck undersized for 4h, current state active+undersized+degraded, last acting [5,32]
    pg 11.c2 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [3]
    pg 11.c3 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [3]
    pg 11.c4 is stuck undersized for 4h, current state active+undersized+degraded, last acting [42,39]
    pg 11.c5 is stuck undersized for 4h, current state active+undersized+degraded, last acting [46,27]
    pg 11.c7 is stuck undersized for 4h, current state active+undersized+degraded, last acting [42,36]
    pg 12.c0 is stuck undersized for 4h, current state active+undersized+degraded, last acting [47,23]
    pg 12.c1 is stuck undersized for 4h, current state active+undersized+degraded, last acting [25,32]
    pg 12.c2 is stuck undersized for 4h, current state active+undersized+degraded, last acting [20,0]
    pg 12.c3 is stuck undersized for 4h, current state active+undersized+degraded, last acting [22,13]
    pg 12.c4 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [23]
    pg 12.c5 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [39]
    pg 12.c6 is stuck undersized for 4h, current state active+undersized+degraded, last acting [29,32]
    pg 12.c7 is stuck undersized for 4h, current state undersized+degraded+peered, last acting [13]
[WRN] SLOW_OPS: 1597 slow ops, oldest one blocked for 16139 sec, daemons [osd.0,osd.10,osd.13,osd.19,osd.22,osd.27,osd.29,osd.3,osd.35,osd.36]... have slow ops.
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph -s
  cluster:
    id:     a2b0c334-ba7c-4ae1-b3f5-c6d514f19bec
    health: HEALTH_WARN
            1 filesystem is degraded
            11 osds down
            3 hosts (23 osds) down
            Reduced data availability: 247 pgs inactive
            Degraded data redundancy: 5609127/17836029 objects degraded (31.448%), 811 pgs degraded, 839 pgs undersized
            1597 slow ops, oldest one blocked for 16159 sec, daemons [osd.0,osd.10,osd.13,osd.19,osd.22,osd.27,osd.29,osd.3,osd.35,osd.36]... have slow ops.

  services:
    mon: 3 daemons, quorum h,j,k (age 4h)
    mgr: a(active, since 4h), standbys: b
    mds: 1/1 daemons up, 1 standby
    osd: 47 osds: 24 up (since 4h), 35 in (since 4h); 42 remapped pgs

  data:
    volumes: 0/1 healthy, 1 recovering
    pools:   12 pools, 1097 pgs
    objects: 5.95M objects, 20 TiB
    usage:   41 TiB used, 99 TiB / 140 TiB avail
    pgs:     3.829% pgs unknown
             18.687% pgs not active
             5609127/17836029 objects degraded (31.448%)
             279094/17836029 objects misplaced (1.565%)
             610 active+undersized+degraded
             201 undersized+degraded+peered
             190 active+clean
             42  unknown
             26  active+clean+remapped
             16  active+undersized+remapped
             8   active+undersized
             4   undersized+peered

[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph -s
E0501 23:49:07.749890 2538728 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0501 23:49:07.787031 2538728 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0501 23:49:07.822712 2538728 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
E0501 23:49:07.855100 2538728 memcache.go:265] couldn't get current server API group list: the server has asked for the client to provide credentials
error: You must be logged in to the server (the server has asked for the client to provide credentials)
[root@dom14npv101-infra-manager ~ vlabrc]# source /root/raj/
alarms/                                health.py                              ingress_ca.crt                         ncp-health.py                          security/
amc-backup/                            htpasswdhub                            install-config                         new.py                                 storage-logging-loki-compactor-0.yaml
backup-etcd/                           htpasswdmang                           kubeadmin.yaml                         oauth.yaml                             testing.txt
beacon.k8s.worker.tar                  htpasswdnlab                           localcert.crt                          pull_secret_cwl_dockerconfigjson.json  users.htpasswd
cephvlanrc.yaml                        hubconfig                              management_new_health_output.txt       registry-cas.yaml                      vlab1config
fedora-tools.tar.gz                    hub_new_health_output.txt              managementrc                           resourcequota.yaml                     vlabrc
git/                                   hubrc                                  managementrcconfig                     rr.txt                                 vlabrc_new_health_output.txt
[root@dom14npv101-infra-manager ~ vlabrc]# source /root/raj/vlabrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 115 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "openshift-storage".
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph -s
  cluster:
    id:     a2b0c334-ba7c-4ae1-b3f5-c6d514f19bec
    health: HEALTH_WARN
            1 filesystem is degraded
            11 osds down
            3 hosts (23 osds) down
            Reduced data availability: 247 pgs inactive
            Degraded data redundancy: 5609127/17836029 objects degraded (31.448%), 811 pgs degraded, 839 pgs undersized
            1597 slow ops, oldest one blocked for 24624 sec, daemons [osd.0,osd.10,osd.13,osd.19,osd.22,osd.27,osd.29,osd.3,osd.35,osd.36]... have slow ops.

  services:
    mon: 3 daemons, quorum h,j,k (age 6h)
    mgr: a(active, since 6h), standbys: b
    mds: 1/1 daemons up, 1 standby
    osd: 47 osds: 24 up (since 7h), 35 in (since 6h); 42 remapped pgs

  data:
    volumes: 0/1 healthy, 1 recovering
    pools:   12 pools, 1097 pgs
    objects: 5.95M objects, 20 TiB
    usage:   41 TiB used, 99 TiB / 140 TiB avail
    pgs:     3.829% pgs unknown
             18.687% pgs not active
             5609127/17836029 objects degraded (31.448%)
             279094/17836029 objects misplaced (1.565%)
             610 active+undersized+degraded
             201 undersized+degraded+peered
             190 active+clean
             42  unknown
             26  active+clean+remapped
             16  active+undersized+remapped
             8   active+undersized
             4   undersized+peered

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
 -7          40.75330      host ncpvnpvlab1-storage-102-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  7    ssd    5.82190          osd.7                                                        down   1.00000  1.00000
 11    ssd    5.82190          osd.11                                                       down         0  1.00000
 17    ssd    5.82190          osd.17                                                       down         0  1.00000
 18    ssd    5.82190          osd.18                                                       down         0  1.00000
 24    ssd    5.82190          osd.24                                                       down         0  1.00000
 31    ssd    5.82190          osd.31                                                       down   1.00000  1.00000
 33    ssd    5.82190          osd.33                                                       down   1.00000  1.00000
 -9          46.57520      host ncpvnpvlab1-storage-103-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  0    ssd    5.82190          osd.0                                                          up   1.00000  1.00000
  5    ssd    5.82190          osd.5                                                          up   1.00000  1.00000
 10    ssd    5.82190          osd.10                                                         up   1.00000  1.00000
 15    ssd    5.82190          osd.15                                                         up   1.00000  1.00000
 23    ssd    5.82190          osd.23                                                         up   1.00000  1.00000
 25    ssd    5.82190          osd.25                                                         up   1.00000  1.00000
 35    ssd    5.82190          osd.35                                                         up   1.00000  1.00000
 36    ssd    5.82190          osd.36                                                         up   1.00000  1.00000
-11          46.57520      host ncpvnpvlab1-storage-201-ncpvnpvlab1-pnwlab-nsn-rdnet-net
 19    ssd    5.82190          osd.19                                                         up   1.00000  1.00000
 22    ssd    5.82190          osd.22                                                         up   1.00000  1.00000
 32    ssd    5.82190          osd.32                                                         up   1.00000  1.00000
 42    ssd    5.82190          osd.42                                                         up   1.00000  1.00000
 43    ssd    5.82190          osd.43                                                         up   1.00000  1.00000
 45    ssd    5.82190          osd.45                                                         up   1.00000  1.00000
 46    ssd    5.82190          osd.46                                                         up   1.00000  1.00000
 47    ssd    5.82190          osd.47                                                         up   1.00000  1.00000
-13          46.57520      host ncpvnpvlab1-storage-202-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  3    ssd    5.82190          osd.3                                                          up   1.00000  1.00000
  8    ssd    5.82190          osd.8                                                          up   1.00000  1.00000
 13    ssd    5.82190          osd.13                                                         up   1.00000  1.00000
 20    ssd    5.82190          osd.20                                                         up   1.00000  1.00000
 27    ssd    5.82190          osd.27                                                         up   1.00000  1.00000
 29    ssd    5.82190          osd.29                                                         up   1.00000  1.00000
 38    ssd    5.82190          osd.38                                                         up   1.00000  1.00000
 39    ssd    5.82190          osd.39                                                         up   1.00000  1.00000
 -5          46.57520      host ncpvnpvlab1-storage-203-ncpvnpvlab1-pnwlab-nsn-rdnet-net
  2    ssd    5.82190          osd.2                                                        down         0  1.00000
  6    ssd    5.82190          osd.6                                                        down         0  1.00000
 12    ssd    5.82190          osd.12                                                       down         0  1.00000
 16    ssd    5.82190          osd.16                                                       down         0  1.00000
 26    ssd    5.82190          osd.26                                                       down         0  1.00000
 30    ssd    5.82190          osd.30                                                       down   1.00000  1.00000
 37    ssd    5.82190          osd.37                                                       down   1.00000  1.00000
 40    ssd    5.82190          osd.40                                                       down   1.00000  1.00000
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 4,9
Error EINVAL: Expected option value to be integer, got '4,9'invalid osd id-1
command terminated with exit code 22
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 4
osd.4 is already out.
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 9
marked out osd.9.
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 14
osd.14 is already out.
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out  ^C
[root@dom14npv101-infra-manager ~ vlabrc]#
[root@dom14npv101-infra-manager ~ vlabrc]#
[root@dom14npv101-infra-manager ~ vlabrc]#
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 4
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 9
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 14
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 21
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 28
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 34
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 41
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 44
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 7
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 11
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 17
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 18
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 24
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 31
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 33
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 2
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 6
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 12
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 16
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 26
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 30
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 37
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd out 40
osd.4 is already out.
osd.9 is already out.
osd.14 is already out.
osd.21 is already out.
marked out osd.28.
marked out osd.34.
marked out osd.41.
marked out osd.44.
marked out osd.7.
osd.11 is already out.
osd.17 is already out.
osd.18 is already out.
osd.24 is already out.
marked out osd.31.
marked out osd.33.
osd.2 is already out.
osd.6 is already out.
osd.12 is already out.
osd.16 is already out.
osd.26 is already out.
marked out osd.30.
marked out osd.37.
marked out osd.40.
[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 4  --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 9  --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 14 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 21 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 28 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 34 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 41 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 44 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 7  --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 11 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 17 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 18 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 24 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 31 --yes-i-really-mean-it
oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph osd purge 33 --yes-i-really-mean-it
purged osd.4
purged osd.9
purged osd.14
purged osd.21
purged osd.28
purged osd.34
purged osd.41
purged osd.44
purged osd.7
purged osd.11
purged osd.17
purged osd.18
purged osd.24
purged osd.31
purged osd.33
[root@dom14npv101-infra-manager ~ vlabrc]#
[root@dom14npv101-infra-manager ~ vlabrc]#
[root@dom14npv101-infra-manager ~ vlabrc]#
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

[root@dom14npv101-infra-manager ~ vlabrc]# oc rsh -n openshift-storage pod/$CEPH_TOOL_POD ceph -s
  cluster:
    id:     a2b0c334-ba7c-4ae1-b3f5-c6d514f19bec
    health: HEALTH_WARN
            1 filesystem is degraded
            Reduced data availability: 203 pgs inactive
            Degraded data redundancy: 5429732/17836062 objects degraded (30.442%), 800 pgs degraded, 218 pgs undersized
            62 slow ops, oldest one blocked for 24939 sec, daemons [osd.10,osd.13,osd.19,osd.22,osd.35,osd.36,osd.42,osd.45,osd.5] have slow ops.

  services:
    mon: 3 daemons, quorum h,j,k (age 6h)
    mgr: a(active, since 6h), standbys: b
    mds: 1/1 daemons up, 1 standby
    osd: 32 osds: 24 up (since 7h), 24 in (since 2m); 879 remapped pgs

  data:
    volumes: 0/1 healthy, 1 recovering
    pools:   12 pools, 1097 pgs
    objects: 5.95M objects, 20 TiB
    usage:   42 TiB used, 98 TiB / 140 TiB avail
    pgs:     3.829% pgs unknown
             14.676% pgs not active
             5429732/17836062 objects degraded (30.442%)
             1857921/17836062 objects misplaced (10.417%)
             639 active+undersized+degraded+remapped+backfill_wait
             176 active+clean
             157 undersized+degraded+remapped+backfill_wait+peered
             79  active+remapped+backfill_wait
             42  unknown
             4   undersized+degraded+remapped+backfilling+peered

  io:
    client:   1.5 MiB/s wr, 0 op/s rd, 6 op/s wr
    recovery: 1.7 GiB/s, 0 keys/s, 507 objects/s

[root@dom14npv101-infra-manager ~ vlabrc]# 