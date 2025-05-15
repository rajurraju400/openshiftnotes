## Method to avoid OCP user profile overlapping issue. 

> this can resolved by create an rc file each cluster/user access. and source before running oc command can prevant. secret will be kubeconfig file be exported to uniq file each new rc files. 

## Problem describe

* when two user or two different shell try to login with two different users or two different clusters, most recent login will be overlapped with old one. example:  both screen will be having same login to user/cluster.


### Create an RC for hub cluster. 

1) login to linux machine and create a rc file for hub cluster 

* `KUBECONFIG` variable should unique between the clusters. so that token will be saved on that particular sheel profile.
* `PS1` this variable should be unique name and can be used as shell reference.

```
[root@ncputility ~ pancwl_rc]$ cat /root/panhubrc
export KUBECONFIG=~/.kube/hubconfig

oc login -u kubeadmin -p NdnkM-SWpwe-SE4Ba-rNSbR https://api.panclyphub01.mnc020.mcc714:6443
PS1="[\u@\h ~ panhub_rc]$ "
[root@ncputility ~ pancwl_rc]$

```

2) To login to this cluster try 

```
[root@ncputility ~ pancwl_rc]$ source /root/panhubrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 103 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "panclypcwl01".
[root@ncputility ~ panhub_rc]$
```

### Create an RC for CWL cluster. 

1) login to linux machine and create a rc file for CWL cluster 

* `KUBECONFIG` variable should unique between the clusters. so that token will be saved on that particular shell profile.
* `PS1` this variable should be unique name and can be used as shell reference.

```
[root@ncputility ~ pancwl_rc]$ cat /root/pancwlrc
export KUBECONFIG=~/.kube/cwlconfig

oc login -u kubeadmin -p Y59eh-d8Poa-sSdyp-9zBvL https://api.panclypcwl01.mnc020.mcc714:6443
PS1="[\u@\h ~ pancwl_rc]$ "

[root@ncputility ~ pancwl_rc]$

```
2) to login to this cluster try 

```
[root@ncputility ~ pancwl_rc]$ source /root/pancwlrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 117 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
[root@ncputility ~ pancwl_rc]$

```
