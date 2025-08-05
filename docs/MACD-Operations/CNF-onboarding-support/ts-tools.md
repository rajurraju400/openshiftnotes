# MACD Guide: Tcpdump and Diagnostic Tools in OpenShift Clusters

This documentation assists the MACD team in running `tcpdump`, `sosreport`, and `must-gather` on the OpenShift cluster.

---

## Guidelines for MACD Team

- Inform the application teams that they are responsible for their own trace collection.  
  > Running `tcpdump` or trace collection is additional validation/troubleshooting initiated by the application teams. They will instruct what needs to be executed.

- CNF teams must specify where they want traces to be collected.  
  > MACD should not guide CNF teams. Simply run the `toolbox` and follow instructions provided by them.

- Share screen during the session.  
  > Screen sharing ensures CNF teams are aware of what is being executed.

- Cleanup after session.  
  > After transferring the `.pcap` file to the infra-manager node, delete it using `rm -f <filename>` to prevent disk pressure on the host OS.

- `tcpdump` should be run on physical or VLAN-based interfaces.  
  > No capture filters should be applied during the `tcpdump` by MACD engineers. All Filters should be applied by CNF owners while reading it from wireshark or equivalent tools. 

---

## Tcpdump collection


> `Note 1`: Collection as much information as possible before joing the call. [ "Name of the cluster", "Application NS name", "Application pod name", "Pod hosted compute name", "vlan name to capture the trace" etc.]


1) Login to node via ssh or debug utitiy 

```
[root@ncputility ~ pancwl_rc]$ ssh core@appworker2-5.ppwncp01.infra.mobi.eastlink.ca
Red Hat Enterprise Linux CoreOS 416.94.202407081958-0
  Part of OpenShift 4.16, RHCOS is a Kubernetes-native operating system
  managed by the Machine Config Operator (`clusteroperator/machine-config`).

WARNING: Direct SSH access to machines is not recommended; instead,
make configuration changes via `machineconfig` objects:
  https://docs.openshift.com/container-platform/4.16/architecture/architecture-rhcos.html

---
[core@appworker2-5 ~]$

or 

[root@ncputility ~ cwl_rc]$oc debug -t node/appworker2-5.ppwncp01.infra.mobi.eastlink.ca
Temporary namespace openshift-debug-99xtp is created for debugging node...
Starting pod/appworker2-5ppwncp01inframobieastlinkca-debug-fm9xk ...
To use host binaries, run `chroot /host`
Pod IP: 10.236.97.53
If you don't see a command prompt, try pressing enter.
sh-5.1# chroot /host
sh-5.1# 
```

2) Trigger toolbox command to execute into a shell which contains all required tools like tcpdump, sosreport etc. 


```
sh-5.1# toolbox
Trying to pull registry.redhat.io/rhel9/support-tools:latest...
Getting image source signatures
Copying blob a0e56de801f5 done   |
Copying blob ec465ce79861 done   |
Copying blob facf1e7dd3e0 done   |
Copying blob cbea42b25984 done   |
Copying config a627accb68 done   |
Writing manifest to image destination
a627accb682adb407580be0d7d707afbcb90abf2f407a0b0519bacafa15dd409
Spawning a container 'toolbox-root' with image 'registry.redhat.io/rhel9/support-tools'
Detected RUN label in the container image. Using that as the default...
b8a833e8ed0aa428271acb952cfb0f870eea66c0465a62fd23e917b0e2217d45
toolbox-root
Container started successfully. To exit, type 'exit'.
[root@appworker2-5 /]#

```


4) Run `tcpdump` command against any linux network interface. 

```
[root@appworker2-5 /]# tcpdump -i br-ex -w br-ex.pcap
dropped privs to tcpdump
tcpdump: listening on br-ex, link-type EN10MB (Ethernet), snapshot length 262144 bytes
^C26702 packets captured
27154 packets received by filter
0 packets dropped by kernel
[root@appworker2-5 /]# file br-ex.pcap
br-ex.pcap: pcap capture file, microsecond ts (little-endian) - version 2.4 (Ethernet, capture length 262144)
[root@appworker2-5 /]# exit
exit
```

5) Locate the file from host OS level for fast transfer, note toolbox files are saved on `/var/lib/containers/storage/` so we will do ing the find command to locate the file easly. 


```
sh-5.1# find /var/lib/containers/storage/ -name br-ex.pcap -print
/var/lib/containers/storage/overlay/b645fb6d5a034493f332f9794cf47967ac50bb8a8e92f26e2c13da18697a5387/diff/br-ex.pcap
sh-5.1#

```

6) Scp to infra-manager node using scp command. if you have a `dedicated infra-manager` ask the application teams where to upload the file.

> `Note 1`: Dont share file via `dedicated infra-manager` node.  its not a file sharing server. 

```
scp -rp /var/lib/containers/storage/overlay/b645fb6d5a034493f332f9794cf47967ac50bb8a8e92f26e2c13da18697a5387/diff/br-ex.pcap root@infra-manager:/tmp/ 
```

7) Delete the file from the node, so prevent causing an disk pressure issue. 

```
toolbox
rm -fr br-ex.pcap
```

> `Note 1`: It is our responsibility to `delete trace files from the OCP node` level. However, removing the trace file after download is `Nokia’s responsibility` (from shared infra-manager node or Jump server).


> `Note 2`: If you copy the trace file to a shared `infra-manager node`, it is still the `responsibility of the application team to delete` the trace file after downloading it.

> `Note 3`: if you have a `dedicated infra-manager` node, Don't share or use this node as file sharing server. Application team should be providing you the IP, user/passwd to where to upload the trace file. 


## Sos report collection 


1) Login to node via ssh or debug utitiy 

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


2) Trigger toolbox command to execute into a shell which contains all required tools like tcpdump, sosreport etc. 


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
3) now use sosreport from here 


```
sos report -k crio.all=on -k crio.logs=on  -k podman.all=on -k podman.logs=on
```


## Must-Gather collection

### References

* [Recovering a node that has lost all networking in OpenShift 4](https://access.redhat.com/solutions/7046419)