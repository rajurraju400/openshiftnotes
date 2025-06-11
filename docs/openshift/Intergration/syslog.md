# Cluster logging operator


## Configuring logging operator 

> Prerequisites
Cluster Logging Operator was deployed via „common” `PolicyGenTemplate` and it has to be configured.
For more details on cluster logging, see About Logging in document Logging, available in OpenShift Container Platform Product Documentation.
```
The YAML files can be created directly on the cluster or via GitOps pipeline. In the first option, always apply the files, in the second option, always trigger the `ClusterGroupUpgrade` object with the correct policy name to apply the files.
However, it is recommended to use the GitOps based option.
```

1) Create the ClusterLogging object
> clusterloggingobject_loki.yaml


```
[root@ncputility ~ hn_cwl_rc]$ cat  clusterloggingobject_loki.yaml
apiVersion: logging.openshift.io/v1
kind: ClusterLogging
metadata:
  name: instance
  namespace: openshift-logging
spec:
  managementState: Managed
  collection:
    type: vector
    tolerations:
    - key: node.ocs.openshift.io/storage
      operator: Equal
      value: 'true'
      effect: NoSchedule
  visualization:
    type: ocp-console
    ocpConsole: null
  logStore:
    type: lokistack
    lokistack:
      name: logging-loki
[root@ncputility ~ hn_cwl_rc]$ oc get ClusterLogging instance  -n openshift-logging
NAME       MANAGEMENT STATE
instance   Managed
[root@ncputility ~ hn_cwl_rc]$

```

2) After the file was applied, the objects are created in the `openshift-logging` namespace:

```
[root@ncputility ~ hn_cwl_rc]$ oc get pods -n openshift-logging -o wide
NAME                                          READY   STATUS    RESTARTS   AGE   IP              NODE                                    NOMINATED NODE   READINESS GATES
cluster-logging-operator-5fd7f999cc-c74nw     1/1     Running   0          10d   172.18.12.35    appworker15.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-2p5hc                               1/1     Running   3          14d   172.16.12.51    appworker12.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-4482t                               1/1     Running   2          14d   172.19.0.22     storage1.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-556t8                               1/1     Running   1          14d   172.19.8.71     appworker8.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-5k4vt                               1/1     Running   1          14d   172.18.16.50    appworker20.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-69f88                               1/1     Running   1          14d   172.16.14.80    appworker13.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-6ccv9                               1/1     Running   1          14d   172.19.16.78    appworker23.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-8nkzz                               1/1     Running   1          14d   172.18.20.105   appworker32.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-8nndr                               1/1     Running   3          14d   172.17.0.41     master2.hnevopcwl01.mnc002.mcc708       <none>           <none>
collector-8wgtd                               1/1     Running   2          14d   172.19.2.3      gateway2.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-985sr                               1/1     Running   2          14d   172.18.6.3      gateway4.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-9n7zn                               1/1     Running   2          14d   172.19.12.61    appworker16.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-9qsmg                               1/1     Running   2          14d   172.16.4.69     appworker5.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-9qv85                               1/1     Running   3          14d   172.16.8.65     master0.hnevopcwl01.mnc002.mcc708       <none>           <none>
collector-9slfx                               1/1     Running   1          14d   172.16.20.63    appworker26.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-bhhmt                               1/1     Running   2          14d   172.17.4.20     storage4.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-c8r5v                               1/1     Running   2          14d   172.18.18.48    appworker28.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-cs4rp                               1/1     Running   3          14d   172.17.18.77    appworker27.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-ggmdf                               1/1     Running   2          14d   172.17.6.80     appworker0.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-gkxmx                               1/1     Running   2          14d   172.17.14.53    appworker22.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-gn7c4                               1/1     Running   3          14d   172.18.22.100   appworker34.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-h5xw6                               1/1     Running   1          14d   172.16.16.75    appworker19.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-hfhf8                               1/1     Running   1          14d   172.16.10.106   appworker2.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-hh4rp                               1/1     Running   1          14d   172.17.22.62    appworker33.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-hmrkh                               1/1     Running   2          14d   172.16.6.67     appworker3.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-hpv64                               1/1     Running   2          14d   172.19.14.44    appworker18.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-jcgs4                               1/1     Running   2          14d   172.17.2.3      gateway1.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-jr7zw                               1/1     Running   1          14d   172.17.20.40    appworker31.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-k7nn9                               1/1     Running   2          14d   172.16.2.25     storage0.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-kwpqh                               1/1     Running   2          14d   172.18.2.18     storage2.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-l2jzn                               1/1     Running   2          14d   172.18.4.88     appworker1.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-lq8hx                               1/1     Running   3          14d   172.16.0.60     master1.hnevopcwl01.mnc002.mcc708       <none>           <none>
collector-lzgrn                               1/1     Running   1          14d   172.18.14.61    appworker17.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-nbs6z                               1/1     Running   2          14d   172.19.4.60     appworker4.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-pr7g7                               1/1     Running   2          14d   172.17.8.50     appworker6.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-pt9hv                               1/1     Running   2          14d   172.19.6.31     storage3.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-stzf4                               1/1     Running   2          14d   172.19.10.109   appworker14.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-szptx                               1/1     Running   2          14d   172.18.8.189    appworker7.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-t9zh7                               1/1     Running   2          14d   172.18.0.3      gateway3.hnevopcwl01.mnc002.mcc708      <none>           <none>
collector-td9sw                               1/1     Running   1          14d   172.16.22.46    appworker25.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-tmzq6                               1/1     Running   1          14d   172.19.20.66    appworker30.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-tvl9n                               1/1     Running   2          14d   172.18.12.45    appworker15.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-vtqc2                               1/1     Running   2          14d   172.17.12.66    appworker11.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-wfv2n                               1/1     Running   1          14d   172.16.18.52    appworker24.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-wgfql                               1/1     Running   1          14d   172.19.18.48    appworker29.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-xdtlz                               1/1     Running   2          14d   172.17.10.65    appworker9.hnevopcwl01.mnc002.mcc708    <none>           <none>
collector-z5r8p                               1/1     Running   2          14d   172.18.10.59    appworker10.hnevopcwl01.mnc002.mcc708   <none>           <none>
collector-z9rpj                               1/1     Running   1          14d   172.17.16.50    appworker21.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-compactor-0                      1/1     Running   0          10d   172.16.22.3     appworker25.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-distributor-78d44b7496-c7kjr     1/1     Running   0          10d   172.19.16.40    appworker23.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-distributor-78d44b7496-nc9zt     1/1     Running   0          10d   172.16.10.31    appworker2.hnevopcwl01.mnc002.mcc708    <none>           <none>
logging-loki-gateway-6558fdbc65-lmqzq         2/2     Running   0          10d   172.16.10.46    appworker2.hnevopcwl01.mnc002.mcc708    <none>           <none>
logging-loki-gateway-6558fdbc65-sg45d         2/2     Running   0          10d   172.18.20.18    appworker32.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-index-gateway-0                  1/1     Running   0          10d   172.18.20.48    appworker32.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-index-gateway-1                  1/1     Running   0          10d   172.16.20.31    appworker26.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-ingester-0                       1/1     Running   0          10d   172.19.16.34    appworker23.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-ingester-1                       1/1     Running   0          10d   172.18.16.58    appworker20.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-querier-79b54c8cf5-tzxst         1/1     Running   0          10d   172.16.12.4     appworker12.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-querier-79b54c8cf5-wqpgm         1/1     Running   0          10d   172.16.22.41    appworker25.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-query-frontend-8d8785885-r7kfr   1/1     Running   0          10d   172.16.22.42    appworker25.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-loki-query-frontend-8d8785885-rblkm   1/1     Running   0          10d   172.18.20.52    appworker32.hnevopcwl01.mnc002.mcc708   <none>           <none>
logging-view-plugin-566757957-nlp2n           1/1     Running   0          10d   172.19.12.23    appworker16.hnevopcwl01.mnc002.mcc708   <none>           <none>
[root@ncputility ~ hn_cwl_rc]$

```

3) Create the `ClusterLogForwarder` object to all log types to make them locally visible

> CWL cluster can support either local forwarding or external forwarding not both. 

```
[root@ncputility ~ hn_cwl_rc]$ oc apply -f local_clusterlogforwarder.yaml
applied.
[root@ncputility ~ hn_cwl_rc]$ cat  local_clusterlogforwarder.yaml
apiVersion: logging.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: instance
  namespace: openshift-logging
spec:
  pipelines:
  - name: all-to-default
    inputRefs:
    - infrastructure
    - application
    - audit
    outputRefs:
    - default
[root@ncputility ~ hn_cwl_rc]$

```

## Sending logs to external syslog server

> For a detailed description, see Forwarding logs using the syslog protocol in document Logging, available in OpenShift Container Platform Product Documentation.

## Steps to be followed

1) To send logs to the external source, ClusterLogForwarder object has to be modified, as shown in the following example.

> All logs and external syslog server can be found at Kibana with the above options.
url: udp://<ip of the syslog server>:514 should be updated based on your infra.

```
[root@ncputility ~ hn_cwl_rc]$ cat  external-syslog_clusterlogforwarder.yaml
apiVersion: logging.openshift.io/v1
kind: ClusterLogForwarder
metadata:
  name: instance
  namespace: openshift-logging
spec:
  outputs:
  - name: infra-node
    syslog:
      appName: myapp
      facility: user
      msgID: mymsg
      procID: myproc
      rfc: RFC5424
      severity: informational
    type: syslog
    url: udp://10.89.27.71:13000
  pipelines:
  - inputRefs:
    - infrastructure
    - application
    - audit
    name: all-to-default
    outputRefs:
    - default
  - inputRefs:
    - infrastructure
    - application
    - audit
    name: infra-node-rsyslog
    outputRefs:
    - infra-node
[root@ncputility ~ hn_cwl_rc]$ oc apply  -f external-syslog_clusterlogforwarder.yaml
clusterlogforwarder.logging.openshift.io/instance created
[root@ncputility ~ hn_cwl_rc]$

```

> Just for testing, i applied it manually. but it should done via PGT process. 



## Redhat Cluster logging operator plugin enable from UI.

1) Go to Operators > Red Hat Openshift Logging to view the collected logs in the webUI

>In the Details page, click "Disabled" for the "Console plugin" option
In the "Console plugin" enablement dialog, select "Enable"
Click on "Save"
Verify that the "Console plugin" option now shows "Enabled"

2) The web console displays a pop-up window when changes have been applied. The window prompts to reload the web console. Refresh the browser when you see the pop-up window to apply the changes. After the browser is refreshed to apply the changes, the logs can be check under Objects > Logs.




## PGT process 

1) make sure site-specific.yaml policy file has been called for external log forwarding. 

```
[root@ncputility ~ hn_cwl_rc]$ cat  site-hnevopcwl01-247mp1-config.yaml |tail -10
   # Cluster Logging Operator
     - fileName: clusterlogging/clusterloggingobject_loki.yaml
       policyName: config-policies-2nd-wave
         #Uncommnent the necessary method of collecting logs before apply this PolicyGenTemplate
         #External syslog collection
     - fileName: clusterlogging/external-syslog_clusterlogforwarder.yaml
       policyName: config-policies-2nd-wave
         #Local log collection only
    # - fileName: clusterlogging/local_clusterlogforwarder.yaml
    #   policyName: config-policies-2nd-wave
[root@ncputility ~ hn_cwl_rc]$

```

2) update it on the git and commit it.

```
[root@ncputility ~ hn_cwl_rc]$ git add  .
[root@ncputility ~ hn_cwl_rc]$ git commit -m "external-syslog_clusterlogforwarder"
[main 65680b3] external-syslog_clusterlogforwarder
 Committer: root <root@ncputility.panclyphub01.mnc020.mcc714>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 4 files changed, 39 insertions(+), 3 deletions(-)
 create mode 100644 CWL_CLUSTER/site-policies/sites/hub/source-crs/metallb/ncp-metallb-oam-pa-pa-bgp-peer-loopback.yaml
 create mode 100644 CWL_CLUSTER/site-policies/sites/hub/source-crs/metallb/ncp-metallb-static-routes-bgpadvertisement-loopback.yaml
[root@ncputility ~ hn_cwl_rc]$ git push
Username for 'https://gitlab.apps.panclyphub01.mnc020.mcc714': ncpadmin
Password for 'https://ncpadmin@gitlab.apps.panclyphub01.mnc020.mcc714':
Enumerating objects: 23, done.
Counting objects: 100% (23/23), done.
Delta compression using up to 128 threads
Compressing objects: 100% (13/13), done.
Writing objects: 100% (13/13), 1.70 KiB | 1.70 MiB/s, done.
Total 13 (delta 8), reused 0 (delta 0), pack-reused 0
To https://gitlab.apps.panclyphub01.mnc020.mcc714/ncpadmin/hnevopcwl01.git
   abbe4fa..65680b3  main -> main
[root@ncputility ~ hn_cwl_rc]$

```

3) Access the argocd console and sync it. 


4) apply the CGU on the hub cluster and wait for it complete. 