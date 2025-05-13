# Container Image download issue due to TLS problem. 


### Creating tls certificate on the OCP cluster as additional tls `newly`

#### This step will resolve issue on Linux OS level(bastion host level)

> In order to be able to push images (for example) from the infra node to this Quay, the rootCA certificate shall be put to the trusted list of the client. The Quay is exposed using the OCP’s default ingress controller, route, so its rootCA shall be fetched (if it was not swapped already).


1) from bastion host, login to respective cluster and find the respective CWL cluster quay url. 
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get route -A |grep -i quay
quay-registry              quay-registry-quay                          quay-registry.apps.ncpvnpvlab1.pnwlab.nsn-rdnet.net                                                             quay-registry-quay-app                             http         edge/Redirect          None
quay-registry              quay-registry-quay-builder                  quay-registry-quay-builder-quay-registry.apps.ncpvnpvlab1.pnwlab.nsn-rdnet.net                                  quay-registry-quay-app                             grpc         edge/Redirect          None
[root@dom14npv101-infra-manager ~ vlabrc]# 
```

2) first locally resolve it, so make dir and download the cert (this is resolve on that particular linux server.)

```
[root@dom14npv101-infra-manager ~ vlabrc]# sudo mkdir -p /etc/containers/certs.d/quay-registry.apps.ncpvnpvlab1.pnwlab.nsn-rdnet.net
[root@dom14npv101-infra-manager ~ vlabrc]#
```

3) create the ingress certificate to local host 

```
[root@dom14npv101-infra-manager ~ vlabrc]# oc get secrets -n openshift-ingress-operator router-ca \
-o jsonpath="{.data['tls\.crt']}" | base64 -d | \
sudo tee -a \
/etc/containers/certs.d/quay-registry.apps.ncpvnpvlab1.pnwlab.nsn-rdnet.net/ca.crt
-----BEGIN CERTIFICATE-----
MIIDDDCCAfSgAwIBAgIBATANBgkqhkiG9w0BAQsFADAmMSQwIgYDVQQDDBtpbmdy
ZXNzLW9wZXJhdG9yQDE3NDE2MjI1OTkwHhcNMjUwMzEwMTYwMzE4WhcNMjcwMzEw
MTYwMzE5WjAmMSQwIgYDVQQDDBtpbmdyZXNzLW9wZXJhdG9yQDE3NDE2MjI1OTkw
ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCtDCDqA6Cx+MvulZtYNleK
T3e4OVlQrR8zytgIQIvlLpeGoqsoNWEe/ZukJ35fco6LA42RcIiI+F5aI6zZ4+F8
81ZEpsSRBx8VUMsZCdkb5mA8tl5vJjV+GC1tRlohk6KWqYoR5VJVLbggFer95efv
xyny/BCYXmU2CSHSmRQRnwAI6cX0K7QgEB0kMHaFjEta16UnwzKdhNbaj5rn0aTm
hLSGYLvPMx9RVZswjqOqrju0Aovfv9ZzzE++e6+KH9/jZr2HepK62ZZdGznbmnzu
Al0D+ILaVj8DiFpcwUIaSaRxUVlphAUmm530GLbKrBdQGSsWcJTo4ixf8R2wYo69
AgMBAAGjRTBDMA4GA1UdDwEB/wQEAwICpDASBgNVHRMBAf8ECDAGAQH/AgEAMB0G
A1UdDgQWBBQMuq1odXMd4OlIU4vG8Kfu/aLltjANBgkqhkiG9w0BAQsFAAOCAQEA
BVerN+fxay+kk9uei+bQIpryakFstJ5ApuB1wDKgLY3LucwbzXhaE48i9TEOoNlB
32ugNpShYQoOyVMMAvQNQG69HNu0KDJHYGDMAs4seGIsMwqityS6Zgv8T3xo176g
mR0y74yiK1ImtnUAaAPt7NNFflhpZafzhY24k4L3AVNEjMKI9B2SgUJAscmXkNIZ
Dri+EILpba6MzmeLdE3sVTaOIRberr6yTKbZQskaci+twaO7r83hD3E3xwGJB823
Zu+B2i/txKbBrFeKUpppfrg7zCsyqM1UwFtenuj1yj3qECJVwe1Lr8SctrzpJc+J
ryyB1JeEPQWwewI1j7QXqg==
-----END CERTIFICATE-----
[root@dom14npv101-infra-manager ~ vlabrc]#

```

#### On the OCP cluster level changes, TLS Creation

1) Similarly if images would be pulled on the HUB cluster, its ingress’ rootCA shall be put into the image.config.openshift.io/cluster CR, as the registry is using self-signed certificate by default and treated as an insecure registry, more precisely the OCP’s ingress (if it is not swapped yet). In order to overcome issues the following commands:
```
 [root@dom14npv101-infra-manager ~ vlabrc]# oc get secrets -n openshift-ingress-operator router-ca \
-o jsonpath="{.data['tls\.crt']}" | base64 -d > ingress_ca.crt
[root@dom14npv101-infra-manager ~ vlabrc]# 
```

2) create an cm to enforce the certificate here.
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc create configmap registry-cas -n openshift-config \
--from-file=quay-registry.apps.ncpvnpvlab1.pnwlab.nsn-rdnet.net=ingress_ca.crt
configmap/registry-cas created
[root@dom14npv101-infra-manager ~ vlabrc]# 
```
3) now create an image patch to cluster iamge config. 
```
[root@dom14npv101-infra-manager ~ vlabrc]# oc patch image.config.openshift.io/cluster --patch '{"spec":
{"additionalTrustedCA":{"name":"registry-cas"}}}' \
--type=merge
image.config.openshift.io/cluster patched
[root@dom14npv101-infra-manager ~ vlabrc]#
```

### Creating tls certificate on the OCP cluster as additional tls `ADD`

1) oc apply is the preferred way to update an existing resource, including ConfigMaps. This command will update the ConfigMap with the new data while keeping existing data intact. If you don’t have a YAML file, you can first export the current ConfigMap to a file, edit it, and then apply the changes:


```
oc get configmap registry-cas -n openshift-config -o yaml > registry-cas.yaml

oc apply -f registry-cas.yaml
```

2) If you need to update the existing ConfigMap with new or modified data directly from the command line, you can force the update with oc create configmap using the --dry-run and --force flags:

```
oc create configmap registry-cas -n openshift-config \
--from-file=harbor.ncdvnpv.ncpvnpvmgt.pnwlab.nsn-rdnet.net=ingress_ca.crt \
--dry-run=client -o yaml | oc replace -f -

```

3) Using oc patch (for small changes) Optional extra steps 
```
oc patch configmap registry-cas -n openshift-config \
  --type='json' \
  -p='[{"op": "replace", "path": "/data/harbor.ncdvnpv.ncpvnpvmgt.pnwlab.nsn-rdnet.net", "value": "ingress_ca.crt"}]'
```