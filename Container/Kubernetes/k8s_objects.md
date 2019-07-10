# Kubernetes Objects

- k8s Objects are persistent entities in the k8s system
- k8s uses these entities to represent the state of your cluster
- To work with k8s objects, you must use the k8s API

## Object Spec and Status

- Every k8s object includes two nested object fields that govern the object's configuration
  - The object spec
    - Describe the desired state of the object
  - The object status
    - Represents the actual state of the object
    - Provided and updated by the k8s system
- At any given time, the k8s Control Plane actively manages an object's actual state to match the desired state you supplied


## Kubernetes Object Management

- The kubectl command-line tool supports different ways to create and manage k8s objects
  - Imperative commands
    - Live objects
    - ```kubectl run nginx --image nginx```
  - Imperative object configuration
    - Individual files
    - ```kubectl create -f nginx.yml```
  - Declarative object configuration
    - Directories of files
    - ```kubectl apply -f config/```

## Names

- All objects in the k8s REST API are unambiguously identified by a Name and a UID
  - Names
    - A client-provided string that refers to an object in a resource URL
    - Only one object of a given kind can have a given name at a time
  - UIDs
    - A k8s systems-generated string to uniquely identify objects
    - Every object created over the whole lifetime of a k8s cluster has a distinct UID

## Namespaces

k8s supports multiple virtual clusters backed by the same physical cluster  
These virtual clusters are called namespaces

- When to use multiple namespaces
  - Use in environments with many users spread across multiple teams, or projects
    - It's not necessary when several people use it
  - Namespaces provide a scope for names
    - Name of resources need to be unique within a namespaces, but not across namespaces
- Working with namespaces
  - List the current namespace
    - ```kubectl get namespace```
  - k8s starts with three initial namespaces
    - default
      - The default namespace for objects with no other namespace
    - kube-system
      - The namespace for objects created by the k8s system
    - kube-public
      - This namespace is created automatically and is readable by all users
  - Setting the namespace for a request
    - ```kubectl --namespace=<insert-namespace-name-here> run get nginx --image=nginx>```
  - Setting the namespace preference
    - ```kubectl config set-context $(kubectl config current-context) --namespace=<insert-namespace-name-here>```
    - ```kubectl config view |grep namespace:```
- Namespace and DNS
  - When you create a Service, it creates a corresponding DNS entry  
  - This entry is of the form "<service-name>.<namespace-name>.svc.cluster.local"
- Not all objects are in a namespace
  - Most k8s resource are in some namespaces
    - pods, service, replication, controller, and other
  - However namespace resource are not themselves in a space
  - Low-level resources, such as nodes and persistentVolumes, are not in any namespace

## Labels and Selector

- Labels are key/value pairs that are attached to objects, such as pods
- Label identifies the metadata for an object
- Label selectors
  - Unlike names and UIDs, labels do not provide uniqueness.
    - In general, we expect many objects to carry the same label
  - Via label selector, the client/useer can identify a set of objects
- Apply Label
  - ```kubectl run nginx --image nginx --labels="ver=1,env=prod"```
- Change Label
  - ```kubectl label deployments nginx "ver=2"```
- Label selector
  - ```kubectl get pods --selector="ver=2"```

## Annotations

- Use k8s annotations to attach arbitrary non-identifying metadata to objects
- Annotations are not used to identity and select objects
