# -*- coding: utf-8 -*-
import boto3
import json

file = 'iam_group_user.md'
client = boto3.client('iam')


def main():
    """
    IAM Group及びIAM Userの設定を取得し、
    Markdownに変換して出力する為の関数を呼び出す。
    """

    with open(file, 'w', encoding='utf-8') as f:
        f.write('# IAM'
                '\n\n## IAM Group'
                '\n\n| Group Name | Policy | User |'
                '\n|:--|:--|:--|')

    # IAM Group
    list_groups = client.list_groups()['Groups']
    for group in list_groups:
        iam_groups(group)

    # IAM User
    with open(file, 'a', encoding='utf-8') as f:
        f.write('\n\n## IAM User'
                '\n\n| Username | Group | Policy ※Group Policy Exclusions |'
                '\n|:--|:--|:--|')
    list_users = client.list_users()['Users']
    for user in list_users:
        iam_users(user)


def iam_groups(group):
    """
    IAM Groupの名前、ポリシー、所属ユーザを整理し、
    Markdown形式に変換して'iam_group_user.md'に出力する。

    Parameter
    ------
    group: dict
        IAM Groupの設定。
    """

    group_name = group['GroupName']
    inline_policies = client.list_group_policies(
        GroupName=group_name
    )['PolicyNames']
    attach_polcies = [i['PolicyName'] for i in
                      client.list_attached_group_policies(
                          GroupName=group_name
                      )['AttachedPolicies']]
    group_policies = '<br>'.join(map(str, inline_policies + attach_polcies))
    group_users = [i['UserName'] for i in
                   client.get_group(GroupName=group_name)['Users']]
    group_user = '<br>'.join(map(str, group_users))
    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n| {group_name} | {group_policies} | {group_user} |')


def iam_users(user):
    """
    IAM Userの名前、所属グループ、ポリシーを整理し、
    Markdown形式に変換して'iam_group_user.md'に出力する。

    Parameter
    ------
    user: dict
        IAM Userの設定。
    """

    user_name = user['UserName']
    join_groups = [i['GroupName'] for i in
                   client.list_groups_for_user(UserName=user_name)['Groups']]
    group_name = '<br>'.join(map(str, join_groups))
    inline_policies = client.list_user_policies(
        UserName=user_name
    )['PolicyNames']
    attach_policies = [i['PolicyName'] for i in
                       client.list_attached_user_policies(
                           UserName=user_name
                       )['AttachedPolicies']]
    user_policy = '<br>'.join(map(str, inline_policies + attach_policies))

    with open(file, 'a', encoding='utf-8') as f:
        f.write(f'\n| {user_name} | {group_name} | {user_policy} |')


if __name__ == '__main__':
    main()
