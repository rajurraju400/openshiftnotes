# OCP User management using htpassword


## Configure HTPASSWD as an identity provider for OCP
 

## Add, update, remove users for OCP using htpasswd as indentity provider. 

#### Procedure to `Add` an additional users

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



#### Procedure to `update` the password of an existing users


1) Retrieve the htpasswd file from the htpass-secret Secret object and save the file to your file system:

```
[root@dom14npv101-infra-manager ~ hub]# oc get secret htpass-secret -ojsonpath={.data.htpasswd} -n openshift-config | base64 --decode > users.htpasswd
[root@dom14npv101-infra-manager ~ hub]# cat users.htpasswd
ncpadmin:$2y$05$DYlpXiwFzfyRioO4hRNq1.ZdFLO3yMz3Pl3gs7.yUpEUKeOGoHX9K
nokia:$2y$05$SLpgZb3AE.fE7WQEGIMOXesoZdY9pV9OHVpXb5CuITdZO5RVId8Ye
[root@dom14npv101-infra-manager ~ hub]# 
```

2) update the users password from the users.htpasswd file.

```
[root@dom14npv101-infra-manager ~ hub]# htpasswd -bB users.htpasswd nokia nokia@1234
Updating password for user nokia
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
[root@dom14npv101-infra-manager ~ hub]# oc get pods -n openshift-authentication -o wide -w
NAME                             READY   STATUS    RESTARTS   AGE     IP             NODE                                                       NOMINATED NODE   READINESS GATES
oauth-openshift-f446bd5b-58cps   1/1     Running   0          6m48s   172.20.2.190   ncpvnpvhub-hubmaster-101.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-k8dqx   1/1     Running   0          5m53s   172.21.0.241   ncpvnpvhub-hubmaster-103.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-v4n6m   1/1     Running   0          6m21s   172.20.0.134   ncpvnpvhub-hubmaster-102.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-v4n6m   1/1     Terminating   0          6m24s   172.20.0.134   ncpvnpvhub-hubmaster-102.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-6497ccb4f5-d5wxd   0/1     Pending       0          0s      <none>         <none>                                                     <none>           <none>
oauth-openshift-6497ccb4f5-d5wxd   0/1     Pending       0          0s      <none>         <none>                                                     <none>           <none>

```

5) Validate the login now. 

```
[root@dom14npv101-infra-manager ~ hub]# oc login -u nokia -p nokia@123
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login failed (401 Unauthorized)
Verify you have provided the correct credentials.
[root@dom14npv101-infra-manager ~ hub]# oc login -u nokia -p nokia@1234
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

[root@dom14npv101-infra-manager ~ hub]# 

```


#### Procedure to `delete` an user completely


1) Retrieve the htpasswd file from the htpass-secret Secret object and save the file to your file system:

```
[root@dom14npv101-infra-manager ~ hub]# oc get secret htpass-secret -ojsonpath={.data.htpasswd} -n openshift-config | base64 --decode > users.htpasswd
[root@dom14npv101-infra-manager ~ hub]# cat users.htpasswd
ncpadmin:$2y$05$DYlpXiwFzfyRioO4hRNq1.ZdFLO3yMz3Pl3gs7.yUpEUKeOGoHX9K
nokia:$2y$05$SLpgZb3AE.fE7WQEGIMOXesoZdY9pV9OHVpXb5CuITdZO5RVId8Ye
[root@dom14npv101-infra-manager ~ hub]# 
```

2) remove users from the users.htpasswd file.

```
[root@dom14npv101-infra-manager ~ hub]# htpasswd -D users.htpasswd nokia
Deleting password for user nokia
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
[root@dom14npv101-infra-manager ~ hub]# oc get pods -n openshift-authentication -o wide -w
NAME                             READY   STATUS    RESTARTS   AGE     IP             NODE                                                       NOMINATED NODE   READINESS GATES
oauth-openshift-f446bd5b-58cps   1/1     Running   0          6m48s   172.20.2.190   ncpvnpvhub-hubmaster-101.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-k8dqx   1/1     Running   0          5m53s   172.21.0.241   ncpvnpvhub-hubmaster-103.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-v4n6m   1/1     Running   0          6m21s   172.20.0.134   ncpvnpvhub-hubmaster-102.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-f446bd5b-v4n6m   1/1     Terminating   0          6m24s   172.20.0.134   ncpvnpvhub-hubmaster-102.ncpvnpvhub.pnwlab.nsn-rdnet.net   <none>           <none>
oauth-openshift-6497ccb4f5-d5wxd   0/1     Pending       0          0s      <none>         <none>                                                     <none>           <none>
oauth-openshift-6497ccb4f5-d5wxd   0/1     Pending       0          0s      <none>         <none>                                                     <none>           <none>

```

5) If you removed one or more users, you must additionally remove existing resources for each user.

    a) Delete the User object:

    ```
    [root@dom14npv101-infra-manager ~ hub]# oc get user 
    NAME       UID                                    FULL NAME   IDENTITIES
    ncpadmin   8e728883-a17f-4bde-8b0f-2eab78ccc6c3               my_htpasswd_provider:ncpadmin
    nokia      7e44ba3a-8d91-435f-800f-380a8e87f0d1               my_htpasswd_provider:nokia
    [root@dom14npv101-infra-manager ~ hub]# oc delete user nokia 
    user.user.openshift.io "nokia" deleted
    [root@dom14npv101-infra-manager ~ hub]# 

    ```
    b) Be sure to remove the user, otherwise the user can continue using their token as long as it has not expired.

    ```
    [root@dom14npv101-infra-manager ~ hub]#  oc get identity 
    NAME                            IDP NAME               IDP USER NAME   USER NAME   USER UID
    my_htpasswd_provider:ncpadmin   my_htpasswd_provider   ncpadmin        ncpadmin    8e728883-a17f-4bde-8b0f-2eab78ccc6c3
    my_htpasswd_provider:nokia      my_htpasswd_provider   nokia           nokia       7e44ba3a-8d91-435f-800f-380a8e87f0d1
    [root@dom14npv101-infra-manager ~ hub]# oc delete identity my_htpasswd_provider:nokia  
    identity.user.openshift.io "my_htpasswd_provider:nokia" deleted
    [root@dom14npv101-infra-manager ~ hub]# 
    ```

5) Validate the login and it should not work. 

```
[root@dom14npv101-infra-manager ~ hub]# oc login -u nokia -p nokia@1234
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login failed (401 Unauthorized)
Verify you have provided the correct credentials.
[root@dom14npv101-infra-manager ~ hub]# 

```

#### Disclaimer 

> All these procedures are collected from redhat link given below. 

#### References

* [Configuring an htpasswd identity provider ](https://docs.redhat.com/en/documentation/openshift_container_platform/4.10/html/authentication_and_authorization/configuring-identity-providers#identity-provider-htpasswd-update-users_configuring-htpasswd-identity-provider)


* [To configure an HTPasswd identity provider in OpenShift 4](https://access.redhat.com/solutions/4039941#:~:text=Prerequisites,Example%20output:)

* [Remove kubeadmin id](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/authentication_and_authorization/removing-kubeadmin#understanding-kubeadmin_removing-kubeadmin)
