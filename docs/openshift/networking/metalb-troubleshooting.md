# metalb configuration troubleshooting 

1.  login to cluster 
```
[root@ncputility ~ pancwl_rc]$ source /root/pancwlrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 113 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "ncd01pan".

```
2. check for `metallb-system` namespace exist

[root@ncputility ~ pancwl_rc]$ oc get ns | grep -i metallb
metallb-system                                     Active   26d
[root@ncputility ~ pancwl_rc]$

3. check the status of the pods on the `metallb-system` namespace here. 
```
[root@ncputility ~ pancwl_rc]$ oc get pods -n metallb-system
NAME                                                   READY   STATUS    RESTARTS   AGE
controller-5785bc85cb-qpk8h                            2/2     Running   0          24d
metallb-operator-controller-manager-7bf5d8978d-clpd7   1/1     Running   0          26d
metallb-operator-webhook-server-86784c6c8c-49ncp       1/1     Running   0          26d
speaker-dlrn5                                          6/6     Running   0          24d
speaker-g2g77                                          6/6     Running   0          24d
speaker-jzbw7                                          6/6     Running   0          24d
speaker-pjstl                                          6/6     Running   0          24d
```

4. check for `bfdprofile` on this cluster 
> here transmit interval and receiver interval should be equal from local and remote end. 

```
 oc -n metallb-system get BFDProfile -o wide
NAME                                PASSIVE MODE   TRANSMIT INTERVAL   RECEIVE INTERVAL   MULTIPLIER
ncp-metallb-oam-pa-hn-bfd-profile   true           300                 300                3
ncp-metallb-oam-pa-ni-bfd-profile   true           300                 300                3
ncp-metallb-oam-pa-pa-bfd-profile   true           300                 300                3
ncp-metallb-oam-pa-sv-bfd-profile   true           300                 300                3
```

5. make sure, desination having the backward route configured here .

```
[root@ncputility ~ pancwl_rc]$ oc -n metallb-system get nncp -o wide
NAME                                           STATUS      REASON
backward-route-for-oam-pa-pa-metallb-vlan104   Available   SuccessfullyConfigured
ncp-metallb-oam-pa-hn-route-for-switches-105   Available   SuccessfullyConfigured
ncp-metallb-oam-pa-ni-route-for-switches-107   Available   SuccessfullyConfigured
ncp-metallb-oam-pa-pa-route-for-switches-104   Available   SuccessfullyConfigured
ncp-metallb-oam-pa-sv-route-for-switches-106   Available   SuccessfullyConfigured
tenant-bond-bgp-oam-vlan104-gateway-0          Available   SuccessfullyConfigured
tenant-bond-bgp-oam-vlan104-gateway-1          Available   SuccessfullyConfigured
tenant-bond-bgp-oam-vlan104-gateway-2          Available   SuccessfullyConfigured
** output omitted **
tenantvlan-373                                 Available   SuccessfullyConfigured
tenantvlan-374                                 Available   SuccessfullyConfigured
```
6. check for `ipaddresspool` exist here, so that application can create their `service` as `loadbalancer` here . 

```[root@ncputility ~ pancwl_rc]$ oc -n metallb-system get IPAddressPool -o wide
NAME                                AUTO ASSIGN   AVOID BUGGY IPS   ADDRESSES
ncp-metallb-oam-pa-hn-addresspool   false         false             ["10.89.147.128/28"]
ncp-metallb-oam-pa-ni-addresspool   false         false             ["10.86.10.16/28"]
ncp-metallb-oam-pa-pa-addresspool   false         false             ["10.89.101.128/27","10.89.97.208/28"]
ncp-metallb-oam-pa-sv-addresspool   false         false             ["10.85.186.240/28"]
```

7. check for `bgppeer` are up on the metallb speakers thats important for this communication

```[root@ncputility ~ pancwl_rc]$ oc -n metallb-system get BGPPeer -o wide
NAME                               ADDRESS         ASN          BFD PROFILE                         MULTI HOPS
ncp-metallb-oam-pa-hn-bgp-peer-1   10.89.147.194   4200000320   ncp-metallb-oam-pa-hn-bfd-profile
ncp-metallb-oam-pa-hn-bgp-peer-2   10.89.147.195   4200000320   ncp-metallb-oam-pa-hn-bfd-profile
ncp-metallb-oam-pa-ni-bgp-peer-1   10.86.10.98     4200000320   ncp-metallb-oam-pa-ni-bfd-profile
ncp-metallb-oam-pa-ni-bgp-peer-2   10.86.10.99     4200000320   ncp-metallb-oam-pa-ni-bfd-profile
ncp-metallb-oam-pa-pa-bgp-peer-1   10.89.97.162    4200000320   ncp-metallb-oam-pa-pa-bfd-profile
ncp-metallb-oam-pa-pa-bgp-peer-2   10.89.97.163    4200000320   ncp-metallb-oam-pa-pa-bfd-profile
ncp-metallb-oam-pa-sv-bgp-peer-1   10.85.187.34    4200000320   ncp-metallb-oam-pa-sv-bfd-profile
ncp-metallb-oam-pa-sv-bgp-peer-2   10.85.187.35    4200000320   ncp-metallb-oam-pa-sv-bfd-profile
```

8. check for `BGPAdvertisement` are created on this cluster and it should be in the `metallb-system` namespace. 

```
[root@ncputility ~ pancwl_rc]$ oc -n metallb-system get BGPAdvertisement -o wide
NAME                                      IPADDRESSPOOLS                          IPADDRESSPOOL SELECTORS   PEERS                                                                     NODE SELECTORS
ncp-metallb-oam-pa-hn-bgp-advertisement   ["ncp-metallb-oam-pa-hn-addresspool"]                             ["ncp-metallb-oam-pa-hn-bgp-peer-1","ncp-metallb-oam-pa-hn-bgp-peer-2"]
ncp-metallb-oam-pa-ni-bgp-advertisement   ["ncp-metallb-oam-pa-ni-addresspool"]                             ["ncp-metallb-oam-pa-ni-bgp-peer-1","ncp-metallb-oam-pa-ni-bgp-peer-2"]
ncp-metallb-oam-pa-pa-bgp-advertisement   ["ncp-metallb-oam-pa-pa-addresspool"]                             ["ncp-metallb-oam-pa-pa-bgp-peer-1","ncp-metallb-oam-pa-pa-bgp-peer-2"]
ncp-metallb-oam-pa-sv-bgp-advertisement   ["ncp-metallb-oam-pa-sv-addresspool"]                             ["ncp-metallb-oam-pa-sv-bgp-peer-1","ncp-metallb-oam-pa-sv-bgp-peer-2"]
```


10. No, error from the container logs on this namespace .
```
[root@ncputility ~ pancwl_rc]$ oc -n metallb-system logs -l component=speaker
Defaulted container "speaker" out of: speaker, frr, reloader, frr-metrics, kube-rbac-proxy, kube-rbac-proxy-frr, cp-frr-files (init), cp-reloader (init), cp-metrics (init)
Defaulted container "speaker" out of: speaker, frr, reloader, frr-metrics, kube-rbac-proxy, kube-rbac-proxy-frr, cp-frr-files (init), cp-reloader (init), cp-metrics (init)
Defaulted container "speaker" out of: speaker, frr, reloader, frr-metrics, kube-rbac-proxy, kube-rbac-proxy-frr, cp-frr-files (init), cp-reloader (init), cp-metrics (init)
Defaulted container "speaker" out of: speaker, frr, reloader, frr-metrics, kube-rbac-proxy, kube-rbac-proxy-frr, cp-frr-files (init), cp-reloader (init), cp-metrics (init)
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:12Z"}
{"caller":"speakerlist.go:274","level":"info","msg":"triggering discovery","op":"memberDiscovery","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:44Z"}
{"caller":"speakerlist.go:274","level":"info","msg":"triggering discovery","op":"memberDiscovery","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway4.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:07Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/gateway3.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:12Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker16.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:21Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker20.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:34Z"}
{"caller":"node_controller.go:46","controller":"NodeReconciler","level":"info","start reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","ts":"2025-03-31T04:44:44Z"}
{"caller":"node_controller.go:69","controller":"NodeReconciler","end reconcile":"/appworker28.panclypcwl01.mnc020.mcc714","level":"info","ts":"2025-03-31T04:44:44Z"}
```
11.  just showing an backwards route here for comparison  and your destination should be exist here . 
```
[root@ncputility ~ pancwl_rc]$ oc get nncp -A -o yaml
apiVersion: v1
items:
- apiVersion: nmstate.io/v1
  kind: NodeNetworkConfigurationPolicy
  metadata:
    annotations:
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"nmstate.io/v1","kind":"NodeNetworkConfigurationPolicy","metadata":{"annotations":{},"name":"backward-route-for-oam-pa-pa-metallb-vlan104"},"spec":{"desiredState":{"routes":{"config":[{"destination":"10.89.100.66/32","metric":150,"next-hop-address":"10.89.97.161","next-hop-interface":"vlan104","table-id":254},{"destination":"10.89.27.4/32","metric":150,"next-hop-address":"10.89.97.161","next-hop-interface":"vlan104","table-id":254}]}},"nodeSelector":{"node-role.kubernetes.io/gateway":""}}}
      nmstate.io/webhook-mutating-timestamp: "1743107464714866687"
    creationTimestamp: "2025-03-27T20:31:04Z"
    generation: 1
    name: backward-route-for-oam-pa-pa-metallb-vlan104
    resourceVersion: "36077334"
    uid: d72a67aa-44d0-403f-8ed5-29a49994eaf6
  spec:
    desiredState:
      routes:
        config:
        - destination: 10.89.100.66/32
          metric: 150
          next-hop-address: 10.89.97.161
          next-hop-interface: vlan104
          table-id: 254
        - destination: 10.89.27.4/32
          metric: 150
          next-hop-address: 10.89.97.161
          next-hop-interface: vlan104
          table-id: 254
    nodeSelector:
      node-role.kubernetes.io/gateway: ""
  status:
    conditions:
    - lastHeartbeatTime: "2025-03-27T20:32:10Z"
      lastTransitionTime: "2025-03-27T20:32:10Z"
      message: 4/4 nodes successfully configured
      reason: SuccessfullyConfigured
      status: "True"
      type: Available
    - lastHeartbeatTime: "2025-03-27T20:32:10Z"
      lastTransitionTime: "2025-03-27T20:32:10Z"
      reason: SuccessfullyConfigured
      status: "False"
      type: Degraded
    - lastHeartbeatTime: "2025-03-27T20:32:10Z"
      lastTransitionTime: "2025-03-27T20:32:10Z"
      reason: ConfigurationProgressing
      status: "False"
      type: Progressing
    lastUnavailableNodeCountUpdate: "2025-03-27T20:32:09Z"
```

12.  Check the status of local and remote configuration by login into the metallb-system namespace. 

``bdf and bgp should be fully up``
```
[root@ncputility ~ pancwl_rc]$ oc get -n metallb-system pods -l component=speaker -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP            NODE                                  NOMINATED NODE   READINESS GATES
speaker-dlrn5   6/6     Running   0          24d   10.89.96.18   gateway2.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-g2g77   6/6     Running   0          24d   10.89.96.19   gateway3.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-jzbw7   6/6     Running   0          24d   10.89.96.17   gateway1.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-pjstl   6/6     Running   0          24d   10.89.96.20   gateway4.panclypcwl01.mnc020.mcc714   <none>           <none>
[root@ncputility ~ pancwl_rc]$ oc exec -n metallb-system  speaker-dlrn5 -c frr -- vtysh -c "show running-config"
Building configuration...

Current configuration:
!
frr version 8.3.1
frr defaults traditional
hostname gateway2.panclypcwl01.mnc020.mcc714
log file /etc/frr/frr.log informational
log timestamp precision 3
service integrated-vtysh-config
!
router bgp 4200000320
 no bgp ebgp-requires-policy
 no bgp default ipv4-unicast
 no bgp network import-check
 neighbor 10.85.187.34 remote-as 4200000320
 neighbor 10.85.187.34 bfd
 neighbor 10.85.187.34 bfd profile ncp-metallb-oam-pa-sv-bfd-profile
 neighbor 10.85.187.34 timers 30 90
 neighbor 10.85.187.35 remote-as 4200000320
 neighbor 10.85.187.35 bfd
 neighbor 10.85.187.35 bfd profile ncp-metallb-oam-pa-sv-bfd-profile
 neighbor 10.85.187.35 timers 30 90
 neighbor 10.86.10.98 remote-as 4200000320
 neighbor 10.86.10.98 bfd
 neighbor 10.86.10.98 bfd profile ncp-metallb-oam-pa-ni-bfd-profile
 neighbor 10.86.10.98 timers 30 90
 neighbor 10.86.10.99 remote-as 4200000320
 neighbor 10.86.10.99 bfd
 neighbor 10.86.10.99 bfd profile ncp-metallb-oam-pa-ni-bfd-profile
 neighbor 10.86.10.99 timers 30 90
 neighbor 10.89.97.162 remote-as 4200000320
 neighbor 10.89.97.162 bfd
 neighbor 10.89.97.162 bfd profile ncp-metallb-oam-pa-pa-bfd-profile
 neighbor 10.89.97.162 timers 30 90
 neighbor 10.89.97.163 remote-as 4200000320
 neighbor 10.89.97.163 bfd
 neighbor 10.89.97.163 bfd profile ncp-metallb-oam-pa-pa-bfd-profile
 neighbor 10.89.97.163 timers 30 90
 neighbor 10.89.147.194 remote-as 4200000320
 neighbor 10.89.147.194 bfd
 neighbor 10.89.147.194 bfd profile ncp-metallb-oam-pa-hn-bfd-profile
 neighbor 10.89.147.194 timers 30 90
 neighbor 10.89.147.195 remote-as 4200000320
 neighbor 10.89.147.195 bfd
 neighbor 10.89.147.195 bfd profile ncp-metallb-oam-pa-hn-bfd-profile
 neighbor 10.89.147.195 timers 30 90
 !
 address-family ipv4 unicast
  network 10.89.97.210/32
  neighbor 10.85.187.34 activate
  neighbor 10.85.187.34 route-map 10.85.187.34-in in
  neighbor 10.85.187.34 route-map 10.85.187.34-out out
  neighbor 10.85.187.35 activate
  neighbor 10.85.187.35 route-map 10.85.187.35-in in
  neighbor 10.85.187.35 route-map 10.85.187.35-out out
  neighbor 10.86.10.98 activate
  neighbor 10.86.10.98 route-map 10.86.10.98-in in
  neighbor 10.86.10.98 route-map 10.86.10.98-out out
  neighbor 10.86.10.99 activate
  neighbor 10.86.10.99 route-map 10.86.10.99-in in
  neighbor 10.86.10.99 route-map 10.86.10.99-out out
  neighbor 10.89.97.162 activate
  neighbor 10.89.97.162 route-map 10.89.97.162-in in
  neighbor 10.89.97.162 route-map 10.89.97.162-out out
  neighbor 10.89.97.163 activate
  neighbor 10.89.97.163 route-map 10.89.97.163-in in
  neighbor 10.89.97.163 route-map 10.89.97.163-out out
  neighbor 10.89.147.194 activate
  neighbor 10.89.147.194 route-map 10.89.147.194-in in
  neighbor 10.89.147.194 route-map 10.89.147.194-out out
  neighbor 10.89.147.195 activate
  neighbor 10.89.147.195 route-map 10.89.147.195-in in
  neighbor 10.89.147.195 route-map 10.89.147.195-out out
 exit-address-family
 !
 address-family ipv6 unicast
  neighbor 10.85.187.34 activate
  neighbor 10.85.187.34 route-map 10.85.187.34-in in
  neighbor 10.85.187.34 route-map 10.85.187.34-out out
  neighbor 10.85.187.35 activate
  neighbor 10.85.187.35 route-map 10.85.187.35-in in
  neighbor 10.85.187.35 route-map 10.85.187.35-out out
  neighbor 10.86.10.98 activate
  neighbor 10.86.10.98 route-map 10.86.10.98-in in
  neighbor 10.86.10.98 route-map 10.86.10.98-out out
  neighbor 10.86.10.99 activate
  neighbor 10.86.10.99 route-map 10.86.10.99-in in
  neighbor 10.86.10.99 route-map 10.86.10.99-out out
  neighbor 10.89.97.162 activate
  neighbor 10.89.97.162 route-map 10.89.97.162-in in
  neighbor 10.89.97.162 route-map 10.89.97.162-out out
  neighbor 10.89.97.163 activate
  neighbor 10.89.97.163 route-map 10.89.97.163-in in
  neighbor 10.89.97.163 route-map 10.89.97.163-out out
  neighbor 10.89.147.194 activate
  neighbor 10.89.147.194 route-map 10.89.147.194-in in
  neighbor 10.89.147.194 route-map 10.89.147.194-out out
  neighbor 10.89.147.195 activate
  neighbor 10.89.147.195 route-map 10.89.147.195-in in
  neighbor 10.89.147.195 route-map 10.89.147.195-out out
 exit-address-family
exit
!
ip prefix-list 10.89.97.162-pl-ipv4 seq 1 permit 10.89.97.210/32
ip prefix-list 10.89.97.163-pl-ipv4 seq 1 permit 10.89.97.210/32
ip prefix-list 10.85.187.34-pl-ipv4 seq 1 deny any
ip prefix-list 10.85.187.35-pl-ipv4 seq 1 deny any
ip prefix-list 10.86.10.98-pl-ipv4 seq 1 deny any
ip prefix-list 10.86.10.99-pl-ipv4 seq 1 deny any
ip prefix-list 10.89.147.194-pl-ipv4 seq 1 deny any
ip prefix-list 10.89.147.195-pl-ipv4 seq 1 deny any
!
ipv6 prefix-list 10.89.97.162-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.89.97.163-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.85.187.34-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.85.187.35-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.86.10.98-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.86.10.99-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.89.147.194-pl-ipv4 seq 2 deny any
ipv6 prefix-list 10.89.147.195-pl-ipv4 seq 2 deny any
!
route-map 10.85.187.34-in deny 20
exit
!
route-map 10.85.187.34-out permit 1
 match ip address prefix-list 10.85.187.34-pl-ipv4
exit
!
route-map 10.85.187.34-out permit 2
 match ipv6 address prefix-list 10.85.187.34-pl-ipv4
exit
!
route-map 10.85.187.35-in deny 20
exit
!
route-map 10.85.187.35-out permit 1
 match ip address prefix-list 10.85.187.35-pl-ipv4
exit
!
route-map 10.85.187.35-out permit 2
 match ipv6 address prefix-list 10.85.187.35-pl-ipv4
exit
!
route-map 10.86.10.98-in deny 20
exit
!
route-map 10.86.10.98-out permit 1
 match ip address prefix-list 10.86.10.98-pl-ipv4
exit
!
route-map 10.86.10.98-out permit 2
 match ipv6 address prefix-list 10.86.10.98-pl-ipv4
exit
!
route-map 10.86.10.99-in deny 20
exit
!
route-map 10.86.10.99-out permit 1
 match ip address prefix-list 10.86.10.99-pl-ipv4
exit
!
route-map 10.86.10.99-out permit 2
 match ipv6 address prefix-list 10.86.10.99-pl-ipv4
exit
!
route-map 10.89.147.194-in deny 20
exit
!
route-map 10.89.147.194-out permit 1
 match ip address prefix-list 10.89.147.194-pl-ipv4
exit
!
route-map 10.89.147.194-out permit 2
 match ipv6 address prefix-list 10.89.147.194-pl-ipv4
exit
!
route-map 10.89.147.195-in deny 20
exit
!
route-map 10.89.147.195-out permit 1
 match ip address prefix-list 10.89.147.195-pl-ipv4
exit
!
route-map 10.89.147.195-out permit 2
 match ipv6 address prefix-list 10.89.147.195-pl-ipv4
exit
!
route-map 10.89.97.162-in deny 20
exit
!
route-map 10.89.97.162-out permit 1
 match ip address prefix-list 10.89.97.162-pl-ipv4
exit
!
route-map 10.89.97.162-out permit 2
 match ipv6 address prefix-list 10.89.97.162-pl-ipv4
exit
!
route-map 10.89.97.163-in deny 20
exit
!
route-map 10.89.97.163-out permit 1
 match ip address prefix-list 10.89.97.163-pl-ipv4
exit
!
route-map 10.89.97.163-out permit 2
 match ipv6 address prefix-list 10.89.97.163-pl-ipv4
exit
!
ip nht resolve-via-default
!
ipv6 nht resolve-via-default
!
bfd
 profile ncp-metallb-oam-pa-hn-bfd-profile
  passive-mode
 exit
 !
 profile ncp-metallb-oam-pa-ni-bfd-profile
  passive-mode
 exit
 !
 profile ncp-metallb-oam-pa-pa-bfd-profile
  passive-mode
 exit
 !
 profile ncp-metallb-oam-pa-sv-bfd-profile
  passive-mode
 exit
 !
exit
!
end
[root@ncputility ~ pancwl_rc]$ oc exec -n metallb-system  speaker-dlrn5 -c frr -- vtysh -c "show bgp summary"

IPv4 Unicast Summary (VRF default):
BGP router identifier 172.16.2.2, local AS number 4200000320 vrf-id 0
BGP table version 1
RIB entries 1, using 192 bytes of memory
Peers 8, using 5788 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt Desc
10.85.187.34    4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.85.187.35    4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.86.10.98     4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.86.10.99     4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.89.97.162    4 4200000320      7306      7307        0    0    0 2d12h50m            0        1 N/A
10.89.97.163    4 4200000320      7305      7307        0    0    0 2d12h50m            0        1 N/A
10.89.147.194   4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.89.147.195   4 4200000320         0         0        0    0    0    never       Active        0 N/A

Total number of neighbors 8

IPv6 Unicast Summary (VRF default):
BGP router identifier 172.16.2.2, local AS number 4200000320 vrf-id 0
BGP table version 0
RIB entries 0, using 0 bytes of memory
Peers 8, using 5788 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt Desc
10.85.187.34    4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.85.187.35    4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.86.10.98     4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.86.10.99     4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.89.97.162    4 4200000320      7306      7307        0    0    0 2d12h50m        NoNeg    NoNeg N/A
10.89.97.163    4 4200000320      7305      7307        0    0    0 2d12h50m        NoNeg    NoNeg N/A
10.89.147.194   4 4200000320         0         0        0    0    0    never       Active        0 N/A
10.89.147.195   4 4200000320         0         0        0    0    0    never       Active        0 N/A

Total number of neighbors 8
[root@ncputility ~ pancwl_rc]$ oc exec -n metallb-system  speaker-dlrn5 -c frr -- vtysh -c "show bfd peers brief"
Session count: 2
SessionId  LocalAddress                             PeerAddress                             Status
=========  ============                             ===========                             ======
62069252   10.89.97.165                             10.89.97.162                            down
3159552171 10.89.97.165                             10.89.97.163                            down
[root@ncputility ~ pancwl_rc]$ oc exec -n metallb-system  speaker-dlrn5 -c frr -- vtysh -c "show bfd peer"
BFD Peers:
        peer 10.89.97.162 local-address 10.89.97.165 vrf default interface vlan104
                ID: 62069252
                Remote ID: 0
                Passive mode
                Status: down
                Downtime: 2 day(s), 10 hour(s), 3 minute(s), 16 second(s)
                Diagnostics: ok
                Remote diagnostics: ok
                Peer Type: dynamic
                Local timers:
                        Detect-multiplier: 3
                        Receive interval: 300ms
                        Transmission interval: 300ms
                        Echo receive interval: 50ms
                        Echo transmission interval: disabled
                Remote timers:
                        Detect-multiplier: 3
                        Receive interval: 1000ms
                        Transmission interval: 1000ms
                        Echo receive interval: disabled

        peer 10.89.97.163 local-address 10.89.97.165 vrf default interface vlan104
                ID: 3159552171
                Remote ID: 0
                Passive mode
                Status: down
                Downtime: 2 day(s), 10 hour(s), 3 minute(s), 16 second(s)
                Diagnostics: ok
                Remote diagnostics: ok
                Peer Type: dynamic
                Local timers:
                        Detect-multiplier: 3
                        Receive interval: 300ms
                        Transmission interval: 300ms
                        Echo receive interval: 50ms
                        Echo transmission interval: disabled
                Remote timers:
                        Detect-multiplier: 3
                        Receive interval: 1000ms
                        Transmission interval: 1000ms
                        Echo receive interval: disabled

[root@ncputility ~ pancwl_rc]$ oc exec -n metallb-system  speaker-dlrn5 -c frr -- vtysh -c "show ip bgp neighbors"
BGP neighbor is 10.85.187.34, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.85.187.34-in
  Route map for outgoing advertisements is *10.85.187.34-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.85.187.34-in
  Route map for outgoing advertisements is *10.85.187.34-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

BGP neighbor is 10.85.187.35, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.85.187.35-in
  Route map for outgoing advertisements is *10.85.187.35-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.85.187.35-in
  Route map for outgoing advertisements is *10.85.187.35-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

BGP neighbor is 10.86.10.98, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.86.10.98-in
  Route map for outgoing advertisements is *10.86.10.98-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.86.10.98-in
  Route map for outgoing advertisements is *10.86.10.98-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

BGP neighbor is 10.86.10.99, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.86.10.99-in
  Route map for outgoing advertisements is *10.86.10.99-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.86.10.99-in
  Route map for outgoing advertisements is *10.86.10.99-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

BGP neighbor is 10.89.97.162, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 10.29.90.34, local router ID 172.16.2.2
  BGP state = Established, up for 2d12h53m
  Last read 00:00:00, Last write 00:00:03
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Neighbor capabilities:
    4 Byte AS: advertised and received
    Extended Message: advertised
    AddPath:
      IPv4 Unicast: RX advertised
      IPv6 Unicast: RX advertised
    Long-lived Graceful Restart: advertised
    Route refresh: advertised and received(new)
    Enhanced Route Refresh: advertised
    Address Family IPv4 Unicast: advertised and received
    Address Family IPv6 Unicast: advertised
    Hostname Capability: advertised (name: gateway2.panclypcwl01.mnc020.mcc714,domain name: n/a) not received
    Graceful Restart Capability: advertised and received
      Remote Restart timer is 300 seconds
      Address families by peer:
        none
  Graceful restart information:
    End-of-RIB send: IPv4 Unicast
    End-of-RIB received: IPv4 Unicast
    Local GR Mode: Helper*
    Remote GR Mode: Helper
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 300
    IPv4 Unicast:
      F bit: False
      End-of-RIB sent: Yes
      End-of-RIB sent after update: Yes
      End-of-RIB received: Yes
      Timers:
        Configured Stale Path Time(sec): 360
    IPv6 Unicast:
      F bit: False
      End-of-RIB sent: No
      End-of-RIB sent after update: No
      End-of-RIB received: No
      Timers:
        Configured Stale Path Time(sec): 360
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  3          1
    Notifications:          0          0
    Updates:                2          2
    Keepalives:          7307       7308
    Route Refresh:          0          0
    Capability:             0          0
    Total:               7312       7311
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Update group 3, subgroup 3
  Packet Queue length 0
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.97.162-in
  Route map for outgoing advertisements is *10.89.97.162-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.97.162-in
  Route map for outgoing advertisements is *10.89.97.162-out
  0 accepted prefixes

  Connections established 1; dropped 0
  Last reset 2d12h55m,  Waiting for peer OPEN
Local host: 10.89.97.165, Local port: 37680
Foreign host: 10.89.97.162, Foreign port: 179
Nexthop: 10.89.97.165
Nexthop global: ::
Nexthop local: ::
BGP connection: shared network
BGP Connect Retry Timer in Seconds: 120
Read thread: on  Write thread: on  FD used: 26

  BFD: Type: single hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Down, Last update: 2:10:03:42

BGP neighbor is 10.89.97.163, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 10.29.90.38, local router ID 172.16.2.2
  BGP state = Established, up for 2d12h53m
  Last read 00:00:29, Last write 00:00:03
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Neighbor capabilities:
    4 Byte AS: advertised and received
    Extended Message: advertised
    AddPath:
      IPv4 Unicast: RX advertised
      IPv6 Unicast: RX advertised
    Long-lived Graceful Restart: advertised
    Route refresh: advertised and received(new)
    Enhanced Route Refresh: advertised
    Address Family IPv4 Unicast: advertised and received
    Address Family IPv6 Unicast: advertised
    Hostname Capability: advertised (name: gateway2.panclypcwl01.mnc020.mcc714,domain name: n/a) not received
    Graceful Restart Capability: advertised and received
      Remote Restart timer is 300 seconds
      Address families by peer:
        none
  Graceful restart information:
    End-of-RIB send: IPv4 Unicast
    End-of-RIB received: IPv4 Unicast
    Local GR Mode: Helper*
    Remote GR Mode: Helper
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 300
    IPv4 Unicast:
      F bit: False
      End-of-RIB sent: Yes
      End-of-RIB sent after update: Yes
      End-of-RIB received: Yes
      Timers:
        Configured Stale Path Time(sec): 360
    IPv6 Unicast:
      F bit: False
      End-of-RIB sent: No
      End-of-RIB sent after update: No
      End-of-RIB received: No
      Timers:
        Configured Stale Path Time(sec): 360
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  3          1
    Notifications:          0          0
    Updates:                2          1
    Keepalives:          7307       7307
    Route Refresh:          0          0
    Capability:             0          0
    Total:               7312       7309
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Update group 4, subgroup 4
  Packet Queue length 0
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.97.163-in
  Route map for outgoing advertisements is *10.89.97.163-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.97.163-in
  Route map for outgoing advertisements is *10.89.97.163-out
  0 accepted prefixes

  Connections established 1; dropped 0
  Last reset 2d12h55m,  Waiting for peer OPEN
Local host: 10.89.97.165, Local port: 54688
Foreign host: 10.89.97.163, Foreign port: 179
Nexthop: 10.89.97.165
Nexthop global: ::
Nexthop local: ::
BGP connection: shared network
BGP Connect Retry Timer in Seconds: 120
Read thread: on  Write thread: on  FD used: 25

  BFD: Type: single hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Down, Last update: 2:10:03:42

BGP neighbor is 10.89.147.194, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.147.194-in
  Route map for outgoing advertisements is *10.89.147.194-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.147.194-in
  Route map for outgoing advertisements is *10.89.147.194-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

BGP neighbor is 10.89.147.195, remote AS 4200000320, local AS 4200000320, internal link
  BGP version 4, remote router ID 0.0.0.0, local router ID 172.16.2.2
  BGP state = Active
  Last read 2d10h03m, Last write never
  Hold time is 90, keepalive interval is 30 seconds
  Configured hold time is 90, keepalive interval is 30 seconds
  Configured conditional advertisements interval is 60 seconds
  Graceful restart information:
    Local GR Mode: Helper*
    Remote GR Mode: NotApplicable
    R bit: False
    N bit: False
    Timers:
      Configured Restart Time(sec): 120
      Received Restart Time(sec): 0
  Message statistics:
    Inq depth is 0
    Outq depth is 0
                         Sent       Rcvd
    Opens:                  0          0
    Notifications:          0          0
    Updates:                0          0
    Keepalives:             0          0
    Route Refresh:          0          0
    Capability:             0          0
    Total:                  0          0
  Minimum time between advertisement runs is 0 seconds

 For address family: IPv4 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.147.195-in
  Route map for outgoing advertisements is *10.89.147.195-out
  0 accepted prefixes

 For address family: IPv6 Unicast
  Not part of any update group
  Community attribute sent to this neighbor(all)
  Inbound path policy configured
  Outbound path policy configured
  Route map for incoming advertisements is *10.89.147.195-in
  Route map for outgoing advertisements is *10.89.147.195-out
  0 accepted prefixes

  Connections established 0; dropped 0
  Last reset 2d10h03m,  Waiting for peer OPEN
BGP Connect Retry Timer in Seconds: 120
Next connect timer due in 80 seconds
Read thread: off  Write thread: off  FD used: -1

  BFD: Type: multi hop
  Detect Multiplier: 3, Min Rx interval: 300, Min Tx interval: 300
  Status: Unknown, Last update: never

```

12. some more additional test to show the local testing here 

```
[root@ncputility ~ pancwl_rc]$ oc get svc -A -o wide |grep -i loadbalan
ncom01pan                                          ncom01pan-citm-ingress                                     LoadBalancer   172.20.138.133   10.89.97.210                           80:32432/TCP,443:32622/TCP,2309:30135/TCP         10d   app=citm-ingress,component=controller,release=ncom01pan-citm-ingress
[root@ncputility ~ pancwl_rc]$ nslookup 10.89.97.210
210.97.89.10.in-addr.arpa       name = ncom01.panclyncom01.mnc020.mcc714.

[root@ncputility ~ pancwl_rc]$ curl -k https://ncom01.panclyncom01.mnc020.mcc714/
^C
[root@ncputility ~ pancwl_rc]$ ip r get 10.89.97.210
10.89.97.210 via 10.89.100.65 dev br308 src 10.89.100.66 uid 0
    cache
[root@ncputility ~ pancwl_rc]$ tracepath 10.89.97.210
 1?: [LOCALHOST]                      pmtu 1500
 1:  _gateway                                              0.184ms
 1:  _gateway                                              0.290ms
 2:  no reply
 3:  10.89.97.129                                          0.284ms asymm  1
 4:  no reply
 5:  10.89.97.129                                          0.264ms asymm  1
 6:  no reply
 7:  10.89.97.129                                          0.281ms asymm  1
 8:  no reply
 9:  10.89.97.129                                          0.279ms asymm  1
10:  no reply
11:  10.89.97.129                                          0.269ms asymm  1
12:  no reply
13:  10.89.97.129                                          0.280ms asymm  1
14:  no reply
15:  10.89.97.129                                          0.234ms asymm  1
16:  no reply
17:  10.89.97.129                                          0.297ms asymm  1
18:  no reply
19:  10.89.97.129                                          0.328ms asymm  1
20:  no reply
21:  10.89.97.129                                          0.292ms asymm  1
22:  no reply
23:  10.89.97.129                                          0.336ms asymm  1
24:  no reply
25:  10.89.97.129                                          0.332ms asymm  1
26:  no reply
27:  10.89.97.129                                          0.330ms asymm  1
28:  no reply
29:  10.89.97.129                                          0.332ms asymm  1
^C
[root@ncputility ~ pancwl_rc]$ oc get -n metallb-system pods -l component=speaker -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP            NODE                                  NOMINATED NODE   READINESS GATES
speaker-dlrn5   6/6     Running   0          24d   10.89.96.18   gateway2.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-g2g77   6/6     Running   0          24d   10.89.96.19   gateway3.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-jzbw7   6/6     Running   0          24d   10.89.96.17   gateway1.panclypcwl01.mnc020.mcc714   <none>           <none>
speaker-pjstl   6/6     Running   0          24d   10.89.96.20   gateway4.panclypcwl01.mnc020.mcc714   <none>           <none>
[root@ncputility ~ pancwl_rc]$ oc -n metallb-system exec -it -c frr vtysh
error: you must specify at least one command for the container
[root@ncputility ~ pancwl_rc]$ oc -n metallb-system exec -it speaker-dlrn5 -c frr vtysh
kubectl exec [POD] [COMMAND] is DEPRECATED and will be removed in a future version. Use kubectl exec [POD] -- [COMMAND] instead.

Hello, this is FRRouting (version 8.3.1).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

gateway2.panclypcwl01.mnc020.mcc714# curl
% Unknown command: curl
gateway2.panclypcwl01.mnc020.mcc714# exit
[root@ncputility ~ pancwl_rc]$ oc debug -t node/gateway3.panclypcwl01.mnc020.mcc714
Temporary namespace openshift-debug-8j8fb is created for debugging node...
Starting pod/gateway3panclypcwl01mnc020mcc714-debug-qsrhj ...
To use host binaries, run `chroot /host`
Pod IP: 10.89.96.19
If you don't see a command prompt, try pressing enter.
sh-5.1# chroot /host
sh-5.1# ping 10.89.97.163
PING 10.89.97.163 (10.89.97.163) 56(84) bytes of data.
From 10.89.97.166 icmp_seq=1 Destination Host Unreachable
From 10.89.97.166 icmp_seq=2 Destination Host Unreachable
From 10.89.97.166 icmp_seq=3 Destination Host Unreachable
^C
--- 10.89.97.163 ping statistics ---
4 packets transmitted, 0 received, +3 errors, 100% packet loss, time 3090ms
pipe 3
sh-5.1# ping 10.89.97.162
PING 10.89.97.162 (10.89.97.162) 56(84) bytes of data.
From 10.89.97.166 icmp_seq=1 Destination Host Unreachable
From 10.89.97.166 icmp_seq=2 Destination Host Unreachable
From 10.89.97.166 icmp_seq=3 Destination Host Unreachable
From 10.89.97.166 icmp_seq=4 Destination Host Unreachable
^C
--- 10.89.97.162 ping statistics ---
5 packets transmitted, 0 received, +4 errors, 100% packet loss, time 4064ms
pipe 4
sh-5.1# ip r g 10.89.97.163
10.89.97.163 via 10.89.97.161 dev vlan104 src 10.89.97.166 uid 0
    cache
sh-5.1# ip r g 10.89.97.162
10.89.97.162 via 10.89.97.161 dev vlan104 src 10.89.97.166 uid 0
    cache
sh-5.1#  curl -k https://ncom01.panclyncom01.mnc020.mcc714/
<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,shrink-to-fit=no"><meta name="theme-color" content="#000000"><link rel="manifest" href="/manifest.json"><link rel="shortcut icon" href="/favicon.ico"><title>Nokia Cloud Operations Manager</title><link href="/static/css/27.2dbd0a91.chunk.css" rel="stylesheet"><link href="/static/css/main.167b01c4.chunk.css" rel="stylesheet"></head><body><noscript>You need to enable JavaScript to run this app.</noscript><div id="root"></div><script>!function(e){function t(t){for(var r,o,l=t[0],c=t[1],s=t[2],u=0,d=[];u<l.length;u++)o=l[u],Object.prototype.hasOwnProperty.call(n,o)&&n[o]&&d.push(n[o][0]),n[o]=0;for(r in c)Object.prototype.hasOwnProperty.call(c,r)&&(e[r]=c[r]);for(f&&f(t);d.length;)d.shift()();return i.push.apply(i,s||[]),a()}function a(){for(var e,t=0;t<i.length;t++){for(var a=i[t],r=!0,o=1;o<a.length;o++){var c=a[o];0!==n[c]&&(r=!1)}r&&(i.splice(t--,1),e=l(l.s=a[0]))}return e}var r={},o={25:0},n={25:0},i=[];function l(t){if(r[t])return r[t].exports;var a=r[t]={i:t,l:!1,exports:{}};return e[t].call(a.exports,a,a.exports,l),a.l=!0,a.exports}l.e=function(e){var t=[];o[e]?t.push(o[e]):0!==o[e]&&{2:1,5:1,6:1,7:1,8:1,11:1,12:1,13:1,14:1,15:1,16:1,17:1,18:1,19:1,20:1,21:1,22:1,26:1}[e]&&t.push(o[e]=new Promise((function(t,a){for(var r="static/css/"+({5:"[AlarmDetailsPage]",6:"[AlarmPage]",7:"[CatalogDetailsPage]",8:"[CatalogTablePage]",9:"[CloudFlowLogin]",10:"[CloudFlowLogout]",11:"[CsvExporterDetailsPage]",12:"[DashboardPage]",13:"[ExecutionDetailsPage]",14:"[JobDetailsPage]",15:"[JobsTablePage]",16:"[ManagedWorkloadsTablePage]",17:"[NSDetailsContainerPage]",18:"[OperationsDetailsPage]",19:"[ResourceCompositionDetailsPage]",20:"[ResourceCompositionsPage]",21:"[ResourcesTablePage]",22:"[VimDetailsPage]",23:"[loginPage]"}[e]||e)+"."+{0:"31d6cfe0",1:"31d6cfe0",2:"559272a8",3:"31d6cfe0",4:"31d6cfe0",5:"affca9cb",6:"affca9cb",7:"91932cb4",8:"bf9ba349",9:"31d6cfe0",10:"31d6cfe0",11:"a0ed0644",12:"b2dca462",13:"b77ab692",14:"4ca14441",15:"f59232c1",16:"c1e044f2",17:"398f0759",18:"d8693b3e",19:"7b4dfbce",20:"d9277a02",21:"03edf692",22:"b6690f64",23:"31d6cfe0",26:"4391d164",28:"31d6cfe0",29:"31d6cfe0"}[e]+".chunk.css",n=l.p+r,i=document.getElementsByTagName("link"),c=0;c<i.length;c++){var s=(f=i[c]).getAttribute("data-href")||f.getAttribute("href");if("stylesheet"===f.rel&&(s===r||s===n))return t()}var u=document.getElementsByTagName("style");for(c=0;c<u.length;c++){var f;if((s=(f=u[c]).getAttribute("data-href"))===r||s===n)return t()}var d=document.createElement("link");d.rel="stylesheet",d.type="text/css",d.onload=t,d.onerror=function(t){var r=t&&t.target&&t.target.src||n,i=new Error("Loading CSS chunk "+e+" failed.\n("+r+")");i.code="CSS_CHUNK_LOAD_FAILED",i.request=r,delete o[e],d.parentNode.removeChild(d),a(i)},d.href=n,document.getElementsByTagName("head")[0].appendChild(d)})).then((function(){o[e]=0})));var a=n[e];if(0!==a)if(a)t.push(a[2]);else{var r=new Promise((function(t,r){a=n[e]=[t,r]}));t.push(a[2]=r);var i,c=document.createElement("script");c.charset="utf-8",c.timeout=120,l.nc&&c.setAttribute("nonce",l.nc),c.src=function(e){return l.p+"static/js/"+({5:"[AlarmDetailsPage]",6:"[AlarmPage]",7:"[CatalogDetailsPage]",8:"[CatalogTablePage]",9:"[CloudFlowLogin]",10:"[CloudFlowLogout]",11:"[CsvExporterDetailsPage]",12:"[DashboardPage]",13:"[ExecutionDetailsPage]",14:"[JobDetailsPage]",15:"[JobsTablePage]",16:"[ManagedWorkloadsTablePage]",17:"[NSDetailsContainerPage]",18:"[OperationsDetailsPage]",19:"[ResourceCompositionDetailsPage]",20:"[ResourceCompositionsPage]",21:"[ResourcesTablePage]",22:"[VimDetailsPage]",23:"[loginPage]"}[e]||e)+"."+{0:"9ea1f8f1",1:"d7647e6d",2:"49e46739",3:"6bb32e31",4:"5066ed38",5:"3e390b6c",6:"88b37376",7:"e7438c70",8:"f547dc3b",9:"c157abf8",10:"c3c2011c",11:"62ea6190",12:"c002dc82",13:"f0d807bf",14:"cee9c63a",15:"737e42f0",16:"2aae2df5",17:"4a2ec46d",18:"4777a959",19:"f28d098b",20:"7e96e980",21:"abc77c4e",22:"9d55d492",23:"44757b03",26:"c04605d3",28:"52a01c15",29:"f0708fbb"}[e]+".chunk.js"}(e);var s=new Error;i=function(t){c.onerror=c.onload=null,clearTimeout(u);var a=n[e];if(0!==a){if(a){var r=t&&("load"===t.type?"missing":t.type),o=t&&t.target&&t.target.src;s.message="Loading chunk "+e+" failed.\n("+r+": "+o+")",s.name="ChunkLoadError",s.type=r,s.request=o,a[1](s)}n[e]=void 0}};var u=setTimeout((function(){i({type:"timeout",target:c})}),12e4);c.onerror=c.onload=i,document.head.appendChild(c)}return Promise.all(t)},l.m=e,l.c=r,l.d=function(e,t,a){l.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:a})},l.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},l.t=function(e,t){if(1&t&&(e=l(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var a=Object.create(null);if(l.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)l.d(a,r,function(t){return e[t]}.bind(null,r));return a},l.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return l.d(t,"a",t),t},l.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},l.p="/",l.oe=function(e){throw console.error(e),e};var c=this.webpackJsonpfrontend=this.webpackJsonpfrontend||[],s=c.push.bind(c);c.push=t,c=c.slice();for(var u=0;u<c.length;u++)t(c[u]);var f=s;a()}([])</script><script src="/static/js/27.08ffca3e.chunk.js"></script><script src="/static/js/main.90334f28.chunk.js"></script></body></html>sh-5.1#

```