import json,boto3

def lambda_handler(event, context):
    InvokeLam = boto3.client("lambda", region_name="us-east-1")
    event2 = {
        "contactid": "%s"%event['cid'],
        "fields": "%s"%event['filtermask'],
        "body": 
            {
                "etag":"%s"%event['etag'],
                "nicknames":
                        [
                        {
                         "value":"%s"%event['nname']
                        }
                        ],
                "organizations":
                        [
                        {
                         "name":"%s"%event['oname'],
                         "jobDescription":"%s"%event['odesc'],
                         "department":"%s"%event['odept']
                        }
                        ]
            }        
        }
    response = InvokeLam.invoke(FunctionName = "UpdateContact", InvocationType = "RequestResponse", Payload = json.dumps(event2))
    return {
        'Result': json.loads(response["Payload"].read())
    }
