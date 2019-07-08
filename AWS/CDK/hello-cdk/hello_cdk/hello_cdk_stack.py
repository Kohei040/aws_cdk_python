from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
    cdk
)

class HelloCdkStack(core.Stack):

    def __init__(self, app: core.App, id: str, **kwargs) -> None:
        super().__init__(app, id)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, 
            "MyFirstBucket",
            versioned=True,)
