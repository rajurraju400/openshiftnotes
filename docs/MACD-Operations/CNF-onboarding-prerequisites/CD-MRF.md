# Temporary Sysctl Update Procedure for CD-MRF
## (fs.pipe-max-size for Troubleshooting)

This procedure describes how to temporarily update the `fs.pipe-max-size` sysctl parameter on a specific node during troubleshooting.  
The change must be **requested by the MRF team**, applied **only for the troubleshooting window**, and **reverted immediately** afterward.


## This change is approved by NCP blueprint team only for tmp usage. 

- https://jiradc2.ext.net.nokia.com/browse/NCPFM-2422 

---

## 1. Identify the Node Running the `nrd-oam` Pod

```bash
oc get pod -n <namespace> -o wide | grep nrd-oam
```

Note the **node name** from the output. 
Note:  this node name will be provided by the mrf team. we dont do it on all the nodes on the MCP.  

---

## 2. Connect to the Node

```bash
oc debug node/<node-name>
```

Inside the debug shell, enter the host filesystem:

```bash
chroot /host
```

---

## 3. Check the Current Value

```bash
sysctl fs.pipe-max-size
```

Default is usually:

```
fs.pipe-max-size = 1048576
```

---

## 4. Apply the Temporary Increase

```bash
sysctl -w fs.pipe-max-size=5242880
```

Verify the change:

```bash
sysctl fs.pipe-max-size
```

---

## 5. Perform Troubleshooting

Proceed with the required tech-support or debugging actions (MRF team activity).

---

## 6. Revert the Sysctl Value After Troubleshooting

Once the MRF team confirms troubleshooting is complete:

```bash
sysctl -w fs.pipe-max-size=1048576
```

Verify the revert:

```bash
sysctl fs.pipe-max-size
```

---

## 7. Exit the Node

```bash
exit
exit
```

This will leave the chroot and close the debug session.

---

## Notes

- **Do not** modify MachineConfig or persist the change.
- This method is **temporary only**, per NCPFM-2422 approval.
- Must always be done **on-demand** and **per MRF team request**.
- Must be applied **only on the specific node** where the affected pod is running.
