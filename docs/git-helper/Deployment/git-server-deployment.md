# Git Server Deployment Guide

This document outlines the steps required to deploy the Git Server and its associated services on an OpenShift-based infrastructure.

---

## 1. Create Required Namespaces

> Git required to create following three namespace/project

```bash
oc new-project paclypancdgit01
oc new-project paclypancddb01
oc new-project paclypancdcbur01
```



## 2. Set Security Context Constraints (SCC)

> this step is added only for the git project.

```bash
oc adm policy add-scc-to-group anyuid system:serviceaccounts:paclypancdgit01
```


## 3. Apply Pod Security Labels

```bash
oc label --overwrite ns paclypancdgit01 pod-security.kubernetes.io/enforce=baseline
oc label --overwrite ns paclypancddb01 pod-security.kubernetes.io/enforce=restricted
oc label --overwrite ns paclypancdcbur01 pod-security.kubernetes.io/enforce=restricted
```



## 4. Create Image Pull Secrets

> here the username and password should be used on the git hub registry.

```bash
# Git Namespace
oc create secret -n paclypancdgit01 docker-registry my-pull-secret   --docker-server=quay-registry.apps.panclyphub01.mnc020.mcc714   --docker-username=ncd01pan --docker-password=ncd01pan

# DB Namespace
oc create secret -n paclypancddb01 docker-registry my-pull-secret   --docker-server=quay-registry.apps.panclyphub01.mnc020.mcc714   --docker-username=ncd01pan --docker-password=ncd01pan

# CBUR Namespace
oc create secret -n paclypancdcbur01 docker-registry my-pull-secret   --docker-server=quay-registry.apps.panclyphub01.mnc020.mcc714   --docker-username=ncd01pan --docker-password=ncd01pan
```



## 5. Generate TLS Certificate for GitLab

> you can define the actual git url as /CN field.  example `gitlab.apps.panclyphub01.mnc020.mcc714`

```bash
openssl genrsa -out ca.key 2048

openssl req -x509 -new -nodes -key ca.key -days 3650   -reqexts v3_req -subj "/CN=gitlab.apps.panclyphub01.mnc020.mcc714"   -extensions v3_ca -out ca.crt
```



## 6. Deploy Helm Charts

### 6.1 CBUR CRDs

```bash
helm install cbur-crds -n paclypancdcbur01   /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/cbur-crds-2.6.0.tgz   -f cbur-crd.yaml
```

### 6.2 CBUR Product

```bash
helm install ncd-cbur -n paclypancdcbur01   /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/cbur-1.18.1.tgz   -f cbur.yaml --debug
```

### 6.3 PostgreSQL HA

```bash
helm install ncd-postgresql -n paclypancddb01   /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/postgresql-ha-24.9.1-1009.g19e2a92.tgz   -f post.yaml --debug --timeout 20m
```

### 6.4 Redis

```bash
helm install ncd-redis -n paclypancddb01   /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/ncd-redis-24.9.1-1009.g19e2a92.tgz   -f redis.yaml --debug --timeout 20m
```



## 7. Validate Pod SCC Annotations

```bash
oc get pods -n paclypancddb01   -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.annotations.openshift\.io/scc}{"\n"}{end}'
```



## 8. Deploy Git Server

```bash
helm install ncd-git -n paclypancdgit01   /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/ncd-git-server-24.9.1-7.g30f1acf.tgz   -f git.yaml --debug --timeout 20m
```



## Notes

- No changes are required in the values files: `cbur-crd.yaml`.
- update are improtant on  `cbur.yaml`, `post.yaml`, `redis.yaml`, and `git.yaml`.
- Ensure the registry, certificates, hosts, redis and postgress service hostnames are properly configured before deployment.


## Download the sample files

📄 [Click here to download sample](./denmarkfiles.tar)
