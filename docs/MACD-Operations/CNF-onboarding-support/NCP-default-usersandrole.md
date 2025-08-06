# NCP  user's and role's as delivery 


This document outlines the list of approved user IDs and their associated access levels as permitted by management. It serves as a reference for the NCP engineering team to ensure that user and role configurations are strictly within the defined scope. No actions should be taken beyond what is specified in this document.

> Note: All user IDs and privileges must be provisioned exactly as outlined above. Any deviations or additional access requests require explicit approval from management.


## Users and Role management on HUB cluster 

> For `Administrator` level privileges


* `ncpadmin–` `cluster-admin` role – for the NCP team (our team).

* `ncdadmin` – `cluster-admin` role – for the NCD team. This user will be used for NCD git installation (our team)and shared with the NCD team for ongoing lifecycle management.

> Note 1: if your `HUB` cluster does not planned to install `ncd git server`, you can ignore those respective user id creation.


## Users and Role management on NMC/NWC clusters 
> For `Administrator` level privileges

* `ncpadmin` – `cluster-admin` role – for the NCP team (our team).

* `ncdadmin` – `cluster-admin` role – for the NCD team. Used for NCD application installation by NCD team.

* `ncomadmin` – `cluster-admin` role – for the NCOM team. To be used exclusively for NCOM installation.

* `ncom-sa` - (`cluster-admin` role) Service Account - for NCOM Application is used via CaaS registration. We will create it for them.  

> Note 1: if your `NMC/NWC` clusters does not planned to install `ncd` or `ncom`, you can ignore those respective user id creation.

### Cluster-Admin Role Implementation

No additional setup required. Clusterrole `cluster-admin` mapped to user.()

```bash
oc adm policy add-cluster-role-to-user cluster-admin ncpadmin
```



## Role Management for CNF users on NMC/NWC

> For Non-Administrator users.

By default, all CNF application users are assigned the following four roles:

* `Admin` role: Full access to the entire namespace (tenant-admin role for their specific namespace/project).

* `ncp-default-rw-cnf-role`: Access at the namespace level, allowing users to create, update, delete, and schedule backup jobs, network attachments, redisentercluster, etc. 

* `ncp-default-ro-cnf-role`: Access at the cluster level to list, view, watch, and get information for nodes, SCC, NNCP, Metallb IP pool, static routes, backward routes, egress routes, CRDs, profiles, pv etc.


> Note 1: No need to add above four role to any of these users (ncpadmin, ncdadmin,ncomadmin and ncom-sa)

> Note 2: Clarity - CNF id act as read-only for cluster level resources and read-write for tenant level resources.

<!-- Additionally, if users require access to other important resources at the cluster level as read only, we can add those as needed. To existing “ncp-default-cluster-role “, so automatically all cnf users will get the viewer access from there.  -->


### Admin Role Implementation

No additional setup required. Role `admin` mapped to user and namespace:

```bash
oc policy add-role-to-user admin paclypamrf01 -n paclypamrf01
```

---

### Read,Write Custom  Role Implementation

1) Create `ClusterRole` for network attachment:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncp-default-rw-cnf-role
rules:
  - apiGroups: ["k8s.cni.cncf.io"]
    resources: ["network-attachment-definitions"]
    verbs: ["create", "get", "list", "watch", "update", "patch", "delete"]
  - apiGroups: ["cbur.bcmt.local"]
    resources: ["brpolices"]
    verbs: ["create", "get", "list", "watch", "update", "patch"]
  - apiGroups: ["cbur.csf.nokia.com"]
    resources: ["brhooks", "brpolices"]
    verbs: ["create", "get", "list", "watch", "update", "patch"]
  - apiGroups: ["app.redislabs.com"]
    resources: ["redisenterpriseclusters"]
    verbs: ["get", "list", "create", "delete", "update", "patch"]
  - apiGroups: ["app.csf.nokia.com"]
    resources: ["profiles"]
    verbs: ["get", "list", "watch", "patch"]
  - apiGroups: ["charging.nokia.com"]
    resources: ["chargingfunctions"]
    verbs: ["get", "list", "watch", "patch"]
```

2) Bind role to user in their namespace:

```bash
oc create rolebinding ncp-default-rw-cnf-role-paclypamrf01-rolebinding \
  --clusterrole=ncp-default-rw-cnf-role \
  --user=paclypamrf01 \
  --namespace=paclypamrf01
```

3) Validate access:

```bash
oc auth can-i create network-attachment-definitions.k8s.cni.cncf.io --as=paclypamrf01 -n paclypamrf01
oc auth can-i create redisenterpriseclusters --as=paclypamrf01 -n paclypamrf01
oc auth can-i create brpolices --as=paclypamrf01 -n paclypamrf01
```

---



### Read-Only Cluster Infra Role Implementation

1) Create `ClusterRole` for infra read access:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncp-default-ro-cnf-role
rules:
  - apiGroups: ["security.openshift.io"]
    resources: ["securitycontextconstraints"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list"]
  - apiGroups: ["apiextensions.k8s.io"]
    resources: ["customresourcedefinitions"]
    verbs: ["get", "list"]
  - apiGroups: ["compliance.openshift.io"]
    resources: ["profiles"]
    verbs: ["get", "list"]
  - apiGroups: ["nmstate.io"]
    resources: ["nodenetworkconfigurationpolicies"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["metallb.io"]
    resources: ["ipaddresspools"]
    verbs: ["get", "list"]
  - apiGroups: ["k8s.ovn.org"]
    resources: ["egressips"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["k8s.cni.cncf.io"]
    resources: ["network-attachment-definitions"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["topology.node.k8s.io"]
    resources: ["noderesourcetopologies"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["sriovnetwork.openshift.io"]
    resources: ["sriovnetworknodepolicies"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["persistentvolumes"]
    verbs: ["get", "list", "watch"]
```

2) Bind the role:

```bash
oc create clusterrolebinding ncp-default-ro-cnf-role-ppaaa01-binding \
  --clusterrole=ncp-default-ro-cnf-role \
  --user=ppaaa01
```

3) Validate access:

```bash
oc auth can-i get nodes --as=ppaaa01
oc auth can-i get scc --as=ppaaa01
oc auth can-i get crds --as=ppaaa01
oc login -u ppaaa01 -p redhat123
oc get nodes
```
---

## Customer owned user id with read only.  (Optional for certain customer only.)


> [Note:1]
> This user ID should be created only if explicitly requested by the customer.

> [Note:2]
> Create this user ID only during the customer acceptance phase, not before.




### Procedure to `Add` an additional users

1) Retrieve the htpasswd file from the htpass-secret Secret object and save the file to your file system:

```
[root@dom14npv101-infra-manager ~ hub]# oc get secret htpass-secret -ojsonpath={.data.htpasswd} -n openshift-config | base64 --decode > users.htpasswd
[root@dom14npv101-infra-manager ~ hub]# cat users.htpasswd
ncpadmin:$2y$05$DYlpXiwFzfyRioO4hRNq1.ZdFLO3yMz3Pl3gs7.yUpEUKeOGoHX9K
[root@dom14npv101-infra-manager ~ hub]# 
```
2) Add or remove users from the users.htpasswd file.

```
[root@dom14npv101-infra-manager ~ hub]# htpasswd -bB users.htpasswd nokia nokia@123
Adding password for user nokia
[root@dom14npv101-infra-manager ~ hub]# 
```

3) Replace the htpass-secret Secret object with the updated users in the users.htpasswd file:

```
[root@dom14npv101-infra-manager ~ hub]# oc create secret generic htpass-secret --from-file=htpasswd=users.htpasswd --dry-run=client -o yaml -n openshift-config | oc replace -f -
secret/htpass-secret replaced
[root@dom14npv101-infra-manager ~ hub]# 
```

4) Wait for all these pods to be restarted 

```
[root@dom14npv101-infra-manager ~ hub]# oc get pods -n openshift-authentication -o wide |grep -i oauth
oauth-openshift-f446bd5b-58cps   1/1     Running   0          82s   172.20.2.190   ncpvnpvhub-hubmaster-101.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-k8dqx   0/1     Running   0          27s   172.21.0.241   ncpvnpvhub-hubmaster-103.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-v4n6m   1/1     Running   0          55s   172.20.0.134   ncpvnpvhub-hubmaster-102.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
[root@dom14npv101-infra-manager ~ hub]# 
```

5) Validate the login now. 

```
[root@dom14npv101-infra-manager ~ hub]# oc login -u nokia -p nokia@123
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

[root@dom14npv101-infra-manager ~ hub]# oc whoami
nokia
[root@dom14npv101-infra-manager ~ hub]# 

```
---

### Grant cluster level read only access


No additional setup required. Cluster Role `cluster-reader` mapped to customer owned user id:

```bash
oc policy add-cluster-role-to-user cluster-reader customer-admin1
```

---
<!-- 
## Beyond this is still part of future planning. Please do not implement it at this stage.

###  TCPDUMP Role Implementation (under construction)



1) Create the custom role. Here is the sample custom role definition yaml, customize this as per the requirements:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ncp-default-tcpdump
rules:
- apiGroups:
  - ""
  resources:
  - nodes
  verbs:
  - get
  - list
- apiGroups:
  - ""
  resources:
  - namespaces
  verbs:
  - get
  - list
  - watch
  - create
- apiGroups:
  - ""
  resources:
  - pods
  - pods/attach
  verbs:
  - create
  - delete
  - get
  - list
  - watch
```

> apply this role using oc command `oc apply -f ncp-default-tcpdump.yaml`

2) To add the custom role to specific user, execute the following command:

> nokia is the username.

```
oc adm policy add-cluster-role-to-user ncp-default-tcpdump nokia
```


3) Validate with tcpdump execution

```
[root@ncputility ~ pancwl_rc]$ oc login -u nokia -p nokia@123
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 137 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "".
[root@ncputility ~ pancwl_rc]$ oc get nodes |tail -5
storage0.panclypcwl01.mnc020.mcc714      Ready    storage,worker                     82d   v1.29.10+67d3387
storage1.panclypcwl01.mnc020.mcc714      Ready    storage,worker                     82d   v1.29.10+67d3387
storage2.panclypcwl01.mnc020.mcc714      Ready    storage,worker                     82d   v1.29.10+67d3387
storage3.panclypcwl01.mnc020.mcc714      Ready    storage,worker                     82d   v1.29.10+67d3387
storage4.panclypcwl01.mnc020.mcc714      Ready    storage,worker                     82d   v1.29.10+67d3387
[root@ncputility ~ pancwl_rc]$ oc debug -t node/storage1.panclypcwl01.mnc020.mcc714
Starting pod/storage1panclypcwl01mnc020mcc714-debug-4zdjb ...
To use host binaries, run `chroot /host`
Pod IP: 10.89.96.22
If you don't see a command prompt, try pressing enter.
sh-5.1# chroot /host
sh-5.1# toolbox
.toolboxrc file detected, overriding defaults...
Trying to pull quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest...
Getting image source signatures
Copying blob ebc7dc32a098 done   |
Copying blob f5e6502d2728 done   |
Copying config affd08d3be done   |
Writing manifest to image destination
affd08d3bead20c55f40f08270d477b1524d9d7a2db25235956c7858755ef5f3
Spawning a container 'toolbox-root' with image 'quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest'
Detected RUN label in the container image. Using that as the default...
fd81a47b434b6ef9f1f5c1f75f016417ace0424ac444ac160920d1b56317749c
toolbox-root
Container started successfully. To exit, type 'exit'.
[root@storage1 /]# ip a |grep -i vlan
14: tenant-vlan.11@tenant-bond: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9126 qdisc noqueue state UP group default qlen 1000
[root@storage1 /]# tcpdump -i tenant-vlan.11
dropped privs to tcpdump
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on tenant-vlan.11, link-type EN10MB (Ethernet), snapshot length 262144 bytes
00:22:01.223561 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [P.], seq 891630642:891643891, ack 582150265, win 36945, options [nop,nop,TS val 4260967496 ecr 3116894346], length 13249
00:22:01.223694 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [.], ack 13249, win 42521, options [nop,nop,TS val 3116894355 ecr 4260967489], length 0
00:22:01.223728 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [P.], seq 1:45, ack 13249, win 42624, options [nop,nop,TS val 3116894355 ecr 4260967489], length 44
00:22:01.224817 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [P.], seq 45:246, ack 13249, win 42624, options [nop,nop,TS val 3116894356 ecr 4260967489], length 201
00:22:01.224931 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [.], ack 246, win 36944, options [nop,nop,TS val 4260967498 ecr 3116894355], length 0
00:22:01.224932 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [P.], seq 13249:13293, ack 246, win 36944, options [nop,nop,TS val 4260967498 ecr 3116894355], length 44
00:22:01.230811 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [P.], seq 13293:24555, ack 246, win 36944, options [nop,nop,TS val 4260967503 ecr 3116894355], length 11262
00:22:01.230913 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [.], ack 24555, win 42536, options [nop,nop,TS val 3116894362 ecr 4260967498], length 0
00:22:01.230945 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [P.], seq 246:290, ack 24555, win 42624, options [nop,nop,TS val 3116894362 ecr 4260967498], length 44
00:22:01.231996 IP 172.21.1.23.35424 > 172.21.1.3.6802: Flags [P.], seq 290:491, ack 24555, win 42624, options [nop,nop,TS val 3116894363 ecr 4260967498], length 201
00:22:01.232232 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [.], ack 491, win 36943, options [nop,nop,TS val 4260967505 ecr 3116894362], length 0
00:22:01.232233 IP 172.21.1.3.6802 > 172.21.1.23.35424: Flags [P.], seq 24555:24599, ack 491, win 36943, options [nop,nop,TS val 4260967505 ecr 3116894362], length 44
00:22:01.234142 IP 172.21.1.20.48476 > 172.21.1.23.6806: Flags [P.], seq 16618268:16620391, ack 2665739091, win 190, options [nop,nop,TS val 378975619 ecr 1512308539], length 2123
00:22:01.234143 IP 172.21.1.20.56650 > 172.21.1.25.6806: Flags [P.], seq 66939466:66941589, ack 3019954763, win 190, options [nop,nop,TS val 2352592038 ecr 2573341444], length 2123
00:22:01.234179 IP 172.21.1.20.37550 > 172.21.1.5.6806: Flags [P.], seq 536898928:536901051, ack 2721273952, win 190, options [nop,nop,TS val 3815032447 ecr 4261087126], length 2123
00:22:01.234180 IP 172.21.1.20.42496 > 172.21.1.27.6806: Flags [P.], seq 2279422716:2279424839, ack 1228283579, win 190, options [nop,nop,TS val 753256721 ecr 1445287494], length 2123
00:22:01.234306 IP 172.21.1.25.6806 > 172.21.1.20.56650: Flags [P.], seq 1:2124, ack 2123, win 2416, options [nop,nop,TS val 2573344344 ecr 2352592038], length 2123
00:22:01.234315 IP 172.21.1.23.6806 > 172.21.1.20.48476: Flags [P.], seq 1:2124, ack 2123, win 2410, options [nop,nop,TS val 1512311439 ecr 378975619], length 2123
00:22:01.234343 IP 172.21.1.5.6806 > 172.21.1.20.37550: Flags [P.], seq 1:2124, ack 2123, win 2113, options [nop,nop,TS val 4261090026 ecr 3815032447], length 2123
00:22:01.234379 IP 172.21.1.27.6806 > 172.21.1.20.42496: Flags [P.], seq 1:2124, ack 2123, win 2676, options [nop,nop,TS val 1445290394 ecr 753256721], length 2123
00:22:01.234396 IP 172.21.1.20.56650 > 172.21.1.25.6806: Flags [.], ack 2124, win 190, options [nop,nop,TS val 2352592038 ecr 2573344344], length 0
00:22:01.234402 IP 172.21.1.20.48476 > 172.21.1.23.6806: Flags [.], ack 2124, win 190, options [nop,nop,TS val 378975619 ecr 1512311439], length 0
00:22:01.234505 IP 172.21.1.20.37550 > 172.21.1.5.6806: Flags [.], ack 2124, win 190, options [nop,nop,TS val 3815032447 ecr 4261090026], length 0
00:22:01.234537 IP 172.21.1.20.42496 > 172.21.1.27.6806: Flags [.], ack 2124, win 190, options [nop,nop,TS val 753256721 ecr 1445290394], length 0
00:22:01.237103 IP 172.21.1.27.37158 > 172.21.1.4.6802: Flags [.], ack 1012967756, win 40512, options [nop,nop,TS val 1680035224 ecr 16420672], length 0
00:22:01.237103 IP 172.21.1.2.60590 > 172.21.1.7.6802: Flags [.], ack 1116017082, win 43392, options [nop,nop,TS val 3825550554 ecr 581103573], length 0
00:22:01.237104 IP 172.21.1.19.6802 > 172.21.1.11.47258: Flags [.], ack 725570602, win 33408, options [nop,nop,TS val 1704546955 ecr 606498906], length 0
00:22:01.237110 IP 172.21.1.27.40172 > 172.21.1.16.6802: Flags [.], ack 1828746574, win 42763, options [nop,nop,TS val 3228209995 ecr 3785675081], length 0
00:22:01.237112 IP 172.21.1.27.6802 > 172.21.1.24.53758: Flags [.], ack 2581029255, win 40512, options [nop,nop,TS val 876559214 ecr 2297188001], length 0
00:22:01.238104 IP 172.21.1.27.6802 > 172.21.1.7.53514: Flags [.], ack 2578143080, win 43338, options [nop,nop,TS val 2139259988 ecr 593023046], length 0
00:22:01.238110 IP 172.21.1.23.60636 > 172.21.1.16.6802: Flags [.], ack 3061253067, win 43392, options [nop,nop,TS val 3409467790 ecr 465730765], length 0
00:22:01.243103 IP 172.21.1.5.58300 > 172.21.1.30.6802: Flags [.], ack 3801079551, win 43968, options [nop,nop,TS val 1313654200 ecr 3953015095], length 0
00:22:01.245254 IP 172.21.1.9.60686 > 172.21.1.19.6802: Flags [P.], seq 3886789242:3886795319, ack 4202967298, win 35133, options [nop,nop,TS val 3668480800 ecr 724885667], length 6077
00:22:01.245268 IP 172.21.1.19.6802 > 172.21.1.9.60686: Flags [.], ack 6077, win 43537, options [nop,nop,TS val 724886173 ecr 3668480800], length 0
00:22:01.245326 IP 172.21.1.23.6802 > 172.21.1.24.48990: Flags [P.], seq 2121865670:2121879923, ack 3941873936, win 40512, options [nop,nop,TS val 1387138236 ecr 2042625459], length 14253
00:22:01.245327 IP 172.21.1.23.33826 > 172.21.1.4.6802: Flags [P.], seq 937574034:937588287, ack 2453757626, win 43392, options [nop,nop,TS val 3401137216 ecr 577535357], length 14253
^C00:22:01.245336 IP 172.21.1.29.33576 > 172.21.1.27.6802: Flags [P.], seq 2841329512:2841335589, ack 1230720694, win 43392, options [nop,nop,TS val 1809019513 ecr 2541468665], length 6077

37 packets captured
11885 packets received by filter
11538 packets dropped by kernel
[root@storage1 /]#

``` -->