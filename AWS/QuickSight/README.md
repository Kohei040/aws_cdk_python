#### QuickSightを初めて利用する際のIAM Userについて
- QuickSightを利用する為にはIAM Userが必要
  - IAM Userで権限が足りていない場合、"Create your QuickSight account"の際に以下のエラーが出力される

```
This IAM user or role may not have all the correct permissions to subscribe to QuickSight.  
This can cause your subscription to fail. Log in using a different IAM user or role, and try again.  
Contact your AWS administrator or AWS Support if you need assistance. To learn more, see Set IAM policy
```

- IAM Policyは以下を利用
  - 詳細は[こちら](https://docs.aws.amazon.com/ja_jp/quicksight/latest/user/set-iam-policy.html)を参照

```
{
    "Statement": [
        {
            "Action": [
            "ds:AuthorizeApplication",
            "ds:CheckAlias ",
            "ds:CreateAlias",
            "ds:CreateIdentityPoolDirectory",
            "ds:DeleteDirectory",
            "ds:DescribeDirectories",
            "ds:DescribeTrusts",
            "ds:UnauthorizeApplication",
            "iam:AttachRolePolicy",
            "iam:CreatePolicy",
            "iam:CreatePolicyVersion",
            "iam:CreateRole",
            "iam:DeletePolicyVersion",
            "iam:DeleteRole",
            "iam:DetachRolePolicy",
            "iam:GetPolicy",
            "iam:GetPolicyVersion",
            "iam:GetRole",
            "iam:ListAccountAliases",
            "iam:ListAttachedRolePolicies",
            "iam:ListEntitiesForPolicy",
            "iam:ListPolicyVersions",
            "iam:ListRoles",
            "s3:ListAllMyBuckets",
            "quicksight:*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ],
    "Version": "2012-10-17"
}
```
