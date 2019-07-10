#!/bin/bash
###############################################################################
# create_<サーバ種別>_launchconfig.sh
# 起動設定作成スクリプト
# 引数1： AMIのID
# 引数2：起動設定のプレフィックス
# 引数3：インスタンスタイプ
# 引数4：セキュリティグループのID
#
###############################################################################

## 変数
ami_id=$1
day=`date '+%Y%m%d%H%M'`
launchconfig=$2
launchconfig_name=${launchconfig}_${day}
instance_type=$3
securitygroup_id=$4

## 引数確認
if [[ $ami_id = "$null" ]]; then
  echo "【ERROR】引数(AMI ID)を指定してください"
  exit 1
fi

## AMIの状態確認
ami_state=`aws ec2 describe-images --image-ids $ami_id \
--query 'Images[].State' \
--output text`

if [[ $ami_state != available ]]; then
  echo "【ERROR】AMIの状態もしくはIDを確認してください"
  exit 1
fi

## 起動設定作成

aws autoscaling create-launch-configuration \
--launch-configuration-name $launchconfig_name \
--image-id $ami_id \
--security-groups $securitygroup_id \
--instance-type $instance_type \
--instance-monitoring Enabled=false \
--no-ebs-optimized \
--no-associate-public-ip-address

create_lc=$?
if [ $create_lc = 0 ]; then
  echo "【INFO】起動設定の作成が完了しました($launchconfig_name)"
else
  echo "【ERROR】起動設定の作成に失敗しました"
  exit 1
fi

## 起動設定世代管理(3世代)
generation=3
count=1

configs=`aws autoscaling describe-launch-configurations \
--query 'reverse(sort_by(LaunchConfigurations,&CreatedTime))[].LaunchConfigurationName' \
| grep $launchconfig |awk -F'["]' '{print $2}'`

for list in $configs; do
    if [ $count -le $generation ]; then
     ## 3世代以前の場合、処理をしない
     :
    else
     echo "【INFO】旧世代の起動設定を削除します($list)"

     ## 旧世代の起動設定削除

     aws autoscaling delete-launch-configuration --launch-configuration-name $list
     Stat=$?
      if [ $Stat = 0 ]; then
       echo "【INFO】旧世代の起動設定を削除しました($list)"
      else
       echo "【ERROR】旧世代の起動設定削除に失敗しました。($list)"
       exit 1
      fi
    fi
    count=$((count + 1))
done

## AutoScalingグループ変更のジョブに作成した起動設定を引き渡す
echo "LC_NAME="$launchconfig_name > lc_name.txt
chown -R jenkins:jenkins lc_name.txt