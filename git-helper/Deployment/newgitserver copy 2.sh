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
gitchartdir="/root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/INSTALL_MEDIA/"
gitcbururl="${gitcbur}.${domain}"
gitserverurl="${gitns}.${domain}"
pspqhost="ncd-postgresql-postgresql-ha-proxy.${gitdb}.svc.cluster.local"
redishost="ncd-redis-crdb-redisio.${gitdb}.svc.cluster.local"

crane auth login -u ${quayname} -p ${quaypasswd} ${quayurl}


/root/ncd/ncd24.9PP1/NCD_24.9_PP1_Full_ORB/ncd-product

/root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/INSTALL_MEDIA/image-uploader.sh -a --flatRegistry -r quay-registry.apps.hnevocphub01.mnc002.mcc708/ncd \
-s /root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/containerimages