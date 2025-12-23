#!/bin/bash

set -euo pipefail

# === Configuration Variables ===
gitserverns="ncd-git"
gitdbns="ncd-db"
gitcburns="ncd-cbur"
chartlocation="/root/ncd/NCD_24.9_Git_Server_ORB-RC/ncd-git-server-product/helmcharts/"
sftpip="10.203.197.23"
sftpusername="gitserver01"
sftppasswd="redhat"
# ======= building variables =================

cbururl=$(oc get route -n ${gitcburns}|grep -i cbur-ingress|awk '{print "http://"$2$3}')


helm backup -n ${gitserverns} -a none -t ncd-git -x ${cbururl}


#=============creating a user id here========================

id -u "$sftpusername" >/dev/null 2>&1 || { sudo useradd -m "$sftpusername" && echo "$sftppasswd" | sudo passwd --stdin "$sftpusername"; }



echo "display the toolbox on gitserver"

oc -n ${gitserverns} get brpolices.cbur.csf.nokia.com ncd-git-toolbox

echo "Cbur backup of git server status here !!!"

oc -n ${gitserverns} get brpolices.cbur.csf.nokia.com ncd-git-toolbox -o yaml 


mkdir -p /home/${sftpusername}/.ssh
oc get secret -n ${gitcburns} cburm-ssh-public-key -o jsonpath={.data.ssh_public_key} | base64 -d > /home/${sftpusername}/.ssh/authorized_keys
chown -R ${sftpusername}:${sftpusername} /home/${sftpusername}/.ssh
chmod 600 /home/${sftpusername}/.ssh/authorized_keys




echo "Creating remote backup on NCD git"

oc create secret generic bastionhostpan \
  --namespace=${gitcburns} \
  --from-literal=port="22" \
  --from-literal=host="${sftpip}" \
  --from-literal=mode="sftp" \
  --from-literal=username="${sftpusername}" \
  --from-literal=path="/home/${sftpusername}/" \
  --from-literal=strictHostKeyChecking="no" \
  --from-literal=hostKey="" 


echo "update on the git cbur side."

helm get values ncd-cbur -n ${gitcburns} > rr.yaml


helm upgrade ncd-cbur -n ${gitcburns} ${chartlocation}/cbur-1.18.1.tgz -f rr.yaml --debug

