# Proxy-cache quay based pod creation

## proxy-cache TLS issue. 

1. login to hub cluster and run this command 
```
[root@ncputility ~ pancwl_rc]$ source /root/panhubrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 105 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
[root@ncputility ~ panhub_rc]$ oc get secret -n openshift-ingress-operator router-ca -o "jsonpath={.data['tls\.crt']}" | base64 -d
-----BEGIN CERTIFICATE-----
MIIDDDCCAfSgAwIBAgIBATANBgkqhkiG9w0BAQsFADAmMSQwIgYDVQQDDBtpbmdy
ZXNzLW9wZXJhdG9yQDE3NDAwNzQ1NDQwHhcNMjUwMjIwMTgwMjIzWhcNMjcwMjIw
MTgwMjI0WjAmMSQwIgYDVQQDDBtpbmdyZXNzLW9wZXJhdG9yQDE3NDAwNzQ1NDQw
ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDjXWFSVPshwihivZhaTrB7
0boUOw2j3Ut/J6eSm+JA+xVl05L4XD8+C8VSst+f32Pe42Lso2hrovY1dT7IBX3g
6S9Nnd2iRc9vC/qHcQkGQ6krIYSQ48aCH7UuahCpTqxEp+MwmhCTQngN2maTJBe3
0E6K2IL4zXSi0Iuj08BOnH/w4pJxeWhyngXDf2SeA88EmU3juHLshHrAND84uou2
/sOStIAhFwU+o887dSgx7iERy+6nczSDB9Qvq11cUSS4RPC82bNnxcc+BrynDwZ/
eggs0OEaj/1cHu/svKZHX9gUKrqz80wF8YGZLLgI2oPAf2VJorvtkJAErzgttroF
AgMBAAGjRTBDMA4GA1UdDwEB/wQEAwICpDASBgNVHRMBAf8ECDAGAQH/AgEAMB0G
A1UdDgQWBBTZS/SzkBfiHQ5/Gy+b4g1XJOHkojANBgkqhkiG9w0BAQsFAAOCAQEA
UwPhAbzTWZIlBsMHAL+8jvxM8qxc6HDhayAD4gbCE65vHYgSizost02vRfpOPQq1
D6HM8JjifS3KHd6E6chdTbrHI0W8pMJJPon5akCJf/uGeGDl+2wKfmVC6UoV7hC3
pcUzm3JKwsNJbjS5rxL8f5a8bNdIFfLQKuyRpnVX2CsNHvh+WJzynQ+PUJ6zCa7y
x5AJxca2PTnBKRoVTAyumT1suluI9f4GRYnxTE/qIKRZRs+uT3kIl/N9VX+GbjGb
pPszJ+p6N6Arl1BqJP1DdLin2IFGZL39pTyifm5GP+Vou2aHPuHZDVoCdxsFKup+
gUY2KeKz0UManwubPQNnKA==
-----END CERTIFICATE-----
[root@ncputility ~ panhub_rc]$

```

2. login to workload cluster and run this command 
```
[root@ncputility ~ pancwl_rc]$ source /root/pancwlrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 115 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "nokia".
[root@ncputility ~ pancwl_rc]$ oc get cm -n openshift-config user-ca-bundle -o yaml
apiVersion: v1
data:
  ca-bundle.crt: |
    -----BEGIN CERTIFICATE-----
    MIIDDDCCAfSgAwIBAgIBATANBgkqhkiG9w0BAQsFADAmMSQwIgYDVQQDDBtpbmdy
    ZXNzLW9wZXJhdG9yQDE3NDAwNzQ1NDQwHhcNMjUwMjIwMTgwMjIzWhcNMjcwMjIw
    MTgwMjI0WjAmMSQwIgYDVQQDDBtpbmdyZXNzLW9wZXJhdG9yQDE3NDAwNzQ1NDQw
    ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDjXWFSVPshwihivZhaTrB7
    0boUOw2j3Ut/J6eSm+JA+xVl05L4XD8+C8VSst+f32Pe42Lso2hrovY1dT7IBX3g
    6S9Nnd2iRc9vC/qHcQkGQ6krIYSQ48aCH7UuahCpTqxEp+MwmhCTQngN2maTJBe3
    0E6K2IL4zXSi0Iuj08BOnH/w4pJxeWhyngXDf2SeA88EmU3juHLshHrAND84uou2
    /sOStIAhFwU+o887dSgx7iERy+6nczSDB9Qvq11cUSS4RPC82bNnxcc+BrynDwZ/
    eggs0OEaj/1cHu/svKZHX9gUKrqz80wF8YGZLLgI2oPAf2VJorvtkJAErzgttroF
    AgMBAAGjRTBDMA4GA1UdDwEB/wQEAwICpDASBgNVHRMBAf8ECDAGAQH/AgEAMB0G
    A1UdDgQWBBTZS/SzkBfiHQ5/Gy+b4g1XJOHkojANBgkqhkiG9w0BAQsFAAOCAQEA
    UwPhAbzTWZIlBsMHAL+8jvxM8qxc6HDhayAD4gbCE65vHYgSizost02vRfpOPQq1
    D6HM8JjifS3KHd6E6chdTbrHI0W8pMJJPon5akCJf/uGeGDl+2wKfmVC6UoV7hC3
    pcUzm3JKwsNJbjS5rxL8f5a8bNdIFfLQKuyRpnVX2CsNHvh+WJzynQ+PUJ6zCa7y
    x5AJxca2PTnBKRoVTAyumT1suluI9f4GRYnxTE/qIKRZRs+uT3kIl/N9VX+GbjGb
    pPszJ+p6N6Arl1BqJP1DdLin2IFGZL39pTyifm5GP+Vou2aHPuHZDVoCdxsFKup+
    gUY2KeKz0UManwubPQNnKA==
    -----END CERTIFICATE-----
kind: ConfigMap
metadata:
  annotations:
    openshift.io/owning-component: End User
  creationTimestamp: "2025-03-03T08:56:26Z"
  name: user-ca-bundle
  namespace: openshift-config
  resourceVersion: "43318895"
  uid: 6624e5ad-93b5-418e-8c1e-7a91c724a760
[root@ncputility ~ pancwl_rc]$ oc get proxy cluster -o yaml
apiVersion: config.openshift.io/v1
kind: Proxy
metadata:
  creationTimestamp: "2025-03-03T08:54:59Z"
  generation: 2
  name: cluster
  resourceVersion: "48312416"
  uid: ceaebe02-9bd3-4361-847e-1b880ebb85de
spec:
  trustedCA:
    name: user-ca-bundle   <---------------------------- this should be patched. if missing. 
status: {}
[root@ncputility ~ pancwl_rc]$
```

3. login to workload cluster add tls of hub to cwl. 
```
[root@ncputility ~ pancwl_rc]$ oc patch proxy cluster --patch '{"spec":{"trustedCA":{"name":"user-ca-bundle"}}}' --type=merge
[root@ncputility ~ pancwl_rc]$ oc get proxy cluster -o yaml
apiVersion: config.openshift.io/v1
kind: Proxy
metadata:
  creationTimestamp: "2025-03-03T08:54:59Z"
  generation: 2
  name: cluster
  resourceVersion: "48312416"
  uid: ceaebe02-9bd3-4361-847e-1b880ebb85de
spec:
  trustedCA:
    name: user-ca-bundle
status: {}
[root@ncputility ~ pancwl_rc]$

```
## Configure the proxy cache on the registry level. 

### hub quay configiration

1. Open up the hub quay url 

### CWL quay configuration 

1. Open CWL quay login via super account and created an user called cnfowners also fix the passwd.

![alt text](image-1.png)
![alt text](image-2.png)

2. Create an org as same as hub quay. 

![alt text](image-3.png)

3. Set the proxy cache configuration for the organization

![alt text](image-5.png)

4. create robot account and default permission

![alt text](image-4.png)

5. Create a new team for image pull user

![alt text](image-6.png)

6. Set default permission for the pull user (optional)

<Organization> → Default Permissions → + Create Default Permission

7. Extend the global image pull secret

> During the Managed cluster installation, the global pull secret is configured. If the 2nd Hub Quay account and the cache account are not prepared in advance, these accounts need to be added. In case of mirrored registries, only the global pull secret can be used. It is not possible to add project specific pull secrets. For more information, see chapter Image configuration resources in document Images, available in OpenShift Container Platform Product documentation.

## Testing pod creation using `proxy-cache` quay. 

1. Login the namespace with cluster admin access to grand rights for an scc. 
```
[root@ncputility ~ pancwl_rc]$ source  /root/pancwlrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 116 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
[root@ncputility ~ pancwl_rc]$ 
```
2. Grand admin rights to project. if missed during project creation phase. 
```
[root@ncputility ~ pancwl_rc]$ oc policy add-role-to-user admin  nokia  -n nokia
clusterrole.rbac.authorization.k8s.io/admin added: "nokia"
[root@ncputility ~ pancwl_rc]$ 
```
3. Also grand scc role to default service account via anyuid. 
```
[root@ncputility ~ pancwl_rc]$ oc adm policy add-scc-to-user anyuid -z default -n nokia
clusterrole.rbac.authorization.k8s.io/system:openshift:scc:anyuid added: "default"
[root@ncputility ~ pancwl_rc]$ 
```
4. login to cnf tenant here .
```
[root@ncputility ~ pancwl_rc]$ oc login -u nokia -p nokia@123
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have one project on this server: "nokia"

Using project "nokia".
[root@ncputility ~ pancwl_rc]$ 
```
5. run an pod using proxy-cache url 
```
[root@ncputility ~ pancwl_rc]$  oc run podpingtest3 --image=ephemeral.url/cnfimages/testimage01:latest --restart=Never  -- tail -f /dev/null
pod/podpingtest3 created
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          4s
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          6s
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          8s
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          9s
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          11s
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS              RESTARTS   AGE
podpingtest3   0/1     ContainerCreating   0          13s
[root@ncputility ~ pancwl_rc]$ 
```
6. validate the pod status and make sure it's getting the image via proxy-cache. 
```
[root@ncputility ~ pancwl_rc]$ oc get pods
NAME           READY   STATUS    RESTARTS   AGE
podpingtest3   1/1     Running   0          5m1s
[root@ncputility ~ pancwl_rc]$


[root@ncputility ~ pancwl_rc]$ oc describe pod podpingtest3
Name:             podpingtest3
Namespace:        nokia
Priority:         0
Service Account:  default
Node:             appworker9.panclypcwl01.mnc020.mcc714/10.89.96.35
Start Time:       Fri, 04 Apr 2025 08:04:47 -0500
Labels:           run=podpingtest3
Annotations:      k8s.ovn.org/pod-networks:
                    {"default":{"ip_addresses":["172.19.21.252/23"],"mac_address":"0a:58:ac:13:15:fc","gateway_ips":["172.19.20.1"],"routes":[{"dest":"172.16....
                  k8s.v1.cni.cncf.io/network-status:
                    [{
                        "name": "ovn-kubernetes",
                        "interface": "eth0",
                        "ips": [
                            "172.19.21.252"
                        ],
                        "mac": "0a:58:ac:13:15:fc",
                        "default": true,
                        "dns": {}
                    }]
                  openshift.io/scc: anyuid
Status:           Running
IP:               172.19.21.252
IPs:
  IP:  172.19.21.252
Containers:
  podpingtest3:
    Container ID:  cri-o://749055ef608c6f30be42248c63889fd85377928389dae2e29eed50919cc2ee79
    Image:         ephemeral.url/cnfimages/testimage01:latest
    Image ID:      ephemeral.url/cnfimages/testimage01@sha256:32666e0234f88377a91de56bb78f2d4f8df45b4f99c1c2dc9ee1d134c84f4753
    Port:          <none>
    Host Port:     <none>
    Args:
      tail
      -f
      /dev/null
    State:          Running
      Started:      Fri, 04 Apr 2025 08:05:05 -0500
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-mp46w (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-mp46w:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
    ConfigMapName:           openshift-service-ca.crt
    ConfigMapOptional:       <nil>
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 60s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 60s
Events:
  Type    Reason          Age    From               Message
  ----    ------          ----   ----               -------
  Normal  Scheduled       6m5s   default-scheduler  Successfully assigned nokia/podpingtest3 to appworker9.panclypcwl01.mnc020.mcc714
  Normal  AddedInterface  6m4s   multus             Add eth0 [172.19.21.252/23] from ovn-kubernetes
  Normal  Pulling         6m4s   kubelet            Pulling image "ephemeral.url/cnfimages/testimage01:latest"
  Normal  Pulled          5m47s  kubelet            Successfully pulled image "ephemeral.url/cnfimages/testimage01:latest" in 17.521s (17.521s including waiting)
  Normal  Created         5m47s  kubelet            Created container podpingtest3
  Normal  Started         5m47s  kubelet            Started container podpingtest3
[root@ncputility ~ pancwl_rc]$

```

![alt text](image.png)




## CNF image upload using pod command 

1. login to hub quay using cnfowners and org as cnfimages. 

```
[root@ncputility ~ pancwl_rc]$ podman login quay-registry.apps.panclyphub01.mnc020.mcc714 -u cnfowners -p cnfowners
Login Succeeded!
[root@ncputility ~ pancwl_rc]$

```

2. load the container images to log registry 
```
[root@ncputility ~ pancwl_rc]$ podman load -i <filename>.tar^C
[root@ncputility ~ pancwl_rc]$
```

3. tag the image to your registry here 

```
[root@ncputility ~ pancwl_rc]$ podman tag quay-registry.apps.panclyphub01.mnc020.mcc714/cnfimages/testimage01 quay-registry.apps.panclyphub01.mnc020.mcc714/cnfimagesnew/testimage01:latest
[root@ncputility ~ pancwl_rc]$
```

4. push the image to remore registry using podman push command here .
```
[root@ncputility ~ pancwl_rc]$ podman push quay-registry.apps.panclyphub01.mnc020.mcc714/cnfimagesnew/testimage01:latest
Getting image source signatures
Copying blob 1af69dabfc93 done   |
Copying blob 53f86715cdba done   |
Copying blob b6361360b38a done   |
Copying config d39b33df22 done   |
Writing manifest to image destination
[root@ncputility ~ pancwl_rc]$
```