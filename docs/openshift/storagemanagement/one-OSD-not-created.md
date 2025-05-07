## One or Two OSD not creating recreated post storage node replacement


### Login to the cluster and make sure storage replacement finished fully. 


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

4) assuming here `ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net` node missing one OSD here. but have to find which disk is that fail to create an osd. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get pods  -o wide |grep -i ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net |grep -i osd |grep -i running
rook-ceph-osd-24-6457dffc55-86brj                                 2/2     Running     0               19m     172.31.24.22     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-27-7597d558fc-kw9l9                                 2/2     Running     0               19m     172.31.24.19     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-31-5cdf75ff54-bhmlr                                 2/2     Running     0               19m     172.31.24.24     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-32-6f99fd4845-pqg4m                                 2/2     Running     0               19m     172.31.24.23     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-37-598b85cf5-mjjzk                                  2/2     Running     0               19m     172.31.24.25     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-38-6f9cfbc8d9-wtfrd                                 2/2     Running     0               19m     172.31.24.26     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
rook-ceph-osd-41-6b88b44f56-tlv7m                                 2/2     Running     0               19m     172.31.24.27     ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net   <none>           <none>
[root@dom14npv101-infra-manager ~ vlabrc]# 

```

### Find an method to locate the missing OSD on that particular node.

5) create to command to grep for osd and it's logical disk location on that node. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get pods  -o wide |grep -i ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net |grep -i osd |grep -i running |awk '{print "oc logs "$1 " |grep -i nvme"}'
oc logs rook-ceph-osd-24-6457dffc55-86brj |grep -i nvme
oc logs rook-ceph-osd-27-7597d558fc-kw9l9 |grep -i nvme
oc logs rook-ceph-osd-31-5cdf75ff54-bhmlr |grep -i nvme
oc logs rook-ceph-osd-32-6f99fd4845-pqg4m |grep -i nvme
oc logs rook-ceph-osd-37-598b85cf5-mjjzk |grep -i nvme
oc logs rook-ceph-osd-38-6f9cfbc8d9-wtfrd |grep -i nvme
oc logs rook-ceph-osd-41-6b88b44f56-tlv7m |grep -i nvme
[root@dom14npv101-infra-manager ~ vlabrc]# 
```

6) run that commands to find the OSD name and it;s corresponding disk logical naming details here. 

```
[root@dom14npv101-infra-manager ~ vlabrc]#  oc logs rook-ceph-osd-24-6457dffc55-86brj |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:08.392+0000 7f3d38717640  1 osd.24 185 _collect_metadata nvme2n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-27-7597d558fc-kw9l9 |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:04.368+0000 7f793d509640  1 osd.27 181 _collect_metadata nvme7n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-31-5cdf75ff54-bhmlr |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:13.727+0000 7fbb2a4ee640  1 osd.31 191 _collect_metadata nvme5n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-32-6f99fd4845-pqg4m |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:12.739+0000 7faad8b28640  1 osd.32 190 _collect_metadata nvme6n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-37-598b85cf5-mjjzk |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:21.737+0000 7f7fee8fd640  1 osd.37 199 _collect_metadata nvme4n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-38-6f9cfbc8d9-wtfrd |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:23.718+0000 7f1f6e8b7640  1 osd.38 201 _collect_metadata nvme0n1:
[root@dom14npv101-infra-manager ~ vlabrc]# oc logs rook-ceph-osd-41-6b88b44f56-tlv7m |grep -i nvme
Defaulted container "osd" out of: osd, log-collector, blkdevmapper (init), activate (init), expand-bluefs (init), chown-container-data-dir (init)
debug 2025-05-06T18:36:27.752+0000 7fe6362c5640  1 osd.41 205 _collect_metadata nvme1n1:
[root@dom14npv101-infra-manager ~ vlabrc]# 

```


7) now login to respective storage node via ssh or oc debug so that compare the list osd disk and find out the missing OSD disk and then format that particular drive alone. 

```
ssh core@ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net
Red Hat Enterprise Linux CoreOS 416.94.202411201433-0
  Part of OpenShift 4.16, RHCOS is a Kubernetes-native operating system
  managed by the Machine Config Operator (`clusteroperator/machine-config`).

WARNING: Direct SSH access to machines is not recommended; instead,
make configuration changes via `machineconfig` objects:
  https://docs.openshift.com/container-platform/4.16/architecture/architecture-rhcos.html

---
Last login: Tue May  6 18:16:30 2025 from 10.203.197.23
[core@ncpvnpvlab1-storage-101 ~]$ sudos u -= ^C
[core@ncpvnpvlab1-storage-101 ~]$ sudo su -
Last login: Tue May  6 18:16:35 UTC 2025 on pts/0
[root@ncpvnpvlab1-storage-101 ~]# lsblk
NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0         7:0    0   5.8T  0 loop
loop1         7:1    0   5.8T  0 loop
loop2         7:2    0   5.8T  0 loop
loop3         7:3    0   5.8T  0 loop
loop4         7:4    0   5.8T  0 loop
loop5         7:5    0   5.8T  0 loop
loop6         7:6    0   5.8T  0 loop
nbd0         43:0    0     0B  0 disk
nbd1         43:32   0     0B  0 disk
nbd2         43:64   0     0B  0 disk
nbd3         43:96   0     0B  0 disk
nbd4         43:128  0     0B  0 disk
nbd5         43:160  0     0B  0 disk
nbd6         43:192  0     0B  0 disk
nbd7         43:224  0     0B  0 disk
nvme3n1     259:1    0 894.2G  0 disk
├─nvme3n1p1 259:2    0     1M  0 part
├─nvme3n1p2 259:3    0   127M  0 part
├─nvme3n1p3 259:4    0   384M  0 part /boot
├─nvme3n1p4 259:5    0   460G  0 part /var
│                                     /sysroot/ostree/deploy/rhcos/var
│                                     /usr
│                                     /etc
│                                     /
│                                     /sysroot
└─nvme3n1p5 259:6    0 433.7G  0 part
nvme0n1     259:7    0   5.8T  0 disk
nvme2n1     259:8    0   5.8T  0 disk
nvme8n1     259:9    0   5.8T  0 disk
nvme5n1     259:10   0   5.8T  0 disk
nvme6n1     259:11   0   5.8T  0 disk
nvme1n1     259:12   0   5.8T  0 disk
nvme7n1     259:13   0   5.8T  0 disk
nvme4n1     259:14   0   5.8T  0 disk
nbd8         43:256  0     0B  0 disk
nbd9         43:288  0     0B  0 disk
nbd10        43:320  0     0B  0 disk
nbd11        43:352  0     0B  0 disk
nbd12        43:384  0     0B  0 disk
nbd13        43:416  0     0B  0 disk
nbd14        43:448  0     0B  0 disk
nbd15        43:480  0     0B  0 disk
[root@ncpvnpvlab1-storage-101 ~]#
```

8) on based on output from 6 and compared with output from 7. `nvme8n1` is missed out. so this drive need to formated. 

```
[root@ncpvnpvlab1-storage-101 ~]# wipefs -a -f /dev/nvme8n1
/dev/nvme8n1: 22 bytes were erased at offset 0x00000000 (ceph_bluestore): 62 6c 75 65 73 74 6f 72 65 20 62 6c 6f 63 6b 20 64 65 76 69 63 65
[root@ncpvnpvlab1-storage-101 ~]#
sgdisk -Z /dev/nvme8n1
Creating new GPT entries in memory.
GPT data structures destroyed! You may now partition the disk using fdisk or
other utilities.
[root@ncpvnpvlab1-storage-101 ~]# exit
logout
[core@ncpvnpvlab1-storage-101 ~]$ exit
logout
Connection to ncpvnpvlab1-storage-101.ncpvnpvlab1.pnwlab.nsn-rdnet.net closed.

```

9) wait for lso getting the pv created automationcally. 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                                                              STORAGECLASS          VOLUMEATTRIBUTESCLASS   REASON   AGE
local-pv-1189c26a                          5961Gi     RWO            Delete           Bound       openshift-storage/ocs-deviceset-localblockstorage-1-data-14svnkz   localblockstorage     <unset>                          22s
```

10) wait for 4 mins, this ceph OSD will be auto created and ceph status should be having correct list of OSD's here .


```
bash-5.1$ ceph -s
  cluster:
    id:     d6599242-8a82-410c-aa83-c15b31d8f6c7
    health: HEALTH_OK

  services:
    mon: 3 daemons, quorum a,b,c (age 4h)
    mgr: a(active, since 67m), standbys: b
    mds: 1/1 daemons up, 1 hot standby
    osd: 47 osds: 47 up (since 41m), 47 in (since 42m)
    rgw: 1 daemon active (1 hosts, 1 zones)

  data:
    volumes: 1/1 healthy
    pools:   12 pools, 585 pgs
    objects: 44.41k objects, 169 GiB
    usage:   535 GiB used, 279 TiB / 279 TiB avail
    pgs:     585 active+clean

  io:
    client:   1023 B/s rd, 224 MiB/s wr, 1 op/s rd, 62 op/s wr

bash-5.1$
```