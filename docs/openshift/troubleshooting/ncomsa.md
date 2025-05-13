## NCOM CAAS fluctuate every 1 hours once and here is the process to create a service account for ncom to resolve this issue. 

> Caas using user/passwd based registation is fluctuate

### Problem describe:  

* CAAS flucatuate on the ncom, CNF onboarding may fail. in millicom, 30mins once it;s fluctuate. 
> 
### Solution describe:

* The auto discovery mode NCOM uses a token after discovery to integrate with the workload cluster instead of userID/password. This connection appears to be stable and does not fluctuate. So ncom want to use this token based access as a solution to our problem. instead of user id based. 

###  limitation:  

* based on NCP security hardening, system token may expire within 24hrs. 



### Solution steps: 


1) You need to be logged in with a user who has cluster-admin privileges:

2) Create an service account on the desired project. 
```
[root@ncputility ~ pancwl_rc]$ oc project ncom01pan
Now using project "ncom01pan" on server "https://api.panclypcwl01.mnc020.mcc714:6443".
[root@ncputility ~ pancwl_rc]$ 

[root@ncputility ~ pancwl_rc]$ oc create serviceaccount ncom-sa
serviceaccount/ncom-sa created
[root@ncputility ~ pancwl_rc]$

```

3)  Assing `cluster-admin` role to this `SA` now. 

```
[root@ncputility ~ pancwl_rc]$ oc adm policy add-cluster-role-to-user cluster-admin -z  ncom-sa -n ncom01pan
clusterrole.rbac.authorization.k8s.io/cluster-admin added: "ncom-sa"
[root@ncputility ~ pancwl_rc]$ 
```
4) describe sa here, you wont see the token and it's expected on this version OCP. 

```
[root@ncputility ~ pancwl_rc]$ oc describe sa ncom-sa
Name:                ncom-sa
Namespace:           ncom01pan
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              <none>
Events:              <none>
[root@ncputility ~ pancwl_rc]$

```

5) Now Manually Create a Token for the ServiceAccount. This tells Kubernetes/OpenShift to generate a token for ncom-sa and store it in the secret ncom-sa-secret.


```
[root@ncputility ~ pancwl_rc]$ cat > secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ncom-sa-secret
  annotations:
    kubernetes.io/service-account.name: ncom-sa
type: kubernetes.io/service-account-token

[root@ncputility ~ pancwl_rc]$
```

6) describe sa here again. you can see the secret created. 

```
[root@ncputility ~ pancwl_rc]$ oc describe sa ncom-sa
Name:                ncom-sa
Namespace:           ncom01pan
Labels:              <none>
Annotations:         <none>
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              ncom-sa-secret
Events:              <none>
[root@ncputility ~ pancwl_rc]$
```

7) retrive the token and share with ncom team here

> `oc get secret ncom-sa-secret -n ncom01pan -o jsonpath="{.data.token}" | base64 -d`

```
 [root@ncputility ~ pancwl_rc]$ oc get secret ncom-sa-secret -n ncom01pan -o jsonpath="{.data.token}" | base64 -d

eyJhbGciOiJSUzI1NiIsImtpZCI6IjBpd2lFcjdSU3ktY25uRDl3YTVhU0M2V0wtZ0pUWXBXM0RzMmpUTFp1N28ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZX        Rlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJuY29tMDFwYW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlY3JldC5uYW1lIjoibmNvbS1zYS1zZWNyZXQiLCJrdWJlcm5        ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoibmNvbS1zYSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjU0MDli        ZTIyLTA4YTMtNDVkNS1iNGRlLWMyOGNlMGZjYmIwMyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpuY29tMDFwYW46bmNvbS1zYSJ9.H7EpGT0Le2evHG2UW96OO3-mvY7-Dg6nzVAgr98c        SUALecFyrEC9g-f9lYvgncS4mgQINV7voTaIYQ211AvGn6Adeu-PE3vPObxcIUA5_KJmRbKl7O1TMzqpJmIa5TnDeSLt2xN6D3bn74n1JpaGq3-VhBicA9j0jDbLVTi5EE_JGX2PkpJ-vvMhrnsGF        YzEA7oOAWwyyPMy2RPeEzKYK0bubvQaRLf2T-oZkWgXejWeLV0Z1mU12e75husjrEdu-FEfzyAEU_CQIuPAHHBC7U1OMLAuN_ehImmoLzObSCKqruLxeqIZamr6cNzZAKouc2bcdvLuDWmG3nVZRP        ZRGnRMKPGaFNPnetav0Nq5MvYy4zOAAaDWq1_B5b8iYFxCsycceqZKySe-Z_lmEw1x1lyf2I8Z5fpfaoPW_QxndSuxBrV4h6O9igZpwzoCjwq8vB838vkVMlLIcDGTViLAnLd8pl763-1coSzqsnt        rO_eUUTZICvTzp-dA6QdZOb5SWMXj9-vqvW469rjzgaopSeS7hmUO_6BGMS7O5-nZC4PG-QPISrUKup9eAM62jssTmu2QL4-y3FbY1vjOFvJAbkEwzBhPN-2EPEY9zUu44ZximqFwNkuR4T66u_jG        
[root@ncputility ~ pancwl_rc]$
```


### reference 

* [Creating an SA and map cluster admin role](https://docs.redhat.com/en/documentation/openshift_container_platform/4.8/html/authentication_and_authorization/understanding-and-creating-service-accounts#service-accounts-overview_understanding-service-accounts)
