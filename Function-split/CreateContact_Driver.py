import json,boto3

def lambda_handler(event, context):
    InvokeLam = boto3.client("lambda", region_name="us-east-1")
    event = { 
        "names":
                [
                {
                 "givenName":"%s"%event['name'],
                },
                ],
        "phoneNumbers":
                [
                {
                 "value":"%s"%event['number'],
                },
                ],
        "userDefined":
                [
                {
                "key":"%s"%event['udkey'],
                "value":"%s"%event['udval'],
                },
                ],
        }
    response = InvokeLam.invoke(FunctionName = "CreateContact_Core", InvocationType = "RequestResponse", Payload = json.dumps(event))
    return {
        'Result': json.loads(response["Payload"].read())
    }
