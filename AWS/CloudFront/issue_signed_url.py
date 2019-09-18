import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner

# CloudFrontのKey ID
key_id = 'XXXXXXXXXXXXXX'
# CloudFrontの秘密鍵
file = './xxxxxx.pem'
# 署名付きURLの有効期限
expire_date = datetime.datetime(2019, 10, 1)
# CloudFrontのURL
url = 'http://xxxxx.cloudfront.net/path'

# ダウンロード時に任意のファイル名に変更する場合のURL
# CloudFrontのBehavir設定を以下とする
# Query String Forwarding and Caching : Forward all, cache based on whitelist
# Query String Whitelist : response-content-disposition
# url = 'http://xxxxx.cloudfront.net/path?response-content-disposition=attachment%3B%20filename%3D<ファイル名>'

# ブラウザ表示かつダウンロード時に任意のファイル名に変更する場合のURL
# CloudFrontのBehavir設定を以下とする
# Query String Forwarding and Caching : Forward all, cache based on whitelist
# Query String Whitelist : response-content-disposition, response-content-type
# url = 'http://xxxxx.cloudfront.net/path?response-content-disposition=inline;filename=<ファイル名>&response-content-type=<MIMEタイプ>'


def rsa_signer(message):
    with open(file, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


cloudfront_signer = CloudFrontSigner(key_id, rsa_signer)

# Create a signed url that will be valid until the specfic expiry date
# provided using a canned policy.
signed_url = cloudfront_signer.generate_presigned_url(
    url, date_less_than=expire_date)
print(signed_url)
