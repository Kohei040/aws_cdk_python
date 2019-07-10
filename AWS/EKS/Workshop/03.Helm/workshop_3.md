# [Amazon EKS Workshop](https://eksworkshop.com)

[Previous](./02.example_microservice/workshop_2.md) continuation

#### Kubernetes Helm

[Helm](https://helm.sh/) is a package manager for Kubernetes that packages multiple Kubernetes resources into a single logical deployment unit called Chart.  
A Chart is a collection of files that describe k8s resources.

- Achieve a simple (one command) and repeatable deployment
- Manage application dependency, using specific versions of other application and services
- Manage multiple deployment configurations: test, staging, production and others
- Execute post/pre deployment jobs during application deployment
- Update/rollback and test application deployments

#### Install Helm on EKS

Once you install helm, the command will prompt you to run ‘helm init’. Do not run ‘helm init’.  
Follow the instructions to configure helm using Kubernetes RBAC and then install tiller as specified below If you accidentally run ‘helm init’, you can safely uninstall tiller by running ‘helm reset –force’

```
$ cd ~/environment
$ curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get > get_helm.sh
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  7001  100  7001    0     0   227k      0 --:--:-- --:--:-- --:--:--  227k
$ chmod +x get_helm.sh
$ ./get_helm.sh
Downloading https://get.helm.sh/helm-v2.14.1-linux-amd64.tar.gz
Preparing to install helm and tiller into /usr/local/bin
helm installed into /usr/local/bin/helm
tiller installed into /usr/local/bin/tiller
Run 'helm init' to configure helm.
```

- Configure Helm access with RBAC
  - Helm relies on a service called tiller that requires special permission on the kubernetes cluster, so we need to build a Service Account for tiller to use.

```
$ cat <<EoF > ~/environment/rbac.yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tiller
  namespace: kube-system
---
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: tiller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
  - kind: ServiceAccount
    name: tiller
    namespace: kube-system
EoF

$ kubectl apply -f ~/environment/rbac.yaml
serviceaccount/tiller created
clusterrolebinding.rbac.authorization.k8s.io/tiller created
```

- Install 'tiller' using the helm tooling
  - This will install tiller into the cluster which gives it access to manage resources in your cluster.

```
$ helm init --service-account tiller
Creating /home/ec2-user/.helm
Creating /home/ec2-user/.helm/repository
Creating /home/ec2-user/.helm/repository/cache
Creating /home/ec2-user/.helm/repository/local
Creating /home/ec2-user/.helm/plugins
Creating /home/ec2-user/.helm/starters
Creating /home/ec2-user/.helm/cache/archive
Creating /home/ec2-user/.helm/repository/repositories.yaml
Adding stable repo with URL: https://kubernetes-charts.storage.googleapis.com
Adding local repo with URL: http://127.0.0.1:8879/charts
$HELM_HOME has been configured at /home/ec2-user/.helm.
Tiller (the Helm server-side component) has been installed into your Kubernetes Cluster.
Please note: by default, Tiller is deployed with an insecure 'allow unauthenticated users' policy.
To prevent this, run `helm init` with the --tiller-tls-verify flag.
For more information on securing your installation see: https://docs.helm.sh/using_helm/#securing-your-helm-installation
```

#### Deploy Nginx  with Helm

- To update Helm’s local list of Charts, run

```
$ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Skip local chart repository
...Successfully got an update from the "stable" chart repository
Update Complete.
```

- Serach the Charts repository

```
$ helm search nginx
NAME                            CHART VERSION   APP VERSION     DESCRIPTION                                                 
stable/nginx-ingress            1.6.16          0.24.1          An nginx Ingress controller that uses ConfigMap to store ...
stable/nginx-ldapauth-proxy     0.1.2           1.13.5          nginx proxy with ldapauth                                   
stable/nginx-lego               0.3.1                           Chart for nginx-ingress-controller and kube-lego            
stable/gcloud-endpoints         0.1.2           1               DEPRECATED Develop, deploy, protect and monitor your APIs...
```

- Add the Bitnami repository

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories

$ helm search bitnami/nginx
NAME                                    CHART VERSION   APP VERSION     DESCRIPTION                           
bitnami/nginx                           3.2.2           1.16.0          Chart for the nginx server            
bitnami/nginx-ingress-controller        3.4.7           0.24.1          Chart for the nginx Ingress controller
```

- Install bitnami/nginx

```
$ helm install --name mywebserver bitnami/nginx
NAME:   mywebserver
LAST DEPLOYED: Fri Jun  7 06:49:16 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Pod(related)
NAME                                READY  STATUS             RESTARTS  AGE
mywebserver-nginx-78bd7f47cb-ql6t7  0/1    ContainerCreating  0         0s

==> v1/Service
NAME               TYPE          CLUSTER-IP   EXTERNAL-IP  PORT(S)       AGE
mywebserver-nginx  LoadBalancer  10.100.64.8  <pending>    80:30453/TCP  0s

==> v1beta1/Deployment
NAME               READY  UP-TO-DATE  AVAILABLE  AGE
mywebserver-nginx  0/1    1           0          0s
```

- Confirm Deployment&Service

```
$ kubectl get deployment mywebserver-nginx
NAME                DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
mywebserver-nginx   1         1         1            1           92s

$ kubectl get service mywebserver-nginx
NAME                TYPE           CLUSTER-IP    EXTERNAL-IP                                                               PORT(S)        AGE
mywebserver-nginx   LoadBalancer   10.100.64.8   xxxxxxxxxxxxxxx.us-east-1.elb.amazonaws.com   80:30453/TCP   115s
```

- Clean up

```
$ helm list
NAME            REVISION        UPDATED                         STATUS          CHART           APP VERSION     NAMESPACE
mywebserver     1               Fri Jun  7 06:49:16 2019        DEPLOYED        nginx-3.2.2     1.16.0          default  

$ helm delete --purge mywebserver
release "mywebserver" deleted

$ kubectl get pods -l app=mywebserver-nginx
No resources found.
$ kubectl get service mywebserver-nginx -o wide
Error from server (NotFound): services "mywebserver-nginx" not found
```

#### Deploy example Microservices using Helm

- Create a Chart

```
$ cd ~/environment
$ helm create eksdemo
Creating eksdemo

$ ll eksdemo/
total 16
drwxr-xr-x 2 ec2-user ec2-user 4096 Jun  7 07:06 charts        # a description of the chart
-rw-r--r-- 1 ec2-user ec2-user  103 Jun  7 07:06 Chart.yaml    # defaults, may be overridden during install or upgrade
drwxr-xr-x 3 ec2-user ec2-user 4096 Jun  7 07:06 templates     # May contain subcharts
-rw-r--r-- 1 ec2-user ec2-user 1099 Jun  7 07:06 values.yaml   # the template files themselves
```

- We’re actually going to create our own files, so we’ll delete these boilerplate files

```
$ rm -rf ~/environment/eksdemo/templates/
$ rm ~/environment/eksdemo/Chart.yaml
$ rm ~/environment/eksdemo/values.yaml
```

- Create a new Chart.yaml file which will describe the chart

```
$ cat <<EoF > ~/environment/eksdemo/Chart.yaml
apiVersion: v1
appVersion: "1.0"
description: A Helm chart for EKS Workshop Microservices application
name: eksdemo
version: 0.1.0
EoF
```

- Next we’ll copy the manifest files for each of our microservices into the templates directory as servicename.yaml

```
#create subfolders for each template type
$ mkdir -p ~/environment/eksdemo/templates/deployment
$ mkdir -p ~/environment/eksdemo/templates/service

# Copy and rename frontend manifests
$ cp ~/environment/ecsdemo-frontend/kubernetes/deployment.yaml ~/environment/eksdemo/templates/deployment/frontend.yaml
$ cp ~/environment/ecsdemo-frontend/kubernetes/service.yaml ~/environment/eksdemo/templates/service/frontend.yaml

# Copy and rename crystal manifests
$ cp ~/environment/ecsdemo-crystal/kubernetes/deployment.yaml ~/environment/eksdemo/templates/deployment/crystal.yaml
$ cp ~/environment/ecsdemo-crystal/kubernetes/service.yaml ~/environment/eksdemo/templates/service/crystal.yaml

# Copy and rename nodejs manifests
$ cp ~/environment/ecsdemo-nodejs/kubernetes/deployment.yaml ~/environment/eksdemo/templates/deployment/nodejs.yaml
$ cp ~/environment/ecsdemo-nodejs/kubernetes/service.yaml ~/environment/eksdemo/templates/service/nodejs.yaml
```

- Replace some values with template directives to allow more customization by removing hard-coded values

| Resource | Value |
|:---|:---|
| eksdemo/templates/deployment/* | replicas: {{ .Values.replicas }} |
| eksdemo/templates/deployment/frontend.yaml | - image: {{ .Values.frontend.image }}:{{ .Values.version }} |
| eksdemo/templates/deployment/crystal.yaml | - image: {{ .Values.crystal.image }}:{{ .Values.version }} |
| eksdemo/templates/deployment/nodejs.yaml | - image: {{ .Values.nodejs.image }}:{{ .Values.version }} |

- Create a values.yaml file with our template defaults

```
$ cat <<EoF > ~/environment/eksdemo/values.yaml
# Default values for eksdemo.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# Release-wide Values
replicas: 3
version: 'latest'

# Service Specific Values
nodejs:
  image: brentley/ecsdemo-nodejs
crystal:
  image: brentley/ecsdemo-crystal
frontend:
  image: brentley/ecsdemo-frontend
EoF
```

- Use the dry-run flag to test our templates

```
$ helm install --debug --dry-run --name workshop ~/environment/eksdemo
```

- Deploy the Chart

```
$ helm install --name workshop ~/environment/eksdemo
NAME:   workshop
LAST DEPLOYED: Fri Jun  7 07:36:14 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME              READY  UP-TO-DATE  AVAILABLE  AGE
ecsdemo-crystal   0/3    3           0          0s
ecsdemo-frontend  0/3    3           0          0s
ecsdemo-nodejs    0/3    3           0          0s

==> v1/Pod(related)
NAME                               READY  STATUS             RESTARTS  AGE
ecsdemo-crystal-6b45547688-6c9x9   0/1    ContainerCreating  0         0s
ecsdemo-crystal-6b45547688-mpwnt   0/1    ContainerCreating  0         0s
ecsdemo-crystal-6b45547688-srx2l   0/1    ContainerCreating  0         0s
ecsdemo-frontend-7f7644d5d5-8sgrs  0/1    ContainerCreating  0         0s
ecsdemo-frontend-7f7644d5d5-cf2xx  0/1    ContainerCreating  0         0s
ecsdemo-frontend-7f7644d5d5-tqnn2  0/1    ContainerCreating  0         0s
ecsdemo-nodejs-744d497fdc-944dc    0/1    ContainerCreating  0         0s
ecsdemo-nodejs-744d497fdc-nmwtr    0/1    ContainerCreating  0         0s
ecsdemo-nodejs-744d497fdc-vs4fh    0/1    ContainerCreating  0         0s

==> v1/Service
NAME              TYPE          CLUSTER-IP     EXTERNAL-IP  PORT(S)       AGE
ecsdemo-crystal   ClusterIP     10.100.121.63  <none>       80/TCP        0s
ecsdemo-frontend  LoadBalancer  10.100.80.160  <pending>    80:32406/TCP  0s
ecsdemo-nodejs    ClusterIP     10.100.47.80   <none>       80/TCP        0s
```

- Test the service

```
$ kubectl get svc ecsdemo-frontend -o jsonpath="{.status.loadBalancer.ingress[*].hostname}"; echo
xxxxxxxxxx.us-east-1.elb.amazonaws.com
```

- Rolling back

1. Open values.yaml and modify the image name under nodejs.image to brentley/ecsdemo-nodejs-non-existing. This image does not exist, so this will break our deployment.

```
$ cat eksdemo/values.yaml
# Default values for eksdemo.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# Release-wide Values
replicas: 3
version: 'latest'

# Service Specific Values
nodejs:
  image: brentley/ecsdemo-nodejs-non-existing
crystal:
  image: brentley/ecsdemo-crystal
frontend:
  image: brentley/ecsdemo-frontend
```

2. Deploy the updated demo application chart

```
$ helm upgrade workshop ~/environment/eksdemo
```

3. The rolling upgrade will begin by creating a new nodejs pod with the new image.  
   The new ecsdemo-nodejs Pod should fail to pull non-existing image.  
   Run helm status command to see the ImagePullBackOff error

```
$ helm status workshop
LAST DEPLOYED: Fri Jun  7 07:45:45 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME              READY  UP-TO-DATE  AVAILABLE  AGE
ecsdemo-crystal   3/3    3           3          10m
ecsdemo-frontend  3/3    3           3          10m
ecsdemo-nodejs    3/3    1           3          10m

==> v1/Pod(related)
NAME                               READY  STATUS            RESTARTS  AGE
ecsdemo-crystal-6b45547688-6c9x9   1/1    Running           0         10m
ecsdemo-crystal-6b45547688-mpwnt   1/1    Running           0         10m
ecsdemo-crystal-6b45547688-srx2l   1/1    Running           0         10m
ecsdemo-frontend-7f7644d5d5-8sgrs  1/1    Running           0         10m
ecsdemo-frontend-7f7644d5d5-cf2xx  1/1    Running           0         10m
ecsdemo-frontend-7f7644d5d5-tqnn2  1/1    Running           0         10m
ecsdemo-nodejs-744d497fdc-944dc    1/1    Running           0         10m
ecsdemo-nodejs-744d497fdc-nmwtr    1/1    Running           0         10m
ecsdemo-nodejs-744d497fdc-vs4fh    1/1    Running           0         10m
ecsdemo-nodejs-7d679dccd5-ffnlr    0/1    ImagePullBackOff  0         67s

==> v1/Service
NAME              TYPE          CLUSTER-IP     EXTERNAL-IP       PORT(S)       AGE
ecsdemo-crystal   ClusterIP     10.100.121.63  <none>            80/TCP        10m
ecsdemo-frontend  LoadBalancer  10.100.80.160  xxxxxxx...  80:32406/TCP  10m
ecsdemo-nodejs    ClusterIP     10.100.47.80   <none>            80/TCP        10m
```

4. List Helm release versions

```
$ helm history workshop
REVISION        UPDATED                         STATUS          CHART           DESCRIPTION     
1               Fri Jun  7 07:36:14 2019        SUPERSEDED      eksdemo-0.1.0   Install complete
2               Fri Jun  7 07:45:45 2019        DEPLOYED        eksdemo-0.1.0   Upgrade complete
```

5. Rollback to the previous application revision (can rollback to any revision too)

```
$ helm rollback workshop 1
Rollback was a success.
```

6. Validate workshop release status

```
$ helm status workshop
LAST DEPLOYED: Fri Jun  7 07:51:41 2019
NAMESPACE: default
STATUS: DEPLOYED

RESOURCES:
==> v1/Deployment
NAME              READY  UP-TO-DATE  AVAILABLE  AGE
ecsdemo-crystal   3/3    3           3          16m
ecsdemo-frontend  3/3    3           3          16m
ecsdemo-nodejs    3/3    3           3          16m

==> v1/Pod(related)
NAME                               READY  STATUS   RESTARTS  AGE
ecsdemo-crystal-6b45547688-6c9x9   1/1    Running  0         16m
ecsdemo-crystal-6b45547688-mpwnt   1/1    Running  0         16m
ecsdemo-crystal-6b45547688-srx2l   1/1    Running  0         16m
ecsdemo-frontend-7f7644d5d5-8sgrs  1/1    Running  0         16m
ecsdemo-frontend-7f7644d5d5-cf2xx  1/1    Running  0         16m
ecsdemo-frontend-7f7644d5d5-tqnn2  1/1    Running  0         16m
ecsdemo-nodejs-744d497fdc-944dc    1/1    Running  0         16m
ecsdemo-nodejs-744d497fdc-nmwtr    1/1    Running  0         16m
ecsdemo-nodejs-744d497fdc-vs4fh    1/1    Running  0         16m

==> v1/Service
NAME              TYPE          CLUSTER-IP     EXTERNAL-IP       PORT(S)       AGE
ecsdemo-crystal   ClusterIP     10.100.121.63  <none>            80/TCP        16m
ecsdemo-frontend  LoadBalancer  10.100.80.160  xxxxxxx...  80:32406/TCP  16m
ecsdemo-nodejs    ClusterIP     10.100.47.80   <none>            80/TCP        16m
```

- Clean up

```
$ helm del --purge workshop
release "workshop" deleted

$ helm status workshop
Error: getting deployed release "workshop": release: "workshop" not found
```
