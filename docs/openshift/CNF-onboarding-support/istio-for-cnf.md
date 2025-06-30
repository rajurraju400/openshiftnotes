# Configure the Redhat ISTIO for CNF


## Creating meshroll and allow cnf namespace access istio.

1) 

[root@longb92bst01 ~ cwlcluster]# cat servicemeshmemberroll.yaml
apiVersion: maistra.io/v1
kind: ServiceMeshMemberRoll
metadata:
  name: default
  namespace: istio-system
spec:
  members:
    - longb92ncc01 # your application ns name.
[root@longb92bst01 ~ cwlcluster]#
[root@longb92bst01 ~ cwlcluster]#
[root@longb92bst01 ~ cwlcluster]#
[root@longb92bst01 ~ cwlcluster]# oc apply -f servicemeshmemberroll.yaml
servicemeshmemberroll.maistra.io/default created
[root@longb92bst01 ~ cwlcluster]#
[root@longb92bst01 ~ cwlcluster]#

istio-injection=disabled -> adding this label.