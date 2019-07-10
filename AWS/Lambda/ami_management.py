# -*- coding: utf-8 -*-

import boto3
import os
import logging
import time

# AMI取得対象のインスタンス名を指定
target_ami = os.environ['TARGET_AMI']
ami_list   = target_ami.split(',')

# 世代保持数
gen_num = int(os.environ['GENERATION'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_cl = boto3.client('ec2')
ec2_rs = boto3.resource('ec2')

# Lambda実行
def lambda_handler(event, context):
    excecute_generation()

# AMIの世代一覧取得
def ami_sort(ami):
    ami_desc = ec2_cl.describe_images(
        Owners  = ['self'],
        Filters = [{'Name': 'name', 'Values': [ami + '*']}]
    )['Images']

    sort_ami_list = sorted(
        ami_desc,
        key = lambda x: x['CreationDate'],
        reverse = True,
    )

    return sort_ami_list

# 古い世代のAMI&Snapshot削除
def ami_delete(delete_list):
    count = 0
    for rm_ami in delete_list:
        count += 1
        if gen_num >= count:
            continue

        ami_name = rm_ami['Name']
        ami_id   = rm_ami['ImageId']
        snapshot_id = ec2_rs.Image(ami_id).block_device_mappings[0]['Ebs']['SnapshotId']

        logger.info('削除対象AMI：' + ami_name + ' ' + ami_id)

        ec2_cl.deregister_image(ImageId = ami_id)
        time.sleep(10)
        ec2_rs.Snapshot(snapshot_id).delete()

    return 0

# AMI&Snapshot世代管理
def excecute_generation():
    for ami in ami_list:
        delete_list = ami_sort(ami)
ami_delete(delete_list)
