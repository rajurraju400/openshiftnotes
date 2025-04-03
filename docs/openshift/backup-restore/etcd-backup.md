# Control plane backup 

## Backing up etcd 

etcd is the key-value store for OpenShift Container Platform, which persists the state of all resource objects.

Back up your cluster’s etcd data regularly and store in a secure location ideally outside the OpenShift Container Platform environment. Do not take an etcd backup before the first certificate rotation completes, which occurs 24 hours after installation, otherwise the backup will contain expired certificates. It is also recommended to take etcd backups during non-peak usage hours because the etcd snapshot has a high I/O cost.

Be sure to take an etcd backup after you upgrade your cluster. This is important because when you restore your cluster, you must use an etcd backup that was taken from the same z-stream release. For example, an OpenShift Container Platform 4.y.z cluster must use an etcd backup that was taken from 4.y.z.


### Backing up etcd data

#### Prerequisites

* You have access to the cluster as a user with the cluster-admin role.
* You have checked whether the cluster-wide proxy is enabled.

#### Procedure

1. Start a debug session for a control plane node:

```
oc debug node/<node_name>
```

2. Change your root directory to /host:

```
chroot /host
```

3. If the cluster-wide proxy is enabled, be sure that you have exported the NO_PROXY, HTTP_PROXY, and HTTPS_PROXY environment variables. (optional)


4. Run the cluster-backup.sh script and pass in the location to save the backup to.


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

#### automated steps to run and copy the file locally 

```
backupdir=/tmp/backup-etcd/

servername=$(oc get nodes |grep -i master|awk '{print $1}'|head -1)

[ -d $backupdir/${servername} ] || mkdir -p $backupdir/${servername}

execout=$(oc debug -t node/$servername -- chroot /host bash -c '/usr/local/bin/cluster-backup.sh /home/core/assets/backup') 
# filename=$(echo $execout | awk -F'path":"' '{print $2}' | awk -F'"' '{print $1}')   #<--- not working
sleep 20

oc debug -t node/$servername -- chroot /host bash -c 'chown core:core /home/core/assets/backup/*.db'

scp -rp core@$servername:${filename} $backupdir/${servername}/

```


## Reference 

* [ETCD backup and restore](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/backup_and_restore/control-plane-backup-and-restore#backup-etcd)