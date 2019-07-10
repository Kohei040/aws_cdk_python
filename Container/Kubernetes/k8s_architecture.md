# Kubernetes Architecture

## [Node](https://kubernetes.io/docs/concepts/architecture/nodes/)

- A node is a worker machine in k8s
- A node may be a VM or physical machine, depending on the cluster
- Node Status
  - Addresses
    - HostName
    - ExternalIP
    - InternalIP
  - Condition
    - OutOfDisk : True if there insufficient free in the node for adding new pods
    - Ready     : True if the node is healthy and ready to accept pods
    - MemoryPressure : True if the node memory is low
    - PIDPressure    : True if there are too many processes on the node
    - DiskPressure   : True if the disk capacity is low
    - NetworkUnavalability : True if the network for the node is not correctly
  - Capacity
    - Describe the resources available on the node
      - CPU, Memory
      - The maximum number of node that can be scheduled onto the node
  - Info
    - Kernel version, k8s version, Docker version, OS name

## Master-Node Communication

- Cluster to Master
  - All Communication paths from the cluster to the master terminate at the apiserver
  - The apiserver is configured to listen for remote connections on a secure HTTPS port with one or more forms of client authentication enabled
- Master to Cluster
  - There are two primary communication path
    - apiserver to kubelet
      - Fetching logs for pods
      - Attaching (through kubelet) to running pods
      - Providing the kubelet's port-forwarding functionality
      - These connections terminate at the kubelet's HTTPS endpoint
    - apiserver to nodes, pods, and services
      - Default to plain HTTP connections and are therefore neither authenticated nor encrypted
      - These connections are not currently to run over untrusted and/or public network
