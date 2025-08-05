# MACD Operations – Scope of Work

## Documentation Version History

| **Author Name** | **Published Date** | **Version** | **Comments** |
|------------------|---------------------|-------------|-------------|
| Tript | 08/05/2025          | 1.0         | Initial draft|

## MACD Service Support Channel


All MACD engineers, especially those working in NAM time zone to obtain additional SME support. Thus far, it has been observed that this channel is under-utilized. The  Services Support Teams channel is available to MACD engineers to reach out for next level support when needed. This should be done as soon as possible when stuck. `I encourage all MACD engineers to leverage this channel as the next level of support in case the MACD engineer is unable to address the issue on their own`. The channel is available at

**In general, the following is the support process for MACD engineers**

- MACD engineer tries to resolve issue on their own
- For India based engineers, reach out to your SME “Buddies”  in India time zone for additional support
- If working in the NAM time zone, reach out to the Services Support Team by posting a support message to the channel (also reach out which direct message in Teams chat if you don’t get a response quick enough)
- If buddies or SMEs cannot help resolve the issue, create an NPSS ticket to get next level technical support and a NCPFM ticket in parallel. also the highest sev is 2.   Also when you create the ticket, pls ensure that you also upload the necessary info such must gather and investigative results to expedite the investigation.


Please share feedback if this support process is meeting your needs when next level support is required, especially for engineers working in the NAM time zone.


[Services Support | MACD Operations | Microsoft Teams](https://teams.microsoft.com/l/channel/19%3A7o-tGsUP4VQsfHEy1DcVf4XcJW5rQkR1ocIrVnvJZzs1%40thread.tacv2/Services%20Support?groupId=7a0d773f-51d7-4b85-a359-f6766f94d8e9&tenantId=5d471751-9675-428d-917b-70f44f9630b0&ngc=true&allowXTenantAccess=true)

---

## MACD - Process for tickets that require LLD updates - Important

Here are the steps to follow for any incoming MACD requests that require an LLD update
 
- For any WP requiring an LLD update, inform Resource Manager of that need.
- MACD Request will be put on hold by Resource Manager
- The LLD update will be assigned to the Cloud Architect who worked on the initial project design.
- The Cloud Architect should complete the LLD updates immediately after the HLD, DNP, and CNF input sheets are finalized or aligned.
- If there are any pending updates to Nokia-owned design documents, the Cloud Architect should escalate them to the WP requester for follow-up.
- The LLD location is a common, project-specific SharePoint, and DA should upload the latest LLD to the project SharePoint.
- Once the LLD is updated, the WP is assigned to MACD team engineer for implementation.
- MACD engineer obtains the LLD from the project specific SharePoint and proceeds with resolution
 
To summarize, from a process point of view, the ticket should be put on hold for the DA to complete the LLD and review it with the MACD engineer so he knows what to do.

When it is completed, the ticket will be in assigned state so it is a go for the engineer to proceed.

---


## Don’ts by MACD engineer

### Do Not Perform Workarounds or Scripts Directly on NCP Nodes

- No direct changes are allowed on NCP nodes without NCP R&D approval. Everything must go through a documented NCP R&D ticket. If you receive such a request, just stop and inform Tript.
- Even if the request came from the application team or their R&D, it’s still not officially allowed unless approved and tracked properly from NCP R&D. If you receive such a request, just stop and inform Tript.
- We are delivering this as part of Professional Services, so we’re fully responsible and liable for the work we do.
- Making OS-level or node-level changes might fix things short term, but:
    - After live traffic starts, issues can arise.
    - Any scale-in/out won’t carry your manual fix.
    - Workarounds will be lost after a node restart.
    - This can lead to service outages.
- If something goes wrong, Red Hat can be held accountable, and the customer might claim penalties.

**Example:**

- command on node OS level
- platform validator python file on master node OS level directly
- sysctl.conf, adding or changing parameters directly on the node level

 
Please make sure not to do any workarounds or node-level changes or running scripts on the node directly.
 

### Access to the “anyuid” SCC for CNF user ID or service account - Not supported

- As part of any application prerequisites, if an application requires access to the “anyuid” SCC for its user ID or service account, it is not supported. Even if Application 4LS requests temporary access during troubleshooting, it is still not allowed.
 
- If you receive such a request, please advise the application team to contact their R&D team. After that, they should formally raise an NCPFM ticket and not through us.

---

## Disclaimer

> ⚠️ **Disclaimer:**  
> Failure to follow any of the defined steps, guidelines, or approvals outlined in this document may result in strict disciplinary action. All team members are expected to comply with the process to ensure project integrity and success.
