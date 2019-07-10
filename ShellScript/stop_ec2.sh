#!/bin/bash
###############################################################################
# stop_ec2.sh
# EC2停止スクリプト
# 引数1： インスタンスID
#
###############################################################################

## 変数
instance_id=$1

## インスタンスのステータス確認
status()
{
get_status=`aws ec2 describe-instances \
--filter Name=instance-id,Values=$instance_id \
--query 'Reservations[].Instances[].State[].Name' \
--output text`

echo $get_status
}

if [[ `status` = "$null" ]]; then
  echo "【ERROR】対象のインスタンスが存在しません"
  exit 1
fi

echo "【INFO】ジョブ実行前のステータスは「`status`」です"

## インスタンスの停止
aws ec2 stop-instances --instance-ids $instance_id

action=$?
if [[ $action = 0 ]]; then
  echo "【INFO】インスタンスの停止コマンドを実行しました"
else
  echo "【ERROR】インスタンスの停止コマンドに失敗しました"
  exit 1
fi

## インスタンスの停止確認
i=0
while [[ $i -le 10 ]]; do
  now_status=`status`

  if [[ $now_status = stopped ]]; then
    echo "【INFO】インスタンスの停止が完了しました"
    break
  else
    echo "【INFO】インスタンスを停止中...($now_status)"
    sleep 30
  fi
  i=$((i + 1))
done

if [[ `status` = stopped ]]; then
  echo "【INFO】ジョブは正常終了しました"
  exit 0
else
  echo "【ERROR】ジョブが異常終了しました(ステータス：`status`)"
  exit 1
fi
