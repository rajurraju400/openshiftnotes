# Removing the kubeadmin user 

### The kubeadmin user 


OpenShift Container Platform creates a cluster administrator, kubeadmin, after the installation process completes.

This user has the cluster-admin role automatically applied and is treated as the root user for the cluster. The password is dynamically generated and unique to your OpenShift Container Platform environment. After installation completes the password is provided in the installation program’s output. For example:



```

INFO Install complete!
INFO Run 'export KUBECONFIG=<your working directory>/auth/kubeconfig' to manage the cluster with 'oc', the OpenShift CLI.
INFO The cluster is ready when 'oc login -u kubeadmin -p <provided>' succeeds (wait a few minutes).
INFO Access the OpenShift web-console here: https://console-openshift-console.apps.demo1.openshift4-beta-abcorp.com
INFO Login to the console with user: kubeadmin, password: <provided>
```


### Removing the kubeadmin user 


1. After you define an identity provider and create a new cluster-admin user, you can remove the kubeadmin to improve cluster security.

## Warning
`If you follow this procedure before another user is a cluster-admin, then OpenShift Container Platform must be reinstalled. It is not possible to undo this command.`


#### Prerequisites

* You must have configured at least one identity provider.
* You must have added the cluster-admin role to a user.
* You must be logged in as an administrator.


#### Procedure


1. Remove the kubeadmin secrets:


```
oc delete secrets kubeadmin -n kube-system
```


#### References

* [Remove kubeadmin id](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/authentication_and_authorization/removing-kubeadmin#understanding-kubeadmin_removing-kubeadmin)
