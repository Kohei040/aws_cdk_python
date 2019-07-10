# Lambdaに配置したファイル
file_name = "./hoge.txt"

# Lambda実行関数
def lambda_handler(event, context):
    file = open(file_name)
    data = file.read()
print(data)
