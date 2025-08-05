# OpenShift (NCP) Deployment – Scope of Work

## 📐 1. Design & Planning

- **Prepare the High-Level Design (HLD)** for the NCP deployment. (only the NCP position or dedicated document for NCP alone. not solution HLD.)
- The HLD must be reviewed and approved by **Nokia TDL** before proceeding to the LLD phase.
- **Develop Low-Level Designs (LLD)** for the following clusters:
  - HUB Cluster
  - NMC Cluster
  - NWC Cluster
- Capture and document application-specific requirements in the LLD, including:
  - Tenants
  - Users
  - Security Context Constraints (SCC)
  - Required application roles, if needed (default `network-attach` and `cbur` roles should be documented).
  - Collect all networking information (Metllb, ippool, backwards routes, nmstate networks etc.)
  - NCOM is used for CNF onboarding; no additional roles/SCCs are needed (check with Raj about it.).
- A **Red Hat architect** will perform an internal review of the HLD and LLD.
- Both the HLD and LLD must be formally approved by **Nokia TDL** before any installation activities commence.
- The **Red Hat DTM** must ensure no installation begins before Nokia TDL’s approval of the design documents.
- Redhat Engineer should be gone through “Redhat entry level criteria” process before touching the infra. 
- The **Red Hat DTM** must ensure no installation begins before Redhat Entry level criteria process to be fully completed without any gap. 


---

## 🛠️ 2. MOP for Deployment

- A detailed **Method of Procedure (MOP)** must be prepared for the deployment.
- The **Red Hat engineer** is responsible for preparing the site specific deployment MOP for Hub, NMC/NWC. 
- A **Red Hat architect** will prepare the deployment templates using Red Hat’s automation tools.
  - (Check with **Raj** regarding template creation.)

---

## 🧱 3. Infrastructure & Base Setup

- Install the OS on the `infra-manager` node when it is **dedicated** to NCP.
- Deploy the **infra-quay** application on the `infra-manager` node.
- Deploy the **Hub Cluster**.
- Deploy all **required OpenShift operators** on the Hub Cluster.
- Set up **ACM backup** on the Hub Cluster **before** initiating the NMC/NWC cluster deployment.
- Create and configure the necessary:
  - Users
  - Tenants
  - Roles
  - SCCs  
  on the Hub Cluster for the NCD Git CNF.

---

## ✅ 4. DVTS & Validation – Hub Cluster

- Complete **Hub Cluster DVTS** before starting the NMC/NWC cluster deployments.
  - DVTS artifacts must be obtained from **Tript via the Red Hat Drive**.

---

## 🔁 5. GitOps & Backup

- Deploy the **NCD Git server**.
- The **Nokia NCD team** is responsible for setting up **external backup** of the Git server prior to the CWL cluster deployment.

---

## 🚀 6. Cluster Deployment

- Deploy the **NMC and NWC Clusters**.
- Complete the **end-to-end deployment** of the NMC/NWC clusters, including:
  - All scale-outs
  - Common and site-specific site policies
  - MetalLB configuration
  - Backward routing
  - Egress configuration
  - Multus (NMState) networking
  - Tenant creation
  - User creation
  - SCCs and custom roles (as per the approved LLD)
  - Quay proxy cache setup
  - Standard NCP users for **NCP**, **NCOM**, and **NCD**

---

## ✅ 7. DVTS & Validation – NMC/NWC Clusters

- Complete final **DVTS for NMC/NWC Clusters** before handing over for CNF onboarding.
  - DVTS artifacts must be obtained from **Tript via the Red Hat Drive**.
- Ensure the **NCP Criteria Documentation and Checklist** are fully completed and verified.

---

## 📤 8. CNF Onboarding

- Red Hat will **not engage in CNF onboarding support** until the service is formally **procured by Nokia**.
- CNF onboarding support (once procured) includes:
  - Running **tcpdump** for CNF troubleshooting
  - CNF application installation assistance
  - Resolving CNF communication issues

---

## ⚠️ 9. Scope Management

- Red Hat **will not** cover any additional tasks outside of this scope without a formal **Change Order Request (COR)** process.
- Example requests that require COR:
  - Creating new users or tenants
  - Adding subnets to IP pools
  - Adding/changing/deleting networks/subnets for NMState, MetalLB, backward routes, etc.
  - Handling new application prerequisites not documented in the approved LLD.
  - Handing new changes to the cluster, scale-out, new hostgroup creation, even redeployment, NCP upgrade, Adding/modifying labels, even installing a PP on cluster. Which is not documented in the approved LLD.
- All such requests must be:
  - Documented in the respective **HLD/LLD**
  - **Approved by the TDL**
  - Backed by a **Change Order Request (COR)** before Red Hat engineers implement changes on the clusters

---

## ⚖️ 10. Disclaimer

> ⚠️ **Disclaimer:**  
> Failure to follow any of the defined steps, guidelines, or approvals outlined in this document may result in strict disciplinary action. All team members are expected to comply with the process to ensure project integrity and success.


## 🚫 11. Don’ts by Deployment engineer

- Installation activities must not begin until all design documents have been reviewed and approved, and the Red Hat Entry-Level Criteria process has been fully completed with no gaps.

- If a Red Hat engineer identifies any deviation from the blueprint design—whether at the hardware or software level—it must be escalated to the respective DTM.

- The Red Hat team does not support workarounds in solution implementation. Only fully supported blueprint configurations for Nokia NCP should be used. The only exception is for non-blueprint certification candidates. also Redhat not recommend any workaround. all issues need to be documented by `NCPFM` and recommandation should be coming from `NCPFM`.  

- Red Hat engineers will not provide recommendations for solution components (e.g., selecting between NCP Quay or NCD Harbor registries for CNF). CNF teams must strictly adhere to the High-Level Design (HLD) documentation.

- Red Hat teams are not involved in hardware readiness tasks, such as switch configuration, OS installation for the Infra-Manager server, or creating CNF users on Infra-Manager nodes.

- Red Hat engineers do not grant cluster-admin roles to CNF users, even temporarily. Exceptions apply only to default user IDs associated with NCP, NCD, and NCOM.

- Red Hat engineers are not involved in CNF onboarding unless it has been officially procured by Nokia.

- The Red Hat team will not participate in Customer presentations until they have been formally approved by the DTM.

- Red Hat engineers will not install any third-party software, antivirus, or RPM packages on Hub, NMC/NWC, or Infra-Manager nodes.

- Red Hat teams do not install or configure DNS or NTP servers as part of the NCP installation.

- RedHat teams will not provide any major updates to Nokia PM or Customers, all will go via DTM. `

- RedHat team do not share the credentials or any Exit deliverable artifacts via email. It should be via SP from DTM.
