## Backup Hub Clusters with Red Hat Advanced Cluster Management for Kubernetes

### Redhat ACM introduction

Red Hat Advanced Cluster Management for Kubernetes (RHACM) defines two main types of clusters: hub clusters and managed clusters. 

* The hub cluster is the main cluster with RHACM installed on it. You can create, manage, and monitor other Kubernetes clusters with the hub cluster.
* The managed clusters are Kubernetes clusters that are managed by the hub cluster. You can create some clusters by using the RHACM hub cluster, and you can also import existing clusters to be managed by the hub cluster.



### Prerequisites

MultiClusterHub resource is created and displays the status of Running; the MultiClusterHub resource is automatically created when you install the RHACM Operator

The cluster backup and restore operator chart is not installed automatically. Enable the cluster-backup operator on the hub cluster. Edit the MultiClusterHub resource and set the cluster-backup to true. This installs the OADP operator in the same namespace with the backup chart. 


### How it works

The cluster backup and restore operator runs on the hub cluster and depends on the OADP Operator to create a connection to a backup storage location on the hub cluster. The OADP Operator also installs Velero, which is the component used to backup and restore user created hub resources.

The cluster backup and restore operator is installed using the cluster-backup-chart file. The cluster backup and restore operator chart is not installed automatically. Starting with RHACM version 2.5, the cluster backup and restore operator chart is installed by setting the cluster-backup option to true on the MultiClusterHub resource.

The cluster backup and restore operator chart automatically installs the OADP Operator in the same namespace with the backup chart. If you have previously installed and used the OADP Operator on your hub cluster, you should uninstall the version since the backup chart works now with the operator that is installed in the chart namespace. This should not affect your old backups and previous work. Just use the same storage location for the DataProtectionApplication resource, which is owned by the OADP Operator and installed with the backup chart; you should have access to the same backup data as the previous operator. The only difference is that Velero backup resources are now loaded in the new OADP Operator namespace on your hub cluster.


### Implementation 



1) You need to be logged in with a user who has cluster-admin privileges:


```
[root@ncputility ~ pancwl_rc]$ source /root/panhubrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 103 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "panclypcwl01".
[root@ncputility ~ panhub_rc]$

```


2) Add a new annotation to the `multiclusterhub` CR and enable `cluster-backup`for triggering to deploy the OADP

> Active hub

```
[root@ncputility ~ panhub_rc]$ oc edit multiclusterhubs.operator.open-cluster-management.io -n open-cluster-management multiclusterhub
multiclusterhub.operator.open-cluster-management.io/multiclusterhub edited
[root@ncputility ~ panhub_rc]$ 
```

2.1) sample syntax are attached here

```
oc edit multiclusterhubs.operator.open-cluster-management.io -n open-cluster-management multiclusterhub

apiVersion: operator.open-cluster-management.io/v1
kind: MultiClusterHub
metadata:
  annotations:
    installer.open-cluster-management.io/oadp-subscription-spec: '{"source": "cs-redhat-operator-index-acm-oadp-1-4-0"}'

cluster-backup
enabled: true
```

> On the Hub cluster, the value of source has to be the name of the catalogsource of the Infra manager node's Quay that is pointing to the organization where the operators of 24.7 were mirrored.

3) Create BucketClass

> passive cluster or CWL cluster. 
```
[root@ncputility ~ pancwl_rc]$ cat bucketclass-noobaa-default-backing-store.yaml
apiVersion: noobaa.io/v1alpha1
kind: BucketClass
metadata:
  name: bucketclass-noobaa-default-backing-store
  namespace: openshift-storage
spec:
  placementPolicy:
    tiers:
    - backingStores:
      - noobaa-default-backing-store
      placement: Spread
[root@ncputility ~ pancwl_rc]$


```
> oc apply -f bucketclass-noobaa-default-backing-store.yaml

4) Create Object bucket

> passive cluster or CWL cluster. 

```
[root@ncputility ~ pancwl_rc]$ cat ObjectBucketClaim.yaml
apiVersion: objectbucket.io/v1alpha1
kind: ObjectBucketClaim
metadata:
  name: acm-backups
  namespace: openshift-storage
spec:
  generateBucketName: acm-backups
  storageClassName: openshift-storage.noobaa.io
  additionalConfig:
      bucketclass: bucketclass-noobaa-default-backing-store
[root@ncputility ~ pancwl_rc]$

# spec refers to the BucketClass created earlier.

```

> oc apply -f ObjectBucketClaim.yaml

a) Use the following commands to gather values for later steps

```
BUCKET_NAME=$(oc get -n openshift-storage configmap acm-backups -o jsonpath='{.data.BUCKET_NAME}')
ACCESS_KEY_ID=$(oc get -n openshift-storage secret acm-backups -o jsonpath='{.data.AWS_ACCESS_KEY_ID}' | base64 -d)
SECRET_ACCESS_KEY=$(oc get -n openshift-storage secret acm-backups -o jsonpath='{.data.AWS_SECRET_ACCESS_KEY}' | base64 -d)

echo "BUCKET_NAME=$BUCKET_NAME"
echo "ACCESS_KEY_ID=$ACCESS_KEY_ID"
echo "SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY"

```
5) Create secret.txt file

```
[root@ncputility ~ pancwl_rc]$ cat secret.txt
[default]
aws_access_key_id = hOJGxRsZDKOaBgRRXqf5
aws_secret_access_key = KuOAAqyTDM434if+EM16Ajp7Le66MN1+KirdzXKt
[root@ncputility ~ pancwl_rc]$

#aws_access_key_id and aws_secret_access_key provide access to Object bucket.
```

6) Apply the following command on secret.txt

```
base64 -w 0 secret.txt
```

Expected output: 

```
W2RlZmF1bHRdCmF3c19hY2Nlc3Nfa2V5X2lkID0gWkQ3YnJrRWRUa0lheTBwVUphVlMKYXdzX3NlY3JldF9hY2Nlc3Nfa2V5ID0gZmlvZ0JYek40elpES1lBNVR6cHcrWUhTM3FEeWYwa0tJWlNyekt0agoK
```


7) Create secret.yaml file

> both clusters: 

```
[root@ncputility ~ pancwl_rc]$ cat secret.yaml
apiVersion: v1
data:
  cloud: W2RlZmF1bHRdCmF3c19hY2Nlc3Nfa2V5X2lkID0gaE9KR3hSc1pES09hQmdSUlhxZjUKYXdzX3NlY3JldF9hY2Nlc3Nfa2V5ID0gS3VPQUFxeVRETTQzNGlmK0VNMTZBanA3TGU2Nk1OMStLaXJkelhLdAo=
kind: Secret
metadata:
  name: cloud-credentials
  namespace: open-cluster-management-backup
type: Opaque
[root@ncputility ~ pancwl_rc]$


#The value of cloud under data block is the base64 encoded output of the secret.txt.
```


8) Apply secret.yaml 

> 

```
[root@dom14npv101-infra-manager ~ hubrc]# oc apply -f secret.yaml
secret/cloud-credentials created
[root@dom14npv101-infra-manager ~ hubrc]#
```

9) Create DataProtectionApplication custom resource

9.1) s3 interface can be accessed on the standby cluster via s3Url. The value of s3Url can be checked with the following command:

> oc get routes -n openshift-storage | grep s3-openshift-storage | awk '{print $2}'

9.2) caCert is a root certificate in base64 format of the standby hub cluster's default ingress controller which is used for exposing s3 service. The value of caCert can be checked with the following command:

> oc get secrets -n openshift-ingress-operator router-ca -o jsonpath="{.data['tls\.crt']}"

9.3) The value of credential is the name of the secret which was created in secret.yaml. The value of key is the name of the value created insecret.yaml under data block.

```
[root@ncputility ~ pancwl_rc]$ cat DataProtectionApplication.yaml
kind: DataProtectionApplication
apiVersion: oadp.openshift.io/v1alpha1
metadata:
  name: velero-acm-backup
  namespace: open-cluster-management-backup
spec:
  backupLocations:
    - velero:
        config:
          profile: default
          region: none
          s3ForcePathStyle: "true"
          s3Url: "https://s3-openshift-storage.apps.hnevocphub01.mnc002.mcc708"
        default: true
        provider: aws
        objectStorage:
          bucket: acm-backups-3885ebaa-8c8b-4985-b9c7-0c25d631de14
          prefix: velero
          caCert: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURERENDQWZTZ0F3SUJBZ0lCQVRBTkJna3Foa2lHOXcwQkFRc0ZBREFtTVNRd0lnWURWUVFEREJ0cGJtZHkKWlhOekxXOXdaWEpoZEc5eVFERTNORFV4TlRNM09UZ3dIaGNOTWpVd05ESXdNVEkxTmpNM1doY05NamN3TkRJdwpNVEkxTmpNNFdqQW1NU1F3SWdZRFZRUUREQnRwYm1keVpYTnpMVzl3WlhKaGRHOXlRREUzTkRVeE5UTTNPVGd3CmdnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUUM4aXhWMDZnM0ozZ01lUE04d0JEVTEKRFdMNWhyVW9DeXh5SThkTFNob2trSDNtdTF1RFNCeEJ2blBQYnZhRUs1aFR1RFhjQ3dSaUVNYmZPcFFjUnZzdApQT2dVSU05T3RhY3lwWVZTeGVhSUNQZnNpMlBzd0VaNElWNWMwZEM1SVVSc2hTTTFXaksxckpvanZYQmE3c0c3CjhpQXRCMnJ0K1FwUkhJRzVSYVpnZVdXQVhrMXVPdWlTazBSLzJ3ajZsbDJmZ01NYklOSGluNXdseU1YQldjOHYKaHJTc3VjR2wrL2pXRVl2QWdXKzFrRW5YRDgvclpqUTN6bExVVTRpdzNvNlBMRFlrKzhjYm5DQnNMQjh2RWlqWQppbFRzQ1N3TjdwUk5CVGNqcWxLYVpqWVZ2Mk9QYi80WjF4TG1aekFxWGRhc2pSRW5XNXcyZGtrZy9RNlgxWmZGCkFnTUJBQUdqUlRCRE1BNEdBMVVkRHdFQi93UUVBd0lDcERBU0JnTlZIUk1CQWY4RUNEQUdBUUgvQWdFQU1CMEcKQTFVZERnUVdCQlRsdFFLZ2NjYjZ4bE5BZUt5SFpjY1BZT1A1b0RBTkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQQpnZDYyWVJkRHhNTm5HcCtDWStRaXBZRlMxMkNRMUVwVXcwMEVIUno0b2k0UG5PQzcrazlGbHVZeW9vWWNZa1QyCkNGTGp4K3hOODE2bkFVRWFMQ25Ia2NjK2JCSlhuNmU0LzFqWUZGdFFjRnhJeEZVdXByb3dNY21ZeGxBbHlBQ1oKZU5ac1V1Tk4xWVh1aDl2Z3MrRVE2a1VNSjFYSVNPeVp3RDNIbVZSaW16RHN6MUo4MDRLSlhqVnRURlNEbXR1WQpBbGxLWnF2czdqWGJWTUlxY1VtUmFQclluRm8xRDBXcFFGMnFLRGtUL1RDdnFuS3ROR2x5dHVCZmp1YittL0U0Ck1yOExTdXFjTGlhcGhFQS9BM3pwNHNaVWxVbmVCaksrRnkzTkwwdnprcjZxZGVjbG1YSHU5bzdtMnV4UlBKR2UKTm9vb240cmdYU25SSnB5VForcEhyUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K"
        credential:
          key: cloud
          name: cloud-credentials
  configuration:
    nodeAgent:
      enable: true
      uploaderType: restic
    velero:
      featureFlags:
        - EnableCSI
      defaultPlugins:
        - openshift
        - aws
        - csi
[root@ncputility ~ pancwl_rc]$


#bucket is the value checked earlier with BUCKET_NAME command.
```

>  ```[root@dom14npv101-infra-manager ~ hubrc]# oc apply -f DataProtectionApplication.yaml
dataprotectionapplication.oadp.openshift.io/velero-acm-backup created
[root@dom14npv101-infra-manager ~ hubrc]#```


10) validate that resouce creation is completed successfully. 


```
[root@dom14npv101-infra-manager ~ hubrc]# oc get backupstoragelocations.velero.io -n open-cluster-management-backup
NAME                  PHASE       LAST VALIDATED   AGE   DEFAULT
velero-acm-backup-1   Available   22s              33s   true
[root@dom14npv101-infra-manager ~ hubrc]#
```

11) Check the resources that are application projects from GitOps

> hub cluster: 
```
[root@dom14npv101-infra-manager ~ hubrc]# oc get appprojects.argoproj.io -n openshift-gitops | grep -v default
NAME                  AGE
site-config-project   59d
site-policy-project   59d
```

12) Add label velero.io/exclude-from-backup: "true" manually on both Hub clusters
```
[root@dom14npv101-infra-manager ~ hubrc]# oc get appprojects.argoproj.io -n openshift-gitops -l velero.io/exclude-from-backup
NAME                  AGE
site-config-project   59d
site-policy-project   59d
```
13) Add label velero.io/exclude-from-backup: "true" manually on both Hub clusters

```
[root@dom14npv101-infra-manager ~ hubrc]# oc get applications.argoproj.io -n openshift-gitops -l velero.io/exclude-from-backup
NAME                        SYNC STATUS   HEALTH STATUS
ncpvnpvlab1-site-configs    Synced        Healthy
ncpvnpvlab1-site-policies   Synced        Healthy
ncpvnpvmgt-site-configs     Synced        Healthy
ncpvnpvmgt-site-policies    Synced        Healthy
[root@dom14npv101-infra-manager ~ hubrc]#
``` 

14) A backup is made everyday at 10 PM.

```
[root@dom14npv101-infra-manager ~ hubrc]# cat > backup.yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: BackupSchedule
metadata:
  name: schedule-acm
  namespace: open-cluster-management-backup
spec:
  veleroSchedule: 0 22 * * *
  veleroTtl: 120h
^C
[root@dom14npv101-infra-manager ~ hubrc]# date
Thu May  1 06:04:49 PM UTC 2025
[root@dom14npv101-infra-manager ~ hubrc]# vi backup.yaml
[root@dom14npv101-infra-manager ~ hubrc]# oc apply  -f  backup.yaml
backupschedule.cluster.open-cluster-management.io/schedule-acm created
[root@dom14npv101-infra-manager ~ hubrc]# 

```

### Status of backup job here:


1) checking the status of the backup 

```
[root@dom14npv101-infra-manager ~ hubrc]# oc get backupstoragelocations.velero.io -A
NAMESPACE                        NAME                  PHASE       LAST VALIDATED   AGE     DEFAULT
open-cluster-management-backup   velero-acm-backup-1   Available   4s               5m15s   true
[root@dom14npv101-infra-manager ~ hubrc]# 
```

2) describe the status of the output job 
```
[root@dom14npv101-infra-manager ~ hubrc]#  oc describe backupstoragelocations.velero.io velero-acm-backup-1 -n open-cluster-management-backup
Name:         velero-acm-backup-1
Namespace:    open-cluster-management-backup
Labels:       app.kubernetes.io/component=bsl
              app.kubernetes.io/instance=velero-acm-backup-1
              app.kubernetes.io/managed-by=oadp-operator
              app.kubernetes.io/name=oadp-operator-velero
              openshift.io/oadp=True
              openshift.io/oadp-registry=True
Annotations:  <none>
API Version:  velero.io/v1
Kind:         BackupStorageLocation
Metadata:
  Creation Timestamp:  2025-05-01T18:02:31Z
  Generation:          13
  Owner References:
    API Version:           oadp.openshift.io/v1alpha1
    Block Owner Deletion:  true
    Controller:            true
    Kind:                  DataProtectionApplication
    Name:                  velero-acm-backup
    UID:                   89734e12-0144-4376-954d-cb13cde17515
  Resource Version:        142419914
  UID:                     52b6b341-5e36-4e02-bc98-15622be65673
Spec:
  Config:
    Checksum Algorithm:
    Profile:             default
    Region:              none
    s3ForcePathStyle:    true
    s3Url:               https://s3-openshift-storage.apps.ncpvnpvmgt.pnwlab.nsn-rdnet.net
  Credential:
    Key:    cloud
    Name:   cloud-credentials
  Default:  true
  Object Storage:
    Bucket:   acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63
    Ca Cert:  LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURERENDQWZTZ0F3SUJBZ0lCQVRBTkJna3Foa2lHOXcwQkFRc0ZBREFtTVNRd0lnWURWUVFEREJ0cGJtZHkKWlhOekxXOXdaWEpoZEc5eVFERTNOREV4TXpJek16RXdIaGNOTWpVd016QTBNak0xTWpF        d1doY05NamN3TXpBMApNak0xTWpFeFdqQW1NU1F3SWdZRFZRUUREQnRwYm1keVpYTnpMVzl3WlhKaGRHOXlRREUzTkRFeE16SXpNekV3CmdnRWlNQTBHQ1NxR1NJYjNEUUVCQVFVQUE0SUJEd0F3Z2dFS0FvSUJBUURLOUhrUkd4VWNPRnZjcHVZc1dLdWQKd2ltMFBWc3B3VU        1LNXgyejhBQWJ1eGhuOTRFWThWbk9tSkJUVkhqRnIvbmI0SjRzYldzN3JBbXZINWpjbTdzbApMYW1wWU1uUWlSamtrdE5FSVV3Rm9LVm9VU3ZRSWtiTHJlZk1hcjJYSENOOEU0dHVHeXA3U1c1YjBMRjc4cUY5CktIY0ttMXBDVi9NR3lyU1RtMkx0SmtBcnM5d0lsL0ZPYmox        UEcvUmsvQThtRHZhalBmSUVGbU8yMHduWEQ5bWcKZDVIVk1ZVzkyWWRWVDZPR0FWMEZUNCtJNzNibEdyK3pqQUJzMklxTnUzQ3h0cHlucXMvVVV6RGFodGRvc2ZxSgpWeHhaTUFaZlRENTk0UUtzMFZhamR2aTU1Z1pPejVBQXRLSG96Rm85TWk5dklXblpwR3Z0T2xINnIyVE        ZmSytmCkFnTUJBQUdqUlRCRE1BNEdBMVVkRHdFQi93UUVBd0lDcERBU0JnTlZIUk1CQWY4RUNEQUdBUUgvQWdFQU1CMEcKQTFVZERnUVdCQlRJNVRqeVp2aUJ1NE0wNzd6Mk9PY0lDRmkwMURBTkJna3Foa2lHOXcwQkFRc0ZBQU9DQVFFQQpuNG96eWZha0sySUFqb3dFSlZE        bFNMMlp4YVJuWmJFcjVLanhJbjhiQ0tjaUdBK0h2UURuY0UzK1BzSTJDZGxpCjhXQlR4ZnJ3aFoxTVZ2YjVySmlsTXpZUklQamJaanUrbitaNlB0SGJYMEZDb2Q0elpaYkZBOFQvNlZXUkJSSmUKL3VMaXU3VVRENjJQRDgydVlNSmJFTDNTa1V6b1U5T2NXMSt1S1R3UG56NG        VFblVvNzVnbVlUWnBybkhKSEttNAowUVljTlF6RndHR3JnQnNuTy8wRW94Z2Roa09keENlWFBqRUpURnZXRTdpRjhYWTlKQVZKMVpCcStuZUNoMmRCCkowRGRkaGZjMDhtUnpHbStkVXRyeCtZMnRoSXBxWVUreTN1WDZaM09TcDVNeFIvQzMvelRGR2pqK3pKUmNIOTIKUmtH        c2V5bGNCYXpYbmVvWXgzdEVxUT09Ci0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0K
    Prefix:   velero
  Provider:   aws
Status:
  Last Synced Time:      2025-05-01T18:07:42Z
  Last Validation Time:  2025-05-01T18:07:42Z
  Phase:                 Available
Events:
  Type    Reason                           Age    From            Message
  ----    ------                           ----   ----            -------
  Normal  BackupStorageLocationReconciled  5m33s  DPA-controller  performed created on backupstoragelocation open-cluster-management-backup/velero-acm-backup-1

```

### Access the backup jobs

1) status of open-cluster-manager pods here

```
[root@dom14npv101-infra-manager ~ hubrc]# oc get pods -n  open-cluster-management-backup
NAME                                                 READY   STATUS    RESTARTS   AGE
cluster-backup-chart-clusterbackup-698656f7f-cqxxj   1/1     Running   0          24d
cluster-backup-chart-clusterbackup-698656f7f-dvdz8   1/1     Running   0          24d
node-agent-brq4q                                     1/1     Running   0          6m6s
node-agent-j9xm8                                     1/1     Running   0          6m6s
node-agent-mlrwk                                     1/1     Running   0          6m6s
node-agent-nkb7v                                     1/1     Running   0          6m6s
node-agent-sgqxw                                     1/1     Running   0          6m6s
openshift-adp-controller-manager-74f799649f-v2slw    1/1     Running   0          24d
velero-549fbfb95d-s966g                              1/1     Running   0          6m6s
[root@dom14npv101-infra-manager ~ hubrc]# 
```

2) status of job from velero binary
```
[root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup-location get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                  PROVIDER   BUCKET/PREFIX                                             PHASE       LAST VALIDATED                  ACCESS MODE   DEFAULT
velero-acm-backup-1   aws        acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero   Available   2025-05-01 18:08:42 +0000 UTC   ReadWrite     true
[root@dom14npv101-infra-manager ~ hubrc]#
```

3) Look at the final status of the backup jobs

```
 [root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                                            STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION      SELECTOR
acm-credentials-schedule-20250501180616         Completed   0        0          2025-05-01 18:06:17 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-managed-clusters-schedule-20250501180616    Completed   0        0          2025-05-01 18:06:18 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-resources-generic-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:20 +0000 UTC   4d        velero-acm-backup-1   cluster.open-cluster-management.io/backup
acm-resources-schedule-20250501180616           Completed   0        0          2025-05-01 18:06:29 +0000 UTC   4d        velero-acm-backup-1   !cluster.open-cluster-management.io/backup,!policy.open-cluste        r-management.io/root-policy
acm-validation-policy-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:30 +0000 UTC   1d        velero-acm-backup-1   <none>
[root@dom14npv101-infra-manager ~ hubrc]# date
Thu May  1 06:09:39 PM UTC 2025
[root@dom14npv101-infra-manager ~ hubrc]# 
```