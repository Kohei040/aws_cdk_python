#!/bin/bash
###############################################################################
# start_ec2.sh
# EC2起動スクリプト
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

## インスタンスの起動
aws ec2 start-instances --instance-ids $instance_id

action=$?
if [[ $action = 0 ]]; then
  echo "【INFO】インスタンスの起動コマンドを実行しました"
else
  echo "【ERROR】インスタンスの起動コマンドに失敗しました"
  exit 1
fi

## インスタンスの起動確認
i=0
while [[ $i -le 10 ]]; do
  now_status=`status`

  if [[ $now_status = running ]]; then
    echo "【INFO】インスタンスの起動が完了しました"
    break
  else
    echo "【INFO】インスタンスを起動中...($now_status)"
    sleep 30
  fi
  i=$((i + 1))
done

if [[ `status` = running ]]; then
  echo "【INFO】ジョブは正常終了しました"
  exit 0
else
  echo "【ERROR】ジョブが異常終了しました(ステータス：`status`)"
  exit 1
fi
