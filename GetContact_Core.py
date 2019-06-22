import json,boto3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def lambda_handler(event, context):
    
    s3 = boto3.client("s3")
    bucket = 'credsholder'
    key = 'AuthDetails.json'
    fileObj = s3.get_object(Bucket=bucket, Key=key)
    fileData = json.loads(fileObj["Body"].read().decode('utf-8'))
    
    creds = Credentials(token=fileData['access_token'],
                        refresh_token=fileData['refresh_token'],
                        client_id=fileData['client_id'],
                        token_uri=fileData['token_uri'],
                        client_secret=fileData['client_secret'])
    service = build('people', 'v1', credentials=creds, cache_discovery=False)
    
    contact2 = service.people().get(resourceName=event['contactid'],personFields=event['fields']).execute()
    data = {
        "ResourceName": contact2['resourceName'],
        "ETag": contact2['etag'],
        "Name": contact2['names'][0]['givenName'],
        "PhoneNumber": contact2['phoneNumbers'][0]['value']
    }
    return {
        'statusCode': 200,
        'body': 'Contact Data Retrieved Successfully',
        'DATA': data
    }