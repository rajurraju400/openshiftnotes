# Oc login ssl error on OCP

> To login to NWC cluster, oauth-serving-cert (second certificate) to be copied to /etc/pki/ca-trust/source/anchors/ and then run sudo update-ca-trust extract command. It should be done for each NWC cluster.
 
1. To get the certificate, execute below command on NWC cluster.
 
```
[root@ncputility ~ panhub_rc]$ oc get configmaps -n openshift-config-managed oauth-serving-cert -o yaml
apiVersion: v1
data:
  ca-bundle.crt: |2

    -----BEGIN CERTIFICATE-----
    MIIDeTCCAmGgAwIBAgIIItt373u4MZMwDQYJKoZIhvcNAQELBQAwJjEkMCIGA1UE
    AwwbaW5ncmVzcy1vcGVyYXRvckAxNzQwMDc0NTQ0MB4XDTI1MDIyMDE4MDIyM1oX
    DTI3MDIyMDE4MDIyNFowLDEqMCgGA1UEAwwhKi5hcHBzLnBhbmNseXBodWIwMS5t
    bmMwMjAubWNjNzE0MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoNne
    91mbAMQEjKAyOBWp0wGYpELbNKgYtgUGqL0zteOA3WI+opnJnpTPztlqr4Xqddyw
    EAuPS7gjUqplbwJROO0lQ+sDSVqfOCC7wvrkd6pI/0jxWPK9WgnSZt1lmiJ9L0Rs
    s7H5iVdUq8hvIfI9ZUzvr2BUGi9StdABRFoxk1R+BF6yRRiQnxhyqhYjPOuzV4GM
    blfDAvo3yqFoMOHo0DTZQXcRLQnbt2a3ApPHcsLgyBjTmOMlPilRSHtVFivQP2Pd
    VRhZGSsAANk7aJyCvHZ+oMo0DLUqmBgikHpgm9TAv6M+oX0kbfdqfMci8sEF7Vqj
    9fK5l19t+zZaXTnH3QIDAQABo4GkMIGhMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUE
    DDAKBggrBgEFBQcDATAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBTsyQRlbeyo2H/V
    f887YPhF8jVixDAfBgNVHSMEGDAWgBTZS/SzkBfiHQ5/Gy+b4g1XJOHkojAsBgNV
    HREEJTAjgiEqLmFwcHMucGFuY2x5cGh1YjAxLm1uYzAyMC5tY2M3MTQwDQYJKoZI
    hvcNAQELBQADggEBAE6kBjPoA3RJI09pYfUzQlEyKQrnudNTu+O61ZspCPvafp4s
    4py8hyS/pzkp7611KfmJnzXjiBjw6qzcE5lye4coO5vwplYDbZUTCn9bz30+2g1O
    wpA1ZOLLTHet11+i0FG0m4AJq4OXEjHuA1K2+AyfzG0TsogT88WstndoNPtGrYWJ
    pj1kQYbVqwBtCU/jhKbXycEQ+UdeICRuNp5FbBcJ/ZrxJRmJa/zUkT6tHWMvzlsI
    IPrTpL7BEkoRtWPYhcW4gL70XgkmahuX2bssG7C2IJxN2DNTvmFsMSWHzQNc7AaD
    ND+v4E+mn2zKhzdQyOB4Mx6H4LH5cEHZsLfVal8=
    -----END CERTIFICATE-----

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
    openshift.io/owning-component: apiserver-auth
  creationTimestamp: "2025-02-20T18:02:31Z"
  name: oauth-serving-cert
  namespace: openshift-config-managed
  resourceVersion: "73869405"
  uid: a08c0137-033d-41d0-9c79-8f345662140c
[root@ncputility ~ panhub_rc]$

```
 
2. Then copy second certificate and put it in a file. Move this file to `/etc/pki/ca-trust/source/anchors/`Post that, run `update-ca-trust extrace `command.
 
 
3. Create separate linux user and do oc login kubeadmin, password and api url (find from the kubeconfig) file.
 
