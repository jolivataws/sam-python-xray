import json
import os
import boto3
import requests
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

patch_all()

session = boto3.Session()
lambda_client = session.client('lambda')

@xray_recorder.capture('function_a')
def lambda_handler(event, context):
    function_b_url = os.environ['FUNCTION_B_API']
    
    # Start a custom segment
    with xray_recorder.in_segment('FunctionA-to-FunctionB') as segment:
        try:
            # Add a subsegment for the API call
            with xray_recorder.in_subsegment('CallFunctionB'):
                response = requests.get(function_b_url)
                function_b_response = response.json()
            
            segment.put_annotation('StatusCode', response.status_code)
            segment.put_metadata('ResponseData', function_b_response)
        except Exception as e:
            segment.put_annotation('Error', str(e))
            function_b_response = f"Error calling Function B: {str(e)}"

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from Function A!",
            "function_b_response": function_b_response
        }),
    }
