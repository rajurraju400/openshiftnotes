# Method to use nsenter on the OCP

> Please find the method to use nsenter, so that you will not struggle during your deployment. 

1. Login to the ocp cluster with cluster admin role and find the pod name which you want to login inside the container using nsenter. `ncom01pan-caas-plugin-9bd7755bb-bb5fs` is selected.


```
[root@ncputility ~ pancwl_rc]$ source /root/pancwlrc
WARNING: Using insecure TLS client config. Setting this option is not supported!

Login successful.

You have access to 119 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "ncom01pan".
[root@ncputility ~ pancwl_rc]$ oc get pods -A -o wide |grep -i ^C
[root@ncputility ~ pancwl_rc]$ oc get pods -n ncom01pan -o wide |grep -i caas
ncom01pan-caas-plugin-9bd7755bb-bb5fs                       1/1     Running             0          3h15m   172.17.18.34    appworker23.panclypcwl01.mnc020.mcc714   <none>           <none>
ncom01pan-caas-plugin-9bd7755bb-cwzmm                       1/1     Running             0          3h15m   172.18.8.78     appworker16.panclypcwl01.mnc020.mcc714   <none>           <none>
[root@ncputility ~ pancwl_rc]$
```

2. execute to that node where your pod hosted, and this will be indentified from the previous command. 
```
[root@ncputility ~ pancwl_rc]$ oc debug -t node/appworker0.panclypcwl01.mnc020.mcc714
Temporary namespace openshift-debug-vz9qc is created for debugging node...
Starting pod/appworker0panclypcwl01mnc020mcc714-debug-87f7l ...
To use host binaries, run `chroot /host`
Pod IP: 10.89.96.26
If you don't see a command prompt, try pressing enter.
sh-5.1# chroot /host
sh-5.1#
```

3. now find out the container id using crictl command here 
```
sh-5.1# crictl ps |grep -i ncom01pan-caas-plugin-7654b86fdb-mz5r7
2b61910d5eb23       quay-registry.apps.panclyphub01.mnc020.mcc714/ncom01pan/ncom/caas-plugin@sha256:d6d9506d14d756ecafe7d93debcb9eeb498cc805506fb1480002713d17ce64d6   19 minutes ago      Running             cjee-wildfly                         0                   8ca17869e45fa       ncom01pan-caas-plugin-7654b86fdb-mz5r7

```
4. find out the pid of the container using inspect command. 

```
sh-5.1# crictl inpsect 2b61910d5eb23 |grep -i pid
No help topic for 'inpsect'
sh-5.1# crictl inspect 2b61910d5eb23 |grep -i pid
    "pid": 60545,
          "pids": {
            "type": "pid"
                "getpid",
                "getppid",
                "pidfd_getfd",
                "pidfd_open",
                "pidfd_send_signal",
                "waitpid",
```

5. now use the toolbox command, since tcpdump is not configured on the host os level. 

```
sh-5.1# toolbox
.toolboxrc file detected, overriding defaults...
Checking if there is a newer version of quay-registry.apps.panclyphub01.mnc020.mcc714/ocmirror/rhel9/support-tools:latest available...
Container 'toolbox-root' already exists. Trying to start...
(To remove the container and start with a fresh toolbox, run: sudo podman rm 'toolbox-root')
toolbox-root
Container started successfully. To exit, type 'exit'.
[root@appworker0 /]# nsenter -t 60545 -n ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: gre0@NONE: <NOARP> mtu 1476 qdisc noop state DOWN group default qlen 1000
    link/gre 0.0.0.0 brd 0.0.0.0
3: gretap0@NONE: <BROADCAST,MULTICAST> mtu 1462 qdisc noop state DOWN group default qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
4: erspan0@NONE: <BROADCAST,MULTICAST> mtu 1450 qdisc noop state DOWN group default qlen 1000
    link/ether 00:00:00:00:00:00 brd ff:ff:ff:ff:ff:ff
5: ip6tnl0@NONE: <NOARP> mtu 1452 qdisc noop state DOWN group default qlen 1000
    link/tunnel6 :: brd :: permaddr 3eac:e266:df07::
6: ip6gre0@NONE: <NOARP> mtu 1448 qdisc noop state DOWN group default qlen 1000
    link/gre6 :: brd :: permaddr 6679:afbc:3648::
7: eth0@if609: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 8900 qdisc noqueue state UP group default
    link/ether 0a:58:ac:10:04:0f brd ff:ff:ff:ff:ff:ff link-netns d00bdece-6c79-4840-87d1-10d3103ecdd7
    inet 172.16.4.15/23 brd 172.16.5.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::858:acff:fe10:40f/64 scope link
       valid_lft forever preferred_lft forever
[root@appworker0 /]# nsenter -t 60545 -n ping  quay-registry.apps.panclyphub01.mnc020.mcc714
PING quay-registry.apps.panclyphub01.mnc020.mcc714 (10.89.97.143) 56(84) bytes of data.
From 10.89.97.168 (10.89.97.168) icmp_seq=1 Destination Host Unreachable
From 10.89.97.168 (10.89.97.168) icmp_seq=2 Destination Host Unreachable
From 10.89.97.168 (10.89.97.168) icmp_seq=3 Destination Host Unreachable
From 10.89.97.168 (10.89.97.168) icmp_seq=4 Destination Host Unreachable

^C
--- quay-registry.apps.panclyphub01.mnc020.mcc714 ping statistics ---
5 packets transmitted, 0 received, +4 errors, 100% packet loss, time 4089ms
pipe 4
[root@appworker0 /]# nsenter -t 60545 -n ping  10.89.97.143
PING 10.89.97.143 (10.89.97.143) 56(84) bytes of data.
From 10.89.97.168 icmp_seq=1 Destination Host Unreachable
From 10.89.97.168 icmp_seq=2 Destination Host Unreachable
From 10.89.97.168 icmp_seq=3 Destination Host Unreachable
From 10.89.97.168 icmp_seq=4 Destination Host Unreachable

^C
--- 10.89.97.143 ping statistics ---
4 packets transmitted, 0 received, +4 errors, 100% packet loss, time 3088ms
pipe 4
[root@appworker0 /]# nsenter -t 60545 -n tracepath 10.89.97.143
 1?: [LOCALHOST]                      pmtu 8900
 1:  *.apps.panclyphub01.mnc020.mcc714                     1.683ms asymm  2
 1:  *.apps.panclyphub01.mnc020.mcc714                     0.878ms asymm  2
 2:  100.88.0.7                                            1.903ms asymm  3
 3:  172.17.2.2                                            2.086ms
 4:  no reply
 4:  10.89.97.168                                        3087.371ms !H
     Resume: pmtu 8900
[root@appworker0 /]#
```