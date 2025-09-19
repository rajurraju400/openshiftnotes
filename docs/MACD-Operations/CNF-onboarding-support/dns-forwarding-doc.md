# DNS with Optional Zone-Specific Forwarder Configuration

## Prerequisites

The configuration can be started after installing the DNS Operator via subscription from a common `PolicyGenTemplate`.

To add zone-specific external DNS forwarders that override the default forwarding configuration in `/etc/resolv.conf`, you must create
zone-specific `forwardPlugin` settings with the target DNS forwarders in `spec.servers` for every zone.

> **Note:** Zone-specific external DNS forwarders cannot be defined for
> the cluster domain `cluster.local`.

------------------------------------------------------------------------

## Important Notes

-   The instructions for defining the upstream DNS servers in `spec.upstreamResolvers` are **not covered here**. The upstream DNS servers are used for DNS zones where no zone-specific forwarders match the DNS query.
-   This does not cover any details about modifying the general DNS Operator settings for the ConfigMap named `dns-default`.
-   For more information, see **Understanding the DNS Operator** in the *Networking* documentation of OpenShift Container Platform.

> **Note:** Similar `dns-default` ConfigMap settings may also be
> required for multiple zone-specific DNS forwarders in customer setups.
> For example: - ENUM with the `e164.arpa` zone for IMS Core related
> CNFs. - `3gppnetwork.org` zone for 3GPP 5GC NFs.

------------------------------------------------------------------------

## Configuration

Create a `ConfigMap` for the DNS `forwardPlugin` with additional server configuration blocks in `spec.servers` for zone-specific forwarders.
This is used for updating the ConfigMap named `dns-default`.

> **Note:** In this example, the default policy **Random** is used for
> selecting upstream resolvers. Other policies such as **RoundRobin** or
> **Sequential** can also be selected.

### Example: `dns-forwarding.yaml`

``` yaml
site-policies/sites/hub/source-crs/coredns/dns-forwarding.yaml
apiVersion: operator.openshift.io/v1
kind: DNS
metadata:
  name: default
spec:
  servers:
  - forwardPlugin:
      policy: Random
      upstreams:
      - 10.99.42.53
      - 10.99.42.54
    name: 3gppnetwork
    zones:
    - 3gppnetwork.org
```
#### Example-2: (multi domain)

```
```

After the new DNS operator object (configuration) is created, it can be
added to the cluster via `PolicyGenTemplate`:

``` yaml
…
    # NCPFM-501 CoreDNS with zone-specific forwardPlugin settings
     - fileName: coredns/dns-forwarding.yaml
       policyName: config-policies
…
```

------------------------------------------------------------------------

## Validation

### Check DNS Operator and `forwardPlugin` Status

``` bash
$ oc get clusteroperator/dns
NAME   VERSION   AVAILABLE   PROGRESSING   DEGRADED   SINCE   MESSAGE
dns    4.14.29   True        False         False      19d

$ oc get -n openshift-dns-operator deployment/dns-operator
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
dns-operator   1/1     1            1           19d
```

### Validate Current `dns-default` Configuration

``` bash
$ oc describe dns.operator/default
```

Example output:

    Spec:
      Servers:
        Forward Plugin:
          Policy:  Random
          Upstreams:
            10.99.42.53
            10.99.42.54
        Name:  3gppnetwork
        Zones:
          3gppnetwork.org
      Upstream Resolvers:
        Policy:             Sequential
        Protocol Strategy:
        Transport Config:
        Upstreams:
          Port:  53
          Type:  SystemResolvConf

### Inspect ConfigMap `dns-default`

``` bash
$ oc get configmap/dns-default -n openshift-dns -o yaml
```

Example:

``` yaml
apiVersion: v1
data:
  Corefile: |
    # 3gppnetwork
    3gppnetwork.org:5353 {
        prometheus 127.0.0.1:9153
        forward . 10.99.42.53 10.99.42.54 {
            policy random
        }
        errors
        log . {
            class error
        }
        bufsize 1232
        cache 900 {
            denial 9984 30
        }
    }
kind: ConfigMap
metadata:
  name: dns-default
  namespace: openshift-dns
```

### View DNS Operator Logs

``` bash
$ oc logs -n openshift-dns-operator deployment/dns-operator -c dns-operator
```

------------------------------------------------------------------------

## Summary

This guide covered how to configure zone-specific DNS forwarders with the OpenShift DNS Operator using `forwardPlugin` settings. It also included validation steps to confirm the operator and configuration are functioning correctly.
