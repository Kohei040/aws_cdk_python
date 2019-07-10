#!/bin/bash
###############################################################################
# create_ami.sh
# AMI取得スクリプト
# 引数1： インスタンスID
#
###############################################################################

## 変数
instance_id=$1
day=`date '+%Y%m%d%H%M'`

## 引数確認
if [[ $instance_id = "$null" ]]; then
  echo "【ERROR】引数を指定してください"
  exit 1
fi

## 対象インスタンス確認
instance_name=`aws ec2 describe-instances --instance-ids $instance_id \
|grep -2 Name|grep Value |awk -F'["]' '{print $4}'`

if [[ $instance_name = "$null" ]]; then
  echo "【ERROR】対象のインスタンスが存在しません"
  exit 1
fi

## AMI作成
ami_name=$instance_name-ami-$day

create_ami_id=`aws ec2 create-image --instance-id $instance_id \
--name $ami_name \
--no-reboot \
--output text`

create_ami=$?
if [ $create_ami = 0 ]; then
  aws ec2 create-tags --resources $create_ami_id --tags Key=Name,Value=$ami_name
  aws ec2 wait image-available --image-ids $create_ami_id
  echo "【INFO】AMIを作成しました($create_ami_id)"
else
  echo "【ERROR】AMIの作成に失敗しました"
  exit 1
fi

## AMI世代数確認
generation=7
count=1

images=`aws ec2 describe-images \
--filters Name=tag-value,Values="$instance_name-*" \
--query 'reverse(sort_by(Images,&CreationDate))[].ImageId' \
--output text`

for ami_id in $images; do
    if [ $count -le $generation ]; then
     ## 7世代以前の場合、処理をしない
     :
    else
     ## 削除するAMI名取得
     image_name=`aws ec2 describe-images \
     --image-ids $ami_id \
     --query 'Images[].Name' \
     --output text`

     echo "【INFO】旧世代バックアップAMIを削除します($image_name:$ami_id)"

     ## 旧世代のスナップショットID取得
     snapshot_id=`aws ec2 describe-snapshots \
     --filters Name=description,Values="*$ami_id*" \
     --query 'Snapshots[].SnapshotId' \
     --output text`

     ## 旧世代のAMI削除
     aws ec2 deregister-image --image-id $ami_id
     sleep 5
     ## 旧世代のスナップショット削除
     aws ec2 delete-snapshot --snapshot-id $snapshot_id
     Stat=$?
      if [ $Stat = 0 ]; then
       echo "【INFO】旧世代のAMIを削除しました($image_name:$ami_id)"
      else
       echo "【ERROR】旧世代バックアップAMIの削除に失敗しました。($image_name:$ami_id)"
       exit 1
      fi
    fi
    count=$((count + 1))
done

## LaunchConfig作成ジョブにAMI IDを引き渡す
echo "AMI_ID="$create_ami_id > id.txt
chown -R jenkins:jenkins id.txt

echo "【INFO】バックアップジョブが完了しました"