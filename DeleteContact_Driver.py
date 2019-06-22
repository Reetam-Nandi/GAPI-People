import json,boto3

def lambda_handler(event, context):
    InvokeLam = boto3.client("lambda", region_name="us-east-1")
    response = InvokeLam.invoke(FunctionName = "DeleteContact", InvocationType = "RequestResponse", Payload = json.dumps(event))
    return {
        'Result': json.loads(response["Payload"].read())
    }