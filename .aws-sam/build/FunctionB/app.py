import json
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

@xray_recorder.capture('function_b')
def lambda_handler(event, context):
    # The X-Ray context is automatically propagated via API Gateway
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Function B!"
        }),
    }
