
[root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup-location get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                  PROVIDER   BUCKET/PREFIX                                             PHASE       LAST VALIDATED                  ACCESS MODE   DEFAULT
velero-acm-backup-1   aws        acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero   Available   2025-05-01 18:20:42 +0000 UTC   ReadWrite     true
[root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                                            STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION      SELECTOR
acm-credentials-schedule-20250501180616         Completed   0        0          2025-05-01 18:06:17 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-managed-clusters-schedule-20250501180616    Completed   0        0          2025-05-01 18:06:18 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-resources-generic-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:20 +0000 UTC   4d        velero-acm-backup-1   cluster.open-cluster-management.io/backup
acm-resources-schedule-20250501180616           Completed   0        0          2025-05-01 18:06:29 +0000 UTC   4d        velero-acm-backup-1   !cluster.open-cluster-management.io/backup,!policy.open-cluste        r-management.io/root-policy
acm-validation-policy-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:30 +0000 UTC   23h       velero-acm-backup-1   <none>
[root@dom14npv101-infra-manager ~ hubrc]# oc -n open-cluster-management-backup exec -it velero-549fbfb95d-s966g -- ./velero backup get
Defaulted container "velero" out of: velero, openshift-velero-plugin (init), velero-plugin-for-aws (init)
NAME                                            STATUS      ERRORS   WARNINGS   CREATED                         EXPIRES   STORAGE LOCATION      SELECTOR
acm-credentials-schedule-20250501180616         Completed   0        0          2025-05-01 18:06:17 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-managed-clusters-schedule-20250501180616    Completed   0        0          2025-05-01 18:06:18 +0000 UTC   4d        velero-acm-backup-1   <none>
acm-resources-generic-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:20 +0000 UTC   4d        velero-acm-backup-1   cluster.open-cluster-management.io/backup
acm-resources-schedule-20250501180616           Completed   0        0          2025-05-01 18:06:29 +0000 UTC   4d        velero-acm-backup-1   !cluster.open-cluster-management.io/backup,!policy.open-cluste        r-management.io/root-policy
acm-validation-policy-schedule-20250501180616   Completed   0        0          2025-05-01 18:06:30 +0000 UTC   22h       velero-acm-backup-1   <none>
[root@dom14npv101-infra-manager ~ hubrc]# curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 67.2M  100 67.2M    0     0  20.2M      0  0:00:03  0:00:03 --:--:-- 20.2M
[root@dom14npv101-infra-manager ~ hubrc]# unzip awscliv2.zip
Archive:  awscliv2.zip
   creating: aws/
   creating: aws/dist/
  inflating: aws/install
  inflating: aws/README.md
  inflating: aws/THIRD_PARTY_LICENSES
   creating: aws/dist/awscli/
   creating: aws/dist/cryptography/
   creating: aws/dist/docutils/
   creating: aws/dist/lib-dynload/
  inflating: aws/dist/aws
  inflating: aws/dist/aws_completer
  inflating: aws/dist/libpython3.13.so.1.0
  inflating: aws/dist/_awscrt.abi3.so
  inflating: aws/dist/_cffi_backend.cpython-313-x86_64-linux-gnu.so
  inflating: aws/dist/_ruamel_yaml.cpython-313-x86_64-linux-gnu.so
  inflating: aws/dist/libz.so.1
  inflating: aws/dist/liblzma.so.5
  inflating: aws/dist/libbz2.so.1
  inflating: aws/dist/libffi.so.6
  inflating: aws/dist/libuuid.so.1


[root@dom14npv101-infra-manager ~ hubrc]# sudo ./aws/install
You can now run: /usr/local/bin/aws --version
[root@dom14npv101-infra-manager ~ hubrc]# aws --version
aws-cli/2.27.6 Python/3.13.2 Linux/5.14.0-427.13.1.el9_4.x86_64 exe/x86_64.rhel.9
[root@dom14npv101-infra-manager ~ hubrc]# 




root@dom14npv101-infra-manager ~ hubrc]# aws configure --profile oadp
AWS Access Key ID [None]: I35Rzin4xFf58GaCkJlC
AWS Secret Access Key [None]: vaimKLwBnO5glSe+f4AKgwJTtYEMOPMnfon540LZ
Default region name [None]:
Default output format [None]:
[root@dom14npv101-infra-manager ~ hubrc]# aws --endpoint-url $AWS_ENDPOINT_URL s3 ls s3://acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero/

SSL validation failed for https://s3-openshift-storage.apps.ncpvnpvmgt.pnwlab.nsn-rdnet.net:443/acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63?list-type=2&prefix=velero%2F&delimiter=%2F&encoding-type=url         [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1028)

[root@dom14npv101-infra-manager ~ hubrc]#
[root@dom14npv101-infra-manager ~ hubrc]# aws --endpoint-url "$AWS_ENDPOINT_URL" --no-verify-ssl s3 ls s3://acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero/
urllib3/connectionpool.py:1064: InsecureRequestWarning: Unverified HTTPS request is being made to host 's3-openshift-storage.apps.ncpvnpvmgt.pnwlab.nsn-rdnet.net'. Adding certificate verification is strongl        y advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
                           PRE backups/
[root@dom14npv101-infra-manager ~ hubrc]# aws --endpoint-url "$AWS_ENDPOINT_URL" --no-verify-ssl s3 ls s3://acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero/backups/
urllib3/connectionpool.py:1064: InsecureRequestWarning: Unverified HTTPS request is being made to host 's3-openshift-storage.apps.ncpvnpvmgt.pnwlab.nsn-rdnet.net'. Adding certificate verification is strongl        y advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
                           PRE acm-credentials-schedule-20250501180616/
                           PRE acm-managed-clusters-schedule-20250501180616/
                           PRE acm-resources-generic-schedule-20250501180616/
                           PRE acm-resources-schedule-20250501180616/
                           PRE acm-validation-policy-schedule-20250501180616/
[root@dom14npv101-infra-manager ~ hubrc]# aws --endpoint-url "$AWS_ENDPOINT_URL" --no-verify-ssl s3 ls s3://acm-backups-bcf1990d-0846-4a6d-8518-67db81ebee63/velero/backups/acm-credentials-schedule-202505011        80616/
urllib3/connectionpool.py:1064: InsecureRequestWarning: Unverified HTTPS request is being made to host 's3-openshift-storage.apps.ncpvnpvmgt.pnwlab.nsn-rdnet.net'. Adding certificate verification is strongl        y advised. See: https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
2025-05-01 18:06:18         29 acm-credentials-schedule-20250501180616-csi-volumesnapshotclasses.json.gz
2025-05-01 18:06:18         27 acm-credentials-schedule-20250501180616-csi-volumesnapshotcontents.json.gz
2025-05-01 18:06:18         29 acm-credentials-schedule-20250501180616-csi-volumesnapshots.json.gz
2025-05-01 18:06:18         27 acm-credentials-schedule-20250501180616-itemoperations.json.gz
2025-05-01 18:06:18      11604 acm-credentials-schedule-20250501180616-logs.gz
2025-05-01 18:06:18         29 acm-credentials-schedule-20250501180616-podvolumebackups.json.gz
2025-05-01 18:06:18        327 acm-credentials-schedule-20250501180616-resource-list.json.gz
2025-05-01 18:06:18         49 acm-credentials-schedule-20250501180616-results.gz
2025-05-01 18:06:18         27 acm-credentials-schedule-20250501180616-volumeinfo.json.gz
2025-05-01 18:06:18         29 acm-credentials-schedule-20250501180616-volumesnapshots.json.gz
2025-05-01 18:06:18      46601 acm-credentials-schedule-20250501180616.tar.gz
2025-05-01 18:06:18       4428 velero-backup.json
[root@dom14npv101-infra-manager ~ hubrc]#
