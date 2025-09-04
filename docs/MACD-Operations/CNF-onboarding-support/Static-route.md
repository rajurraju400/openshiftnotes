# Creating Routes on NCP (Egress and Backward Routes)

> This guide explains how to configure routes for **egress** and
> **ingress** requirements using **NNCP**.

------------------------------------------------------------------------

## Route Creation Overview

All static routes are created on the **gateway (GW) nodes** to handle
both:\
- **Ingress (backward routes):** for incoming traffic\
- **Egress (default egress routes):** for outgoing traffic

------------------------------------------------------------------------

## Ingress

Ingress traffic is managed through **MetalLB**. Applications expose
services with a **LoadBalancer IP**, which must be part of the MetalLB
configuration (`IPAddressPool`).

-   MetalLB configuration is located at:

        CWL-Cluster/site-policies/sites/hub/source-crs/metallb

### Flow Explanation

1.  MetalLB speaker pods advertise the **application LoadBalancer IP**
    to BGP peers.\
2.  BGP peers (on the switches) receive traffic destined for that IP.\
3.  The traffic is routed to the MetalLB speaker pod.\
4.  From there, Kubernetes iptables forwards it to the internal service
    cluster IP.\
5.  Finally, traffic is directed to the appropriate application pod
    endpoint.

Since speaker pods run on **GW nodes**, the GW nodes must have routes to
external client systems via the **MetalLB VLAN interface** (BGP subnet).

📌 In OCP, these ingress routes are called **backward routes** and are
defined under:

    CWL-Cluster/site-policies/sites/hub/source-crs/nmstate

------------------------------------------------------------------------

## Egress

Egress is needed when application pods communicate with external systems
(e.g., **NetAct**, **SFTP servers**, or **log servers**).

Egress configuration has two components:

1.  **EgressIP configuration** for the application namespace:

        CWL-Cluster/site-policies/sites/hub/source-crs/egressip/egressip.yaml

2.  **Default egress route configuration** (created via NNCP):

        CWL-Cluster/site-policies/sites/hub/source-crs/egressip/default_route_for_egress.yaml


### Flow Explanation

1) Application pods send traffic destined for external systems (e.g., NetAct, SFTP).

2) Kubernetes routes this traffic through the EgressIP assigned to the namespace.

3) The egress traffic exits via the GW node where the EgressIP is active.

4) On the GW node, the default egress route (NNCP) ensures that traffic is forwarded to the correct external next-hop. but this default route will be with metric as 999.  which is low priorty for worste case.  so you need to create additional site specific route with metric as 150. 

5) From there, the external network routes the traffic to the target system (e.g., NetAct/SFTP server).

6) Return traffic comes back via the same GW node using the EgressIP, maintaining session consistency.

This ensures controlled, predictable outbound traffic from applications to external systems.

------------------------------------------------------------------------

> With these configurations, ingress (backward routes) and egress routes are consistently managed across OCP deployments.
