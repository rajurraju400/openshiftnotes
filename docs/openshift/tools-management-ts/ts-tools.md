# This documentation help to setup some troubleshooting tools installation on the openshift infra. 


## TCPDUMP


1. login to node via ssh or debug utitiy 

```
[root@ncputility ~ pancwl_rc]$ ssh core@gateway2.panclypcwl01.mnc020.mcc714
Red Hat Enterprise Linux CoreOS 416.94.202407081958-0
  Part of OpenShift 4.16, RHCOS is a Kubernetes-native operating system
  managed by the Machine Config Operator (`clusteroperator/machine-config`).

WARNING: Direct SSH access to machines is not recommended; instead,
make configuration changes via `machineconfig` objects:
  https://docs.openshift.com/container-platform/4.16/architecture/architecture-rhcos.html

---
[core@gateway2 ~]$
```

2. become root and update the toolbox rc file here.
    a. use your hub cluster quay to avoid ssl certificate trust error. 

```
[root@gateway2 ~]# cat /root/.toolboxrc
#REGISTRY=ncputility.panclyphub01.mnc020.mcc714:8443/ocmirror/rhel9
REGISTRY=quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9
IMAGE=support-tools:latest
[root@gateway2 ~]#

```

3. now trigger toolbox command to execute into a shell which contains all required tools like tcpdump, sosreport etc. 


```
[root@gateway2 ~]# toolbox
.toolboxrc file detected, overriding defaults...
Trying to pull quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest...
Getting image source signatures
Copying blob f5e6502d2728 done   |
Copying blob ebc7dc32a098 done   |
Copying config affd08d3be done   |
Writing manifest to image destination
affd08d3bead20c55f40f08270d477b1524d9d7a2db25235956c7858755ef5f3
Spawning a container 'toolbox-root' with image 'quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest'
Detected RUN label in the container image. Using that as the default...
6bdff24c2e5da044965e2cec8eea58c3d86668f3a5bbe1e2d34495e956fdf0d7
toolbox-root
Container started successfully. To exit, type 'exit'.
[root@gateway2 /]#

```


4. now run tcpdump command against any linux network interface. 

```
[root@gateway2 /]# tcpdump -i vlan104 host 10.89.97.162 -n
dropped privs to tcpdump
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on vlan104, link-type EN10MB (Ethernet), snapshot length 262144 bytes
11:09:46.575071 ARP, Request who-has 10.89.97.167 tell 10.89.97.162, length 42
11:09:46.847283 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:47.111266 ARP, Request who-has 10.89.97.166 tell 10.89.97.162, length 42
11:09:47.575002 ARP, Request who-has 10.89.97.167 tell 10.89.97.162, length 42
11:09:47.614353 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:48.110974 ARP, Request who-has 10.89.97.166 tell 10.89.97.162, length 42
11:09:48.398615 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:49.165561 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:49.944591 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:50.708761 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:51.486902 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:52.262277 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:53.022279 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:53.796498 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:54.578752 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:55.339790 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:56.093946 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:56.871023 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:57.655185 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:58.416364 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:59.198508 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:09:59.976760 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:00.160910 IP 10.89.97.165.37680 > 10.89.97.162.bgp: Flags [P.], seq 207097212:207097231, ack 3177745402, win 64, options [nop,nop,TS val 4011175388 ecr 3700362321], length 19: BGP
11:10:00.162044 IP 10.89.97.162.bgp > 10.89.97.165.37680: Flags [.], ack 19, win 23411, options [nop,nop,TS val 3700389294 ecr 4011175388], length 0
11:10:00.738822 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:01.497752 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:02.254817 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:03.028798 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:03.209179 IP 10.89.97.162.bgp > 10.89.97.165.37680: Flags [P.], seq 1:20, ack 19, win 23411, options [nop,nop,TS val 3700392341 ecr 4011175388], length 19: BGP
11:10:03.209205 IP 10.89.97.165.37680 > 10.89.97.162.bgp: Flags [.], ack 20, win 64, options [nop,nop,TS val 4011178436 ecr 3700392341], length 0
11:10:03.798017 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:04.086263 ARP, Request who-has 10.89.97.163 tell 10.89.97.162, length 42
11:10:04.564104 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:05.086213 ARP, Request who-has 10.89.97.163 tell 10.89.97.162, length 42
11:10:05.343276 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:06.086632 ARP, Request who-has 10.89.97.163 tell 10.89.97.162, length 42
11:10:06.110449 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:06.906665 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:07.686809 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:08.455977 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:09.231136 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:10.002335 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:10.792658 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
11:10:11.561799 IP 10.89.97.162.49152 > 10.89.97.165.bfd-control: BCM-LI-SHIM: direction unused, pkt-type unknown, pkt-subtype single VLAN tag, li-id 2097944
^C
44 packets captured
44 packets received by filter
0 packets dropped by kernel
[root@gateway2 /]# 
```


## sos report


1. login to node via ssh or debug utitiy 

```
[root@ncputility ~ pancwl_rc]$ ssh core@gateway2.panclypcwl01.mnc020.mcc714
Red Hat Enterprise Linux CoreOS 416.94.202407081958-0
  Part of OpenShift 4.16, RHCOS is a Kubernetes-native operating system
  managed by the Machine Config Operator (`clusteroperator/machine-config`).

WARNING: Direct SSH access to machines is not recommended; instead,
make configuration changes via `machineconfig` objects:
  https://docs.openshift.com/container-platform/4.16/architecture/architecture-rhcos.html

---
[core@gateway2 ~]$
```

2. become root and update the toolbox rc file here.
    a. use your hub cluster quay to avoid ssl certificate trust error. 

```
[root@gateway2 ~]# cat /root/.toolboxrc
#REGISTRY=ncputility.panclyphub01.mnc020.mcc714:8443/ocmirror/rhel9
REGISTRY=quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9
IMAGE=support-tools:latest
[root@gateway2 ~]#

```

3. now trigger toolbox command to execute into a shell which contains all required tools like tcpdump, sosreport etc. 


```
[root@gateway2 ~]# toolbox
.toolboxrc file detected, overriding defaults...
Trying to pull quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest...
Getting image source signatures
Copying blob f5e6502d2728 done   |
Copying blob ebc7dc32a098 done   |
Copying config affd08d3be done   |
Writing manifest to image destination
affd08d3bead20c55f40f08270d477b1524d9d7a2db25235956c7858755ef5f3
Spawning a container 'toolbox-root' with image 'quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest'
Detected RUN label in the container image. Using that as the default...
6bdff24c2e5da044965e2cec8eea58c3d86668f3a5bbe1e2d34495e956fdf0d7
toolbox-root
Container started successfully. To exit, type 'exit'.
[root@gateway2 /]#

```
4. now use sosreport from here 


```
sos report -k crio.all=on -k crio.logs=on  -k podman.all=on -k podman.logs=on
```


#### References

* [Recovering a node that has lost all networking in OpenShift 4](https://access.redhat.com/solutions/7046419)