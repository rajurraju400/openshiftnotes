import argparse
import subprocess
import sys

def run_command(command):
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(e.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Run OpenShift and Quay diagnostic commands"
    )

    # hub vs spoke cannot be combined
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--hub",
        action="store_true",
        help="Run commands for hub cluster"
    )
    group.add_argument(
        "--spoke",
        action="store_true",
        help="Run commands for spoke cluster"
    )

    parser.add_argument(
        "--infra-quay",
        action="store_true",
        help="Run commands for Quay infrastructure health"
    )
    args = parser.parse_args()

    # If no arguments passed, show usage examples and exit
    if not (args.hub or args.spoke or args.infra_quay):
        print("""
Usage: python ocp_health_check.py [OPTIONS]

Options:
  --hub         Run diagnostics for hub cluster            (mutually exclusive with --spoke)
  --spoke       Run diagnostics for spoke cluster          (mutually exclusive with --hub)
  --infra-quay  Run diagnostics for Quay infrastructure    (can be combined with --hub or --spoke)

Examples:
  python ocp_health_check.py --hub
  python ocp_health_check.py --spoke
  python ocp_health_check.py --infra-quay
  python ocp_health_check.py --hub --infra-quay
  python ocp_health_check.py --spoke --infra-quay
""")
        sys.exit(1)

    # Base commands (common for hub/spoke clusters)
    base_commands = [
        "oc whoami --show-server",

    ]

    # Hub-specific commands
    hub_commands = [
        "oc get clusterversion",
        "oc get nodes -o wide",
        "oc get bmh -A",
        "oc get agent -A -o wide",
        "oc get infraenv -A",
        "oc get preprovisioningimage -A",
        "oc get hostfirmwarecomponents -A",
        "oc get hostfirmwaresettings -A",
        "oc get nmstateconfig -A",
        "oc get machine -A",
        "oc get mcp",
        "oc get co",
        "oc get pods -A -o wide",
        "oc get deployments -A",
        "oc get sts -A",
        "oc get ds -A",
        "oc get operators -A",
        "helm ls -A",
        "oc get cs",
        "oc get --raw='/readyz?verbose'",
        "oc get etcd -o=jsonpath='{.items[0].status.conditions[?(@.type==\"EtcdMembersAvailable\")].message}'",
        "oc get networks.operator.openshift.io -o yaml | grep -A1 serviceNetwork",
        "oc get networks.operator.openshift.io -o yaml | grep -A1 clusterNetwork",
        "oc get pods -n openshift-machine-api",
        "oc get pods -A | grep -i multus",
        "oc get pods -n openshift-image-registry",
        "oc get pods -n openshift-marketplace",
        "oc get operatorhub -o yaml | grep disableAllDefaultSources",
        "oc get catalogsource -n openshift-marketplace",
        "oc get catalogsource -A",
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config",
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph osd tree -c /var/lib/rook/openshift-storage/openshift-storage.config",
        # secure boot enable - validation
        
        """
         for i in $(oc get nodes --no-headers | awk '{print $1}'); do echo $i; oc debug node/$i -q -- chroot /host /bin/bash -c "mokutil --sb-state" ; done
        """,

        # Node diagnostics loop
        """
        for i in $(oc get nodes -o custom-columns=NAME:.metadata.name --no-headers); do
            echo ">>> Node: $i"
            oc debug node/$i -- bash -c 'chroot /host bash -c "uname -a; cat /etc/resolv.conf; timedatectl status; chronyc tracking; chronyc sources"' || echo "Failed on $i"
            echo "---------------------------------------------"
        done
        """,
        # All Certificate expire check
        """
        echo -e "NAMESPACE\tNAME\tEXPIRY" && \
        oc get secret -A -o jsonpath='{range .items[?(@.type=="kubernetes.io/tls")]}{.metadata.namespace}{"\\t"}{.metadata.name}{"\\t"}{.data.tls\\.crt}{"\\n"}{end}' | \
        while IFS=$'\\t' read ns name cert; do \
        echo -en "$ns\\t$name\\t"; \
        [ -n "$cert" ] && echo "$cert" | base64 -d | openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//' || echo "NO CERT"; \
        done | column -t
         """,
    ]

    # Spoke-specific commands
    spoke_commands = [
        "oc get nodes --show-labels",
        "oc get bmh -A",
        "oc describe node | grep -i Capacity -A3 | grep -i hugepages-1Gi",
        "oc get csv -A | grep NMState",
        "oc get nmstate -A",
        "oc get nncp -A",
        "oc get nnce -A",
        "oc get csv -A | grep SR-IOV",
        "oc get sriovnetworknodepolicy -n openshift-sriov-network-operator",
        "oc auth can-i get SriovNetworkNodeState",
        "oc get csv -n metallb-system | grep -i MetalLB",
        "oc get metallb -A",
        "oc get operators -A",
        "oc get deployment -n metallb-system controller",
        "oc get daemonset -n metallb-system speaker",
        "oc get ipaddresspool -A",
        "oc get pod -n openshift-logging",
        "oc get pod -n openshift-numaresources",
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config",
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph osd tree -c /var/lib/rook/openshift-storage/openshift-storage.config",
        # MetalLB diagnostics
        "oc -n metallb-system exec -it $(oc get pods -n metallb-system | grep -i speaker | awk '{print $1}' | tail -1) -c frr -- vtysh -c 'show running-config'",
        "oc -n metallb-system exec -it $(oc get pods -n metallb-system | grep -i speaker | awk '{print $1}' | tail -1) -c frr -- vtysh -c 'show bfd peers brief'",

        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config",
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph osd tree -c /var/lib/rook/openshift-storage/openshift-storage.config",
        
        # egress configurations
        "oc get egressips.k8s.ovn.org",

        # secure boot enable - validation
        
        """
         for i in $(oc get nodes --no-headers | awk '{print $1}'); do echo $i; oc debug node/$i -q -- chroot /host /bin/bash -c "mokutil --sb-state" ; done
        """,

        # Node diagnostics loop
        """
        for i in $(oc get nodes -o custom-columns=NAME:.metadata.name --no-headers); do
            echo ">>> Node: $i"
            oc debug node/$i -- bash -c 'chroot /host bash -c "uname -a; cat /etc/resolv.conf; timedatectl status; chronyc tracking; chronyc sources"' || echo "Failed on $i"
            echo "---------------------------------------------"
        done
        """,
        # All Certificate expire check
        """
        echo -e "NAMESPACE\tNAME\tEXPIRY" && \
        oc get secret -A -o jsonpath='{range .items[?(@.type=="kubernetes.io/tls")]}{.metadata.namespace}{"\\t"}{.metadata.name}{"\\t"}{.data.tls\\.crt}{"\\n"}{end}' | \
        while IFS=$'\\t' read ns name cert; do \
        echo -en "$ns\\t$name\\t"; \
        [ -n "$cert" ] && echo "$cert" | base64 -d | openssl x509 -noout -enddate 2>/dev/null | sed 's/notAfter=//' || echo "NO CERT"; \
        done | column -t
         """,
    ]

    # Quay infra validation commands
    infra_quay_commands = [
        # Health checks
        "curl -k https://localhost:8443/health/instance",
        # Logs check
        "podman logs quay-redis | tail -n 5",
        # Verify ports
        "ss -lntp | grep 8443",
    ]

    commands_to_run = []

    # If either hub or spoke chosen, include base commands
    if args.hub or args.spoke:
        commands_to_run += base_commands
    if args.hub:
        commands_to_run += hub_commands
    if args.spoke:
        commands_to_run += spoke_commands
    if args.infra_quay:
        commands_to_run += infra_quay_commands

    for command in commands_to_run:
        print(f"\n--- Running Command ---\n{command.strip()}\n")
        run_command(command)

if __name__ == "__main__":
    main()
