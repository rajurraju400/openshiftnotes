
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


Passive hub: 


