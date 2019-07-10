# Kubernetes Components

## What is Master Components
- Provides a control plane for the cluster
- Can be started on any machine in the cluster
- Essentially all master components are started on one machine and user containers are not started

## About Master Components
- kube-apiserver
  - Components for exposing the Kubernetes API
- [etcd](https://github.com/etcd-io/etcd/blob/master/Documentation/docs.md)
  - Distributed key-value store designed to reliability and quickly provides access to critical data
- kube-scheduler
  - Components on the master that watches newly created pods that have no nodes assigned, and selects a node for them to run on
- kube-controller-manager
  - Components for running the controller
  - The controllers include the following
    - Node Controller
      - Responsible for noticing and responding when nodes go down
    - Replication Controller
      - Responsible for maintaining the correct number of pods for every replication controller object in the system
    - Endpoints Controller
      - Populates the Endpoints object
    - Service Account & Token Controller
      - Create default account
      - API access tokens for new namespaces
- [cloud-controller-manager](https://kubernetes.io/docs/tasks/administer-cluster/running-cloud-controller/)
  - Run a controller that interacts with the underlying cloud providers
  - The following controllers have cloud provider dependencies
    - Node Controller
      - For checking the cloud provider to determine if a node has been deleted in the cloud after it stop responding
    - Route Controller
      - For setting up routes in the underlying cloud infrastructure
    - Service Controller
      - For creating, updating and deleting cloud provider load balancers
    - Volume Controller
      - For creating, attaching, and mounting volumes, and interacting with the cloud provider to orchestrate volumes

## What is Node Components

- Run on every node
- Maintaining running pods
- Providing the Kubernetes runtime environment

## About Node Components

- kubelet
  - An agent that runs on each node in the cluster
  - Ensure that the containers described in the PodSpecs are running correctly
- [kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/)
  - The Kubernetes network proxy runs on each node
  -  Role to route network traffic
- Container Runtime
  - The software that is responsible for running containers

## What is Addons

- Pods and services that implement cluster feature
- [Addons List](https://kubernetes.io/docs/concepts/cluster-administration/addons/)

## About Addons

- [DNS](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
  - All k8s clusters should have cluster DNS
  - Containers started by k8s automatically include DNS server their DNS searches
- [Web UI(Dashboard)](https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/)
  - Manage and troubleshoot clusters as well as applications
- [Container Resource Monitoring](https://kubernetes.io/docs/tasks/debug-application-cluster/resource-usage-monitoring/)
  -  General times series metrics can be recorded and viewed in the browser
- Cluster-level Logging
  - Responsible for saving container logs to a central log store with search/browsing interface
  - [Logging Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
