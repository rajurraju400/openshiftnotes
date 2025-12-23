#!/bin/bash

set -euo pipefail

# === Configuration Variables ===
clustername="hnevocphub01"
gitns="hnevocpgit01"
gitdb="hnevocpdb01"
gitcbur="hnevocpcbur01"
quayurl="quay-registry.apps.hnevocphub01.mnc002.mcc708"
quayname="ncd01pan"
quaypasswd="ncd01pan"
domain="apps.hnevocphub01.mnc002.mcc708"
gitchartdir="/root/ncd/ncd24.9PP1/NCD_24.9_PP1_Full_ORB/ncd-product/helmcharts/"
gitcbururl="${gitcbur}.${domain}"
gitserverurl="${gitns}.${domain}"
pspqhost="ncd-postgresql-postgresql-ha-proxy.${gitdb}.svc.cluster.local"
redishost="ncd-redis-crdb-redisio.${gitdb}.svc.cluster.local"

# === Don't Change anything beyond this point ==="  

# === Functions ===

cleanup_dir() {
    echo "🧹 Cleaning up temporary files..."
    rm -f ca.crt ca.key *.yaml
}

create_namespaces() {
    echo "🚀 Creating namespaces..."
    for ns in "$gitns" "$gitdb" "$gitcbur"; do
        if oc get project "$ns" &>/dev/null; then
            echo "✅ Namespace '$ns' exists."
        else
            oc new-project "$ns" && echo "✅ Created '$ns'" || echo "❌ Failed to create '$ns'"
        fi
    done
}

add_scc_labels() {
    echo "🔐 Adding SCCs and labels..."
    oc adm policy add-scc-to-group anyuid "system:serviceaccounts:${gitns}"

    kubectl label --overwrite ns "${gitns}" pod-security.kubernetes.io/enforce=baseline
    kubectl label --overwrite ns "${gitdb}" pod-security.kubernetes.io/enforce=restricted
    kubectl label --overwrite ns "${gitcbur}" pod-security.kubernetes.io/enforce=restricted
}

create_pull_secrets() {
    echo "🔑 Creating pull secrets..."
    for ns in "$gitns" "$gitdb" "$gitcbur"; do
        oc create secret docker-registry my-pull-secret \
            --docker-server="${quayurl}" \
            --docker-username="${quayname}" \
            --docker-password="${quaypasswd}" \
            -n "$ns" \
            --dry-run=client -o yaml | oc apply -f -
    done
}

generate_cert() {
    echo "🔏 Generating self-signed cert..."
    openssl genrsa -out ca.key 2048
    openssl req -x509 -new -nodes -key ca.key -days 3650 \
        -subj "/CN=${gitserverurl}" \
        -extensions v3_ca -out ca.crt
    sleep 2
    export CA_CERT=$(<ca.crt)
    export CA_KEY=$(<ca.key)

}

prepare_values_files() {
    echo "📄 Copying value files if missing..."
    cp -n ./rawfiles/cbur-crd.yaml ./cbur-crd.yaml
}

update_allvaluesfile_yaml() {

    input_file="./rawfiles/cbur.yaml"
    output_file="cbur-updated.yaml"
    echo "🔧 Updating cbur.yaml..."
    sed -e "s|^\( *registry:\).*|\1 ${quayurl}/ncd|" \
        -e "s|^\( *- \"\)cbur\.apps\.[^\"]*\"|\1${gitcbururl}\"|" \
        -e "/^includeNamespaces:/,/^[^ ]/c\
includeNamespaces:\n  - ${gitns}\n  - ${gitdb}\n  - ${gitcbur}" \
        -e "s|clusterName: \"panclyphub01\"|clusterName: \"${clustername}\"|g" \
        "$input_file" > "$output_file"

    export CA_CERT=$(<ca.crt)
    export CA_KEY=$(<ca.key)
    input_file="./rawfiles/redis.yaml"
    output_file="redisupdated.yaml"
    yq eval '
.global.tls.certificates.certManager.certificateAuthorityPublicKey = strenv(CA_CERT) |
.global.tls.certificates.certManager.certificateAuthorityPrivateKey = strenv(CA_KEY)
' ${input_file} > ${output_file}
    sed -i "s|quay-registry.apps.panclyphub01.mnc020.mcc714|${quayurl}|g" ${output_file}
    
    export CA_CERT=$(<ca.crt)
    export CA_KEY=$(<ca.key)
    input_file="./rawfiles/post.yaml"
    output_file="postupdated.yaml"
    yq eval '
.tls.certificates.certificateAuthorityPublicKey = strenv(CA_CERT) |
.tls.certificates.certificateAuthorityPrivateKey = strenv(CA_KEY)
' ${input_file} > ${output_file}
    sed -i "s|quay-registry.apps.panclyphub01.mnc020.mcc714|${quayurl}|g" ${output_file}

    export CA_CERT=$(<ca.crt)
    export CA_KEY=$(<ca.key)
    input_file="./rawfiles/git.yaml"
    output_file="gitupdated.yaml"
    yq eval '
.tls.certificateAuthorityPublicKey = strenv(CA_CERT) |
.tls.certificateAuthorityPrivateKey = strenv(CA_KEY)
' ${input_file} > ${output_file}
    sed -i "s|quay-registry.apps.panclyphub01.mnc020.mcc714|${quayurl}|g" ${output_file}
    sed -i "s|domain: apps.panclyphub01.mnc020.mcc714|domain: ${domain}|g" ${output_file}
    sed -i "s|ncd-postgresql-postgresql-ha-proxy.paclypancddb01.svc.cluster.local|${pspqhost}|g" ${output_file}
    sed -i "s|ncd-redis-crdb-redisio.paclypancddb01.svc.cluster.local|${redishost}|g" ${output_file}

}

install_helm_charts() {
    echo "📦 Installing Helm charts..."
    helm install cbur-crds -n "${gitcbur}" "${gitchartdir}/cbur-crds-2.6.0.tgz" -f cbur-crd.yaml --debug
    helm install ncd-cbur -n "${gitcbur}" "${gitchartdir}/cbur-1.18.1.tgz" -f cbur-updated.yaml --debug
    helm install ncd-postgresql -n "${gitdb}" "${gitchartdir}/postgresql-ha-24.9.1-1009.g19e2a92.tgz" -f postupdated.yaml --debug --timeout 20m
    helm install ncd-redis -n "${gitdb}" "${gitchartdir}/ncd-redis-24.9.1-1009.g19e2a92.tgz" -f redisupdated.yaml --debug --timeout 20m
    helm upgrade ncd-git -n "${gitns}" "${gitchartdir}/ncd-git-server-24.9.1-7.g30f1acf.tgz" -f gitupdated.yaml --debug --timeout 20m
}

verify_sccs() {
    echo "🔍 Verifying SCCs in ${gitdb}..."
    oc get pods -n "${gitdb}" -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.openshift\.io/scc}{"\n"}{end}'
    echo "here is the details about GIT server ....."
    
}

rollback() {
    echo "🔄 Rolling back: Uninstalling Helm charts and deleting namespaces..."
    helm uninstall ncd-git -n "$gitns" || true
    helm uninstall ncd-redis -n "$gitdb" || true
    helm uninstall ncd-postgresql -n "$gitdb" || true
    helm uninstall ncd-cbur -n "$gitcbur" || true
    helm uninstall cbur-crds -n "$gitcbur" || true

    echo "🗑️ Deleting namespaces..."
    for ns in "$gitns" "$gitdb" "$gitcbur"; do
        oc delete ns "$ns" --ignore-not-found
    done

    cleanup_dir
    echo "✅ Rollback complete!"
}

# === Main Execution ===

if [[ "${1:-}" == "rollback" ]]; then
    rollback
else
    cleanup_dir
    create_namespaces
    add_scc_labels
    create_pull_secrets
    generate_cert
    prepare_values_files
    update_allvaluesfile_yaml
    install_helm_charts
    verify_sccs
    echo "✅ All components installed successfully!"
fi
