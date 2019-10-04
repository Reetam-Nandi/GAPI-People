import json,boto3
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def lambda_handler(event, context):
    
    s3 = boto3.client("s3")
    bucket = 'S3 Bucket Name'
    key = 'S3 Data File Name / Path'
    fileObj = s3.get_object(Bucket=bucket, Key=key)
    fileData = json.loads(fileObj["Body"].read().decode('utf-8'))
    
    creds = Credentials(token=fileData['access_token'],
                        refresh_token=fileData['refresh_token'],
                        client_id=fileData['client_id'],
                        token_uri=fileData['token_uri'],
                        client_secret=fileData['client_secret'])
    service = build('people', 'v1', credentials=creds, cache_discovery=False)
    
    service.people().deleteContact(resourceName = event['contactid']).execute()
    return {
        'statusCode': 200,
        'body': 'Contact Deleted Successfully'
    }