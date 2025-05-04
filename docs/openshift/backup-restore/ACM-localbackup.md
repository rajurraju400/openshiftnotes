
both cluster

active hub:

[root@ncputility ~ panhub_rc]$ source /root/panhubrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 108 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
[root@ncputility ~ panhub_rc]$ oc edit multiclusterhubs.operator.open-cluster-management.io -n open-cluster-management multiclusterhub
multiclusterhub.operator.open-cluster-management.io/multiclusterhub edited
[root@ncputility ~ panhub_rc]$ oc edit multiclusterhubs.operator.open-cluster-management.io -n open-cluster-management multiclusterhub
Edit cancelled, no changes made.
[root@ncputility ~ panhub_rc]$


Active hub: 


[root@dom14npv101-infra-manager ~ hubrc]# cd /root/raj/amc-backup
[root@dom14npv101-infra-manager ~ hubrc]# ll
total 24
drwxr-xr-x. 7 root root 4096 May  1 17:46 ../
-rw-r--r--. 1 root root  257 May  1 17:47 bucketclass-noobaa-default-backing-store.yaml
-rw-r--r--. 1 root root  290 May  1 17:48 ObjectBucketClaim.yaml
-rw-r--r--. 1 root root  116 May  1 17:50 secret.txt
-rw-r--r--. 1 root root  293 May  1 17:52 secret.yaml
-rw-r--r--. 1 root root 2329 May  1 17:58 DataProtectionApplication.yaml
drwxr-xr-x. 2 root root  164 May  1 17:58 ./
[root@dom14npv101-infra-manager ~ hubrc]# oc apply -f secret.yaml
secret/cloud-credentials created
[root@dom14npv101-infra-manager ~ hubrc]# oc apply -f DataProtectionApplication.yaml
dataprotectionapplication.oadp.openshift.io/velero-acm-backup created
[root@dom14npv101-infra-manager ~ hubrc]# oc get backupstoragelocations.velero.io
No resources found in ncd-cbur namespace.
[root@dom14npv101-infra-manager ~ hubrc]# oc get backupstoragelocations.velero.io -n open-cluster-management-backup
NAME                  PHASE       LAST VALIDATED   AGE   DEFAULT
velero-acm-backup-1   Available   22s              33s   true
[root@dom14npv101-infra-manager ~ hubrc]# oc get appprojects.argoproj.io -n openshift-gitops | grep -v default
NAME                  AGE
site-config-project   59d
site-policy-project   59d
[root@dom14npv101-infra-manager ~ hubrc]# oc get appprojects.argoproj.io -n openshift-gitops -l velero.io/exclude-from-backup
NAME                  AGE
site-config-project   59d
site-policy-project   59d
[root@dom14npv101-infra-manager ~ hubrc]# oc get applications.argoproj.io -n openshift-gitops -l velero.io/exclude-from-backup
NAME                        SYNC STATUS   HEALTH STATUS
ncpvnpvlab1-site-configs    Synced        Healthy
ncpvnpvlab1-site-policies   Synced        Healthy
ncpvnpvmgt-site-configs     Synced        Healthy
ncpvnpvmgt-site-policies    Synced        Healthy
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
[root@dom14npv101-infra-manager ~ hubrc]# oc get backupstoragelocations.velero.io -A
NAMESPACE                        NAME                  PHASE       LAST VALIDATED   AGE     DEFAULT
open-cluster-management-backup   velero-acm-backup-1   Available   4s               5m15s   true
[root@dom14npv101-infra-manager ~ hubrc]# oc describe backupstoragelocations.velero.io velero-acm-backup-1 -n open-cluster-management-backup
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
[root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup-location get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                  PROVIDER   BUCKET/PREFIX                                             PHASE       LAST VALIDATED                  ACCESS MODE   DEFAULT
velero-acm-backup-1   aws        acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero   Available   2025-05-01 18:08:42 +0000 UTC   ReadWrite     true
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