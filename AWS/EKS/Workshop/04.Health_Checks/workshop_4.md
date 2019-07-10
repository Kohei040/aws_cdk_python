# [Amazon EKS Workshop](https://eksworkshop.com)

[Previous](./03.Health_Checks/workshop_3.md) continuation

## Health Checks

By default, Kubernetes will restart a container if it crashes for any reason.   
It uses Liveness and Readiness probes which can be configured for running a robust application by identifying the healthy containers to send traffic to and restarting the ones when required.

- Liveness probes
  - Used in Kubernetes to know when a pod is alive or dead.
- Readiness probes
  - Used in Kubernetes to know when a pod is ready to serve traffic.
  - Only when the readiness probe passes, a pod will receive traffic from the service.

#### Configure Liveness Probe

- Save the manifest as ~/environment/healthchecks/liveness-app.yaml

```
$ mkdir -p ~/environment/healthchecks
$ cat <<EoF > ~/environment/healthchecks/liveness-app.yaml
apiVersion: v1
kind: Pod
metadata:
  name: liveness-app
spec:
  containers:
  - name: liveness
    image: brentley/ecsdemo-nodejs
    livenessProbe:
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 5
EoF
```

- Create the pod using the manifest

```
$ kubectl apply -f ~/environment/healthchecks/liveness-app.yaml
pod/liveness-app created

$ kubectl get pod liveness-app
NAME           READY   STATUS    RESTARTS   AGE
liveness-app   1/1     Running   0          42s
```

- The kubectl describe command will show an event history which will show any probe failures or restarts.

```
$ kubectl describe pod liveness-app
Name:               liveness-app
Namespace:          default
Priority:           0
PriorityClassName:  <none>
Node:               ip-192-168-21-70.ec2.internal/192.168.21.70
Start Time:         Fri, 07 Jun 2019 08:33:35 +0000
Labels:             <none>
Annotations:        kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"name":"liveness-app","namespace":"default"},"spec":{"containers":[{"image":"...
Status:             Running
IP:                 192.168.3.104
Containers:
  liveness:
    Container ID:   docker://ad9f4daeed7e90d100880acc656a7ad04afcf8dc5b20d14cc29331c7ed9e0191
    Image:          brentley/ecsdemo-nodejs
    Image ID:       docker-pullable://brentley/ecsdemo-nodejs@sha256:dae70ced12111231ab5f9f9be4a01a75b12bbb0ad20c2cdb194fd24b2241bacc
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 07 Jun 2019 08:33:36 +0000
    Ready:          True
    Restart Count:  0
    Liveness:       http-get http://:3000/health delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-t8s2r (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  default-token-t8s2r:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-t8s2r
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age   From                                    Message
  ----    ------     ----  ----                                    -------
  Normal  Scheduled  85s   default-scheduler                       Successfully assigned default/liveness-app to ip-192-168-21-70.ec2.internal
  Normal  Pulling    84s   kubelet, ip-192-168-21-70.ec2.internal  pulling image "brentley/ecsdemo-nodejs"
  Normal  Pulled     84s   kubelet, ip-192-168-21-70.ec2.internal  Successfully pulled image "brentley/ecsdemo-nodejs"
  Normal  Created    84s   kubelet, ip-192-168-21-70.ec2.internal  Created container
  Normal  Started    84s   kubelet, ip-192-168-21-70.ec2.internal  Started container
```

- Introduce  a Failure

We will run the next command to send a SIGUSR1 signal to the nodejs application.  
By issuing this command we will send a kill signal to the application process in docker runtime.

```
$ kubectl exec -it liveness-app -- /bin/kill -s SIGUSR1 1

# Describe the pod after waiting for 15-20 seconds and you will notice kubelet actions of killing the Container and restarting it.
$ kubectl describe pod liveness-app
Name:               liveness-app
Namespace:          default
Priority:           0
PriorityClassName:  <none>
Node:               ip-192-168-21-70.ec2.internal/192.168.21.70
Start Time:         Fri, 07 Jun 2019 08:33:35 +0000
Labels:             <none>
Annotations:        kubectl.kubernetes.io/last-applied-configuration:
                      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"name":"liveness-app","namespace":"default"},"spec":{"containers":[{"image":"...
Status:             Running
IP:                 192.168.3.104
Containers:
  liveness:
    Container ID:   docker://2818f0d537a86952d2ade4d756ba61585a2dfa21a1b30c530ba2c3da1a277756
    Image:          brentley/ecsdemo-nodejs
    Image ID:       docker-pullable://brentley/ecsdemo-nodejs@sha256:dae70ced12111231ab5f9f9be4a01a75b12bbb0ad20c2cdb194fd24b2241bacc
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 07 Jun 2019 08:49:17 +0000
    Last State:     Terminated
      Reason:       Error
      Exit Code:    137
      Started:      Fri, 07 Jun 2019 08:33:36 +0000
      Finished:     Fri, 07 Jun 2019 08:49:17 +0000
    Ready:          True
    Restart Count:  1
    Liveness:       http-get http://:3000/health delay=5s timeout=1s period=5s #success=1 #failure=3
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-t8s2r (ro)
<Output omitted>
Events:
  Type     Reason     Age                From                                    Message
  ----     ------     ----               ----                                    -------
  Normal   Scheduled  16m                default-scheduler                       Successfully assigned default/liveness-app to ip-192-168-21-70.ec2.internal
  Warning  Unhealthy  56s (x3 over 66s)  kubelet, ip-192-168-21-70.ec2.internal  Liveness probe failed: Get http://192.168.3.104:3000/health: net/http: request canceled (Client.Timeout exceeded while awaiting headers)
  Normal   Pulling    26s (x2 over 16m)  kubelet, ip-192-168-21-70.ec2.internal  pulling image "brentley/ecsdemo-nodejs"
  Normal   Pulled     26s (x2 over 16m)  kubelet, ip-192-168-21-70.ec2.internal  Successfully pulled image "brentley/ecsdemo-nodejs"
  Normal   Created    26s (x2 over 16m)  kubelet, ip-192-168-21-70.ec2.internal  Created container
  Normal   Started    26s (x2 over 16m)  kubelet, ip-192-168-21-70.ec2.internal  Started container
  Normal   Killing    26s                kubelet, ip-192-168-21-70.ec2.internal  Killing container with id docker://liveness:Container failed liveness probe.. Container will be killed and recreated.

$ kubectl get pod liveness-app
NAME           READY   STATUS    RESTARTS   AGE
liveness-app   1/1     Running   1          16m
```

- Check the status of the container health checks

```
$ kubectl logs liveness-app --previous
<Output omitted>
Example app listening on port 3000!
::ffff:192.168.21.70 - - [07/Jun/2019:08:33:41 +0000] "GET /health HTTP/1.1" 200 15 "-" "kube-probe/1.12"
::ffff:192.168.21.70 - - [07/Jun/2019:08:33:46 +0000] "GET /health HTTP/1.1" 200 16 "-" "kube-probe/1.12"
```

#### Configure Readiness Probe

Save the text from following block as ~/environment/healthchecks/readiness-deployment.yaml.  
The readinessProbe definition explains how a linux command can be configured as healthcheck.  
We create an empty file /tmp/healthy to configure readiness probe and use the same to understand how kubelet helps to update a deployment with only healthy pods.

```
$ cat <<EoF > ~/environment/healthchecks/readiness-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: readiness-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: readiness-deployment
  template:
    metadata:
      labels:
        app: readiness-deployment
    spec:
      containers:
      - name: readiness-deployment
        image: alpine
        command: ["sh", "-c", "touch /tmp/healthy && sleep 86400"]
        readinessProbe:
          exec:
            command:
            - cat
            - /tmp/healthy
          initialDelaySeconds: 5
          periodSeconds: 3
EoF
```

- Create a deployment to test readiness probe

```
$ kubectl apply -f ~/environment/healthchecks/readiness-deployment.yaml
deployment.apps/readiness-deployment created

$ kubectl get pods -l app=readiness-deployment
NAME                                    READY   STATUS    RESTARTS   AGE
readiness-deployment-6b95b8dd66-52g64   1/1     Running   0          76s
readiness-deployment-6b95b8dd66-7vs4r   1/1     Running   0          76s
readiness-deployment-6b95b8dd66-krrrs   1/1     Running   0          76s
```

- Let us also confirm that all the replicas are available to serve traffic when a service is pointed to this deployment

```
$ kubectl describe deployment readiness-deployment | grep Replicas:
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
```

- Introduce a Failure

Pick one of the pods from above 3 and issue a command as below to delete the /tmp/healthy file which makes the readiness probe fail.

```
# kubectl exec -it <YOUR-READINESS-POD-NAME> -- rm /tmp/healthy
$ kubectl exec -it readiness-deployment-6b95b8dd66-52g64 -- rm /tmp/healthy

$ kubectl get pods -l app=readiness-deployment
NAME                                    READY   STATUS    RESTARTS   AGE
readiness-deployment-6b95b8dd66-52g64   0/1     Running   0          6m35s
readiness-deployment-6b95b8dd66-7vs4r   1/1     Running   0          6m35s
readiness-deployment-6b95b8dd66-krrrs   1/1     Running   0          6m35s

$ kubectl describe deployment readiness-deployment | grep Replicas:
Replicas:               3 desired | 3 updated | 3 total | 2 available | 1 unavailable
```

#### Clean up

```
$ kubectl delete -f ~/environment/healthchecks/liveness-app.yaml
pod "liveness-app" deleted

$ kubectl delete -f ~/environment/healthchecks/readiness-deployment.yaml
deployment.apps "readiness-deployment" deleted
```
