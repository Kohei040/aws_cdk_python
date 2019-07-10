# [Amazon EKS Workshop](https://eksworkshop.com)

[Previous](./04.AutoScaling/workshop_4.md) continuation

## Implement AutoScaling with CPA and CA

- Horizontal Pod Autoscaler(HPA)
  - Scales the pods in a deployment or replica set
  - Implement as a k8s API resource and controller
  - The controller manager queries the resource utilization against the metrics specified in each HorizontalPodAutoscaler definition
- Cluster Autoscaler(CA)
  - The k8s component that can be used to perform pod scaling as well as scaling nodes in a cluster
  - Automatically increases the size of an Auto Scaling group so that pods have a place to run
  - Attempts to remove idle nodes, that is, nodes with no running pods.

#### COnfigure Horizontal Pod Autoscaler(HPA)

- Deploy the Metrics Server

```
$ helm install stable/metrics-server \
    --name metrics-server \
    --version 2.0.4 \
    --namespace metrics

$ kubectl get apiservice v1beta1.metrics.k8s.io -o yaml
apiVersion: apiregistration.k8s.io/v1
kind: APIService
metadata:
  creationTimestamp: 2019-06-18T05:58:41Z
  labels:
    app: metrics-server
    chart: metrics-server-2.0.4
    heritage: Tiller
    release: metrics-server
  name: v1beta1.metrics.k8s.io
  resourceVersion: "15345"
  selfLink: /apis/apiregistration.k8s.io/v1/apiservices/v1beta1.metrics.k8s.io
  uid: 1fc3556d-918e-11e9-aba2-02cc013de700
spec:
  group: metrics.k8s.io
  groupPriorityMinimum: 100
  insecureSkipTLSVerify: true
  service:
    name: metrics-server
    namespace: metrics
  version: v1beta1
  versionPriority: 100
status:
  conditions:
  - lastTransitionTime: 2019-06-18T05:58:45Z
    message: all checks passed
    reason: Passed
    status: "True"
    type: Available
```

#### Scale an application with HPA

- Deplpy Sample APP

```
$ kubectl run php-apache --image=k8s.gcr.io/hpa-example --requests=cpu=200m --expose --port=80
kubectl run --generator=deployment/apps.v1beta1 is DEPRECATED and will be removed in a future version. Use kubectl create instead.
service/php-apache created
deployment.apps/php-apache created

$ kubectl get pods
NAME                         READY   STATUS              RESTARTS   AGE
php-apache-b5f58cc5f-klq8c   0/1     ContainerCreating   0          9s

$ kubectl get service
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.100.0.1       <none>        443/TCP   172m
php-apache   ClusterIP   10.100.121.199   <none>        80/TCP    37s
```

- Create an HPA resource

```
$ kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
horizontalpodautoscaler.autoscaling/php-apache autoscaled

$ kubectl get hpa
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   0%/50%    1         10        1          40s
```

- Generate load to trigger scaling(Other Teminal)

```
$ kubectl run -i --tty load-generator --image=busybox /bin/sh
kubectl run --generator=deployment/apps.v1beta1 is DEPRECATED and will be removed in a future version. Use kubectl create instead.
If you don't see a command prompt, try pressing enter.
/ # while true; do wget -q -O - http://php-apache; done
OK!OK!OK!OK!OK!..........
```

- Confirm HPA

```
$ kubectl get hpa -w
NAME         REFERENCE               TARGETS   MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache   0%/50%    1         10        1          3m46s
php-apache   Deployment/php-apache   371%/50%   1         10        1          5m11s
php-apache   Deployment/php-apache   371%/50%   1     10    4     5m15s
php-apache   Deployment/php-apache   65%/50%   1     10    8     6m
php-apache   Deployment/php-apache   62%/50%   1     10    10    7m15s
php-apache   Deployment/php-apache   46%/50%   1     10    10    8m

$ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
load-generator-5ff6784f85-xcm7g   1/1     Running   0          5m57s
php-apache-b5f58cc5f-bxdgb        1/1     Running   0          3m14s
php-apache-b5f58cc5f-klq8c        1/1     Running   0          10m
php-apache-b5f58cc5f-kx47f        1/1     Running   0          2m59s
php-apache-b5f58cc5f-l4db6        1/1     Running   0          74s
php-apache-b5f58cc5f-pjtck        1/1     Running   0          74s
php-apache-b5f58cc5f-pql72        1/1     Running   0          2m59s
php-apache-b5f58cc5f-qt5df        1/1     Running   0          2m59s
php-apache-b5f58cc5f-t4mzr        1/1     Running   0          2m59s
php-apache-b5f58cc5f-whjdt        1/1     Running   0          3m14s
php-apache-b5f58cc5f-xsqr6        1/1     Running   0          3m14s
```

#### Configure Cluster AutoScaler(CA)

```
$ mkdir ~/environment/cluster-autoscaler
$ cd ~/environment/cluster-autoscaler
$ wget https://eksworkshop.com/scaling/deploy_ca.files/cluster_autoscaler.yml
```

- Configure the ASG

Min : 3 -> 2
Max : 3 -> 8

- Configure the "cluster_autoscaler.yml"

Search for command: and within this block, replace the placeholder text <AUTOSCALING GROUP NAME> with the ASG name that you copied in the previous step.  
Also, update AWS_REGION value to reflect the region you are using and Save the file.

- Create an IAM Role

```
$ test -n "$ROLE_NAME" && echo ROLE_NAME is "$ROLE_NAME" || echo ROLE_NAME is not set

$ mkdir ~/environment/asg_policy

$ cat <<EoF > ~/environment/asg_policy/k8s-asg-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "autoscaling:DescribeAutoScalingGroups",
        "autoscaling:DescribeAutoScalingInstances",
        "autoscaling:SetDesiredCapacity",
        "autoscaling:TerminateInstanceInAutoScalingGroup"
      ],
      "Resource": "*"
    }
  ]
}
EoF

$ aws iam put-role-policy --role-name $ROLE_NAME --policy-name ASG-Policy-For-Worker --policy-document file://~/environment/asg_policy/k8s-asg-policy.json

$ aws iam get-role-policy --role-name $ROLE_NAME --policy-name ASG-Policy-For-Worker
{
    "RoleName": "eksctl-eksworkshop-eksctl-nodegro-NodeInstanceRole-AIMBB3GMPWGB",
    "PolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "autoscaling:DescribeAutoScalingGroups",
                    "autoscaling:DescribeAutoScalingInstances",
                    "autoscaling:SetDesiredCapacity",
                    "autoscaling:TerminateInstanceInAutoScalingGroup"
                ],
                "Resource": "*",
                "Effect": "Allow"
            }
        ]
    },
    "PolicyName": "ASG-Policy-For-Worker"
}
```

- Deploy the AutoScaler

```
$ kubectl apply -f ~/environment/cluster-autoscaler/cluster_autoscaler.yml
serviceaccount/cluster-autoscaler created
clusterrole.rbac.authorization.k8s.io/cluster-autoscaler created
role.rbac.authorization.k8s.io/cluster-autoscaler created
clusterrolebinding.rbac.authorization.k8s.io/cluster-autoscaler created
rolebinding.rbac.authorization.k8s.io/cluster-autoscaler created
deployment.extensions/cluster-autoscaler created

$ kubectl logs -f deployment/cluster-autoscaler -n kube-system
```

#### Scale a Cluster with CA

- Deploy a Sample App

```
cat <<EoF> ~/environment/cluster-autoscaler/nginx.yaml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: nginx-to-scaleout
spec:
  replicas: 1
  template:
    metadata:
      labels:
        service: nginx
        app: nginx
    spec:
      containers:
      - image: nginx
        name: nginx-to-scaleout
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 500m
            memory: 512Mi
EoF

$ kubectl apply -f ~/environment/cluster-autoscaler/nginx.yaml
deployment.extensions/nginx-to-scaleout created

$ kubectl get deployment/nginx-to-scaleout
NAME                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
nginx-to-scaleout   1         1         1            0           0s
```

- Scale our ReplicaSet

```
$ kubectl get nodes
NAME                             STATUS   ROLES    AGE     VERSION
ip-192-168-28-196.ec2.internal   Ready    <none>   4h27m   v1.12.7
ip-192-168-3-15.ec2.internal     Ready    <none>   4h27m   v1.12.7
ip-192-168-61-87.ec2.internal    Ready    <none>   4h27m   v1.12.7

$ kubectl scale --replicas=10 deployment/nginx-to-scaleout
deployment.extensions/nginx-to-scaleout scaled

$ kubectl get pods -o wide --watch
NAME                                 READY   STATUS    RESTARTS   AGE     IP               NODE                             NOMINATED NODE
load-generator-5ff6784f85-xcm7g      1/1     Running   1          98m     192.168.13.236   ip-192-168-3-15.ec2.internal     <none>
nginx-to-scaleout-5df9dff66b-82cx9   1/1     Running   0          21s     192.168.55.128   ip-192-168-61-87.ec2.internal    <none>
nginx-to-scaleout-5df9dff66b-8h7ph   1/1     Running   0          21s     192.168.17.129   ip-192-168-28-196.ec2.internal   <none>
nginx-to-scaleout-5df9dff66b-j9gvn   0/1     Pending   0          21s     <none>           <none>                           <none>
nginx-to-scaleout-5df9dff66b-kn2p6   1/1     Running   0          21s     192.168.58.223   ip-192-168-61-87.ec2.internal    <none>
nginx-to-scaleout-5df9dff66b-nmssz   1/1     Running   0          21s     192.168.4.175    ip-192-168-28-196.ec2.internal   <none>
nginx-to-scaleout-5df9dff66b-p9hbq   1/1     Running   0          21s     192.168.4.63     ip-192-168-3-15.ec2.internal     <none>
nginx-to-scaleout-5df9dff66b-pwn88   1/1     Running   0          21s     192.168.17.102   ip-192-168-3-15.ec2.internal     <none>
nginx-to-scaleout-5df9dff66b-x5fg7   1/1     Running   0          21s     192.168.45.62    ip-192-168-61-87.ec2.internal    <none>
nginx-to-scaleout-5df9dff66b-xbz82   1/1     Running   0          5m42s   192.168.8.11     ip-192-168-3-15.ec2.internal     <none>
nginx-to-scaleout-5df9dff66b-zwbj2   0/1     Pending   0          21s     <none>           <none>                           <none>
```

#### Cleanup scaling

```
$ kubectl delete -f ~/environment/cluster-autoscaler/cluster_autoscaler.yml
$ kubectl delete -f ~/environment/cluster-autoscaler/nginx.yaml
$ kubectl delete hpa,svc php-apache
$ kubectl delete deployment php-apache load-generator
$ rm -rf ~/environment/cluster-autoscaler
```
