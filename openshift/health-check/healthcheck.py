import subprocess

# this script developed by venkatapathiraj.ravichandran.ext@nokia.com
# this can be used for millicom, tmobile, oneweb, charter customers alone.

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(e.stderr)
        

def main():
    # List of OpenShift commands to execute
    commands = [
        # Collecting general cluster information 
		"oc whoami --show-server",
        "oc get clusterversion",
        "oc get bmh -A",
        "oc get machine -A",
        "oc get nodes -o wide",
        "oc get nodes -o wide | grep -i master",
        "oc get mcp",
        "oc get co",
        "oc get ns",
        "oc get pods -A -o wide",
        "oc get deployments -A",
        "oc get sts -A",
        "oc get ds -A",
        "oc get cs",
        "oc get --raw='/readyz?verbose'",
        "oc get etcd -o=jsonpath='{.items[0].status.conditions[?(@.type==\"EtcdMembersAvailable\")].message}'",
        "oc get nodes -o wide",
        "oc get networks.operator.openshift.io -o yaml | grep -A1 serviceNetwork",
        "oc get networks.operator.openshift.io -o yaml | grep -A1 clusterNetwork",
        "oc get provisioning -o yaml | grep CIDR",
        
        #checking the list of apps, operators and its pods status
        "helm ls -A",
        "oc get pods -n openshift-ovn-kubernetes",
        "oc get pods -n openshift-machine-api",
        "oc get pods -A | grep -i multus",
        "oc get pods -A -o wide | grep -i where",
        "oc get po -n openshift-image-registry",
        "oc get po -n openshift-marketplace",
        "oc get operatorhub -o yaml | grep disableAllDefaultSources",
        "oc get catalogsource -n openshift-marketplace",
        "oc get catalogsource -A",
        
        # node specific configuration including the networking stuffs.
        "oc get nodes --show-labels | grep nodeType",
        "oc get nodes --show-labels | grep node-role.kubernetes.io",
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
        "oc get deployment -n metallb-system controller",
        "oc get daemonset -n metallb-system speaker",
        "oc get ipaddresspool -A",
        "oc get pod -n openshift-logging",
        "oc get pod -n openshift-numaresources",
        
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph -s -c /var/lib/rook/openshift-storage/openshift-storage.config",
        # Ceph health status
        "oc exec -it $(oc get pod -n openshift-storage -l app=rook-ceph-operator -o name) -n openshift-storage -- ceph osd tree -c /var/lib/rook/openshift-storage/openshift-storage.config",
        
        # egress configurations
        "oc get egressips.k8s.ovn.org",

        # MetalLB speaker config
        "oc -n metallb-system exec -it $(oc get pods -n metallb-system | grep -i speaker | awk '{print $1}' | tail -1) -c frr -- vtysh -c 'show running-config'",

        # MetalLB BFD peer status
        "oc -n metallb-system exec -it $(oc get pods -n metallb-system | grep -i speaker | awk '{print $1}' | tail -1) -c frr -- vtysh -c 'show bfd peers brief'",
        
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
        """
    ]

    # Run each command
    for command in commands:
        print(f"\n--- Running Command ---\n{command.strip()}\n")
        run_command(command)

if __name__ == "__main__":
    main()


