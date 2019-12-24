# AWS CLIを利用したECS on Fargateの実行

## 前提条件

- AWS CLIの最新バージョンをインストールし、設定済み
- [Amazon ECSでのセットアップ](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/get-set-up-for-amazon-ecs.html)が完了していること

## Procedure

### FaregateClusterを作成

- [Fargate キャパシティプロパイダーを使用](https://docs.aws.amazon.com/ja_jp/AmazonECS/latest/developerguide/fargate-capacity-providers.html)

```sh
aws ecs create-cluster \
     --cluster-name FargateSpotCluster \
     --capacity-providers FARGATE FARGATE_SPOT \
     --region us-east-1
{
    "cluster": {
        "clusterArn": "arn:aws:ecs:us-east-1:<AccountID>:cluster/FargateSpotCluster",
        "clusterName": "FargateSpotCluster",
        "status": "PROVISIONING",
        "registeredContainerInstancesCount": 0,
        "runningTasksCount": 0,
        "pendingTasksCount": 0,
        "activeServicesCount": 0,
        "statistics": [],
        "tags": [],
        "settings": [
            {
                "name": "containerInsights",
                "value": "disabled"
            }
        ],
        "capacityProviders": [
            "FARGATE",
            "FARGATE_SPOT"
        ],
        "defaultCapacityProviderStrategy": [],
        "attachmentsStatus": "UPDATE_IN_PROGRESS"
    }
}
```

### タスク定義を登録

- 以下のタスク定義(JSON)をファイルとして保存

```json
{
    "family": "sample-fargate",
    "networkMode": "awsvpc",
    "containerDefinitions": [
        {
            "name": "fargate-app",
            "image": "httpd:2.4",
            "portMappings": [
                {
                    "containerPort": 80,
                    "hostPort": 80,
                    "protocol": "tcp"
                }
            ],
            "essential": true,
            "entryPoint": [
                "sh",
		      "-c"
            ],
            "command": [
                "/bin/sh -c \"echo '<html> <head> <title>Amazon ECS Sample App</title> <style>body {margin-top: 40px; background-color: #333;} </style> </head><body> <div style=color:white;text-align:center> <h1>Amazon ECS Sample App</h1> <h2>Congratulations!</h2> <p>Your application is now running on a container in Amazon ECS.</p> </div></body></html>' >  /usr/local/apache2/htdocs/index.html && httpd-foreground\""
            ]
        }
    ],
    "requiresCompatibilities": [
        "FARGATE"
    ],
    "cpu": "256",
    "memory": "512"
}
```

- タスク登録

```sh
aws ecs register-task-definition --cli-input-json file://sample01.json
{
    "taskDefinition": {
        "taskDefinitionArn": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
        "containerDefinitions": [
            {
                "name": "fargate-app",
                "image": "httpd:2.4",
                "cpu": 0,
                "portMappings": [
                    {
                        "containerPort": 80,
                        "hostPort": 80,
                        "protocol": "tcp"
                    }
                ],
                "essential": true,
                "entryPoint": [
                    "sh",
                    "-c"
                ],
                "command": [
                    "/bin/sh -c \"echo '<html> <head> <title>Amazon ECS Sample App</title> <style>body {margin-
top: 40px; background-color: #333;} </style> </head><body> <div style=color:white;text-align:center> <h1>Amazon
 ECS Sample App</h1> <h2>Congratulations!</h2> <p>Your application is now running on a container in Amazon ECS.
</p> </div></body></html>' >  /usr/local/apache2/htdocs/index.html && httpd-foreground\""
                ],
                "environment": [],
                "mountPoints": [],
                "volumesFrom": []
            }
        ],
        "family": "sample-fargate",
        "networkMode": "awsvpc",
        "revision": 1,
        "volumes": [],
        "status": "ACTIVE",
        "requiresAttributes": [
            {
                "name": "com.amazonaws.ecs.capability.docker-remote-api.1.18"
            },
            {
                "name": "ecs.capability.task-eni"
            }
        ],
        "placementConstraints": [],
        "compatibilities": [
            "EC2",
            "FARGATE"
        ],
        "requiresCompatibilities": [
            "FARGATE"
        ],
        "cpu": "256",
        "memory": "512"
    }
}
```

- タスク定義を確認

```sh
aws ecs list-task-definitions
{
    "taskDefinitionArns": [
        "arn:aws:ecs:us-east-1:<AccountID>:task-definition/first-run-task-definition:1",
        "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1"
    ]
}
```

### サービス作成

- `--network-configuration`は作業しているアカウント用に修正する
    - パブリックで`http:80`でアクセスできる環境で

```sh
aws ecs create-service \
     --cluster FargateSpotCluster \
     --service-name FargateService \
     --task-definition sample-fargate \
     --desired-count 2 \
     --launch-type "FARGATE" \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-5148637e,subnet-dddafde2],securityGroups=[sg-43831e35]}"
{
    "service": {
        "serviceArn": "arn:aws:ecs:us-east-1:<AccountID>:service/FargateSevrice",
        "serviceName": "FargateService",
        "clusterArn": "arn:aws:ecs:us-east-1:<AccountID>:cluster/FargateSpotCluster",
        "loadBalancers": [],
        "serviceRegistries": [],
        "status": "ACTIVE",
        "desiredCount": 2,
        "runningCount": 0,
        "pendingCount": 0,
        "launchType": "FARGATE",
        "platformVersion": "LATEST",
        "taskDefinition": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
        "deploymentConfiguration": {
            "maximumPercent": 200,
            "minimumHealthyPercent": 100
        },
        "deployments": [
            {
                "id": "ecs-svc/9223370459782473036",
                "status": "PRIMARY",
                "taskDefinition": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
                "desiredCount": 2,
                "pendingCount": 0,
                "runningCount": 0,
                "createdAt": 1577072302.771,
                "updatedAt": 1577072302.771,
                "launchType": "FARGATE",
                "platformVersion": "1.3.0",
                "networkConfiguration": {
                    "awsvpcConfiguration": {
                        "subnets": [
                            "subnet-5148637e",
                            "subnet-dddafde2"
                        ],
                        "securityGroups": [
                            "sg-43831e35"
                        ],
                        "assignPublicIp": "DISABLED"
                    }
                }
            }
        ],
        "roleArn": "arn:aws:iam::<AccountID>:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS",
        "events": [],
        "createdAt": 1577072302.771,
        "placementConstraints": [],
        "placementStrategy": [],
        "networkConfiguration": {
            "awsvpcConfiguration": {
                "subnets": [
                    "subnet-5148637e",
                    "subnet-dddafde2"
                ],
                "securityGroups": [
                    "sg-43831e35"
                ],
                "assignPublicIp": "DISABLED"
            }
        },
        "schedulingStrategy": "REPLICA",
        "enableECSManagedTags": false,
        "propagateTags": "NONE"
    }
```

- サービスを確認

```sh
aws ecs list-services --cluster FargateSpotCluster
{
    "serviceArns": [
        "arn:aws:ecs:us-east-1:<AccountID>:service/FargateService"
    ]
}
```

- 実行中のサービスを確認

```sh
aws ecs describe-services --cluster FargateSpotCluster --services FargateService
{
    "services": [
        {
            "serviceArn": "arn:aws:ecs:us-east-1:<AccountID>:service/FargateService",
            "serviceName": "FargateService",
            "clusterArn": "arn:aws:ecs:us-east-1:<AccountID>:cluster/FargateSpotCluster",
            "loadBalancers": [],
            "serviceRegistries": [
                {
                    "registryArn": "arn:aws:servicediscovery:us-east-1:<AccountID>:service/srv-srzdhwz2hsdsxtkz"
                }
            ],
            "status": "ACTIVE",
            "desiredCount": 1,
            "runningCount": 1,
            "pendingCount": 0,
            "capacityProviderStrategy": [
                {
                    "capacityProvider": "FARGATE_SPOT",
                    "weight": 1,
                    "base": 0
                }
            ],
            "platformVersion": "LATEST",
            "taskDefinition": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
            "deploymentConfiguration": {
                "maximumPercent": 200,
                "minimumHealthyPercent": 100
            },
            "deployments": [
                {
                    "id": "ecs-svc/9223370459780925698",
                    "status": "PRIMARY",
                    "taskDefinition": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
                    "desiredCount": 1,
                    "pendingCount": 0,
                    "runningCount": 1,
                    "createdAt": 1577073850.109,
                    "updatedAt": 1577073965.3,
                    "capacityProviderStrategy": [
                        {
                            "capacityProvider": "FARGATE_SPOT",
                            "weight": 1,
                            "base": 0
                        }
                    ],
                    "platformVersion": "1.3.0",
                    "networkConfiguration": {
                        "awsvpcConfiguration": {
                            "subnets": [
                                "subnet-3b93e15e",
                                "subnet-838562ca"
                            ],
                            "securityGroups": [
                                "sg-046500ece28a81741"
                            ],
                            "assignPublicIp": "ENABLED"
                        }
                    }
                }
            ],
            "roleArn": "arn:aws:iam::<AccountID>:role/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS",
            "events": [
                {
                    "id": "23b8193d-ca40-4ac2-aae8-529365270377",
                    "createdAt": 1577073965.306,
                    "message": "(service FargateService) has reached a steady state."
                },
                {
                    "id": "b5500217-49f3-4b5a-b04a-62f8db077c6a",
                    "createdAt": 1577073858.155,
                    "message": "(service FargateService) has started 1 tasks: (task 6ff51dd5-abf2-4f1b-bee0-3fb7b43672ed)."
                }
            ],
            "createdAt": 1577073850.109,
            "placementConstraints": [],
            "placementStrategy": [],
            "networkConfiguration": {
                "awsvpcConfiguration": {
                    "subnets": [
                        "subnet-3b93e15e",
                        "subnet-838562ca"
                    ],
                    "securityGroups": [
                        "sg-046500ece28a81741"
                    ],
                    "assignPublicIp": "ENABLED"
                }
            },
            "schedulingStrategy": "REPLICA",
            "enableECSManagedTags": false,
            "propagateTags": "NONE"
        }
    ],
    "failures": []
}
```

- 実行中のタスク確認
    - `--tasks`にサービスで起動しているタスクIDを指定する

```sh
aws ecs describe-tasks --cluster FargateSpotCluster --tasks 6ff51dd5-abf2-4f1b-bee0-3fb7b43672ed
{
    "tasks": [
        {
            "attachments": [
                {
                    "id": "8106387a-3c14-47be-ae28-5db660eeba53",
                    "type": "ElasticNetworkInterface",
                    "status": "ATTACHED",
                    "details": [
                        {
                            "name": "subnetId",
                            "value": "subnet-3b93e15e"
                        },
                        {
                            "name": "networkInterfaceId",
                            "value": "eni-065ff4163c2ce82db"
                        },
                        {
                            "name": "macAddress",
                            "value": "02:97:fa:80:32:67"
                        },
                        {
                            "name": "privateIPv4Address",
                            "value": "172.31.72.192"
                        }
                    ]
                }
            ],
            "availabilityZone": "us-east-1a",
            "capacityProviderName": "FARGATE_SPOT",
            "clusterArn": "arn:aws:ecs:us-east-1:<AccountID>:cluster/FargateSpotCluster",
            "connectivity": "CONNECTED",
            "connectivityAt": 1577073863.084,
            "containers": [
                {
                    "containerArn": "arn:aws:ecs:us-east-1:<AccountID>:container/aabadafe-f3d9-4484-ae49-b0c12811391c",
                    "taskArn": "arn:aws:ecs:us-east-1:<AccountID>:task/6ff51dd5-abf2-4f1b-bee0-3fb7b43672ed",
                    "name": "fargate-app",
                    "image": "httpd:2.4",
                    "runtimeId": "a59f6d7765a6735a2ad950c369c29af6e5451154a78b5a273a4364f0eab2e9df",
                    "lastStatus": "RUNNING",
                    "networkBindings": [],
                    "networkInterfaces": [
                        {
                            "attachmentId": "8106387a-3c14-47be-ae28-5db660eeba53",
                            "privateIpv4Address": "172.31.72.192"
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "cpu": "0"
                }
            ],
            "cpu": "256",
            "createdAt": 1577073858.114,
            "desiredStatus": "RUNNING",
            "group": "service:FargateService",
            "healthStatus": "UNKNOWN",
            "lastStatus": "RUNNING",
            "launchType": "FARGATE",
            "memory": "512",
            "overrides": {
                "containerOverrides": [
                    {
                        "name": "fargate-app"
                    }
                ],
                "inferenceAcceleratorOverrides": []
            },
            "platformVersion": "1.3.0",
            "pullStartedAt": 1577073875.292,
            "pullStoppedAt": 1577073910.292,
            "startedAt": 1577073957.428,
            "startedBy": "ecs-svc/9223370459780925698",
            "tags": [],
            "taskArn": "arn:aws:ecs:us-east-1:<AccountID>:task/6ff51dd5-abf2-4f1b-bee0-3fb7b43672ed",
            "taskDefinitionArn": "arn:aws:ecs:us-east-1:<AccountID>:task-definition/sample-fargate:1",
            "version": 4
        }
    ],
    "failures": []
}
```
