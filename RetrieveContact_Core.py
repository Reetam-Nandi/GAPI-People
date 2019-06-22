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

    results = service.people().connections().list(resourceName=event['contactid'],pageSize=event['totalresults'],sortOrder=event['sort'],personFields=event['fields']).execute()
    connections = results.get('connections', [])
    varnames = []
    varpids = []
    varetag = []
    for person in connections:
        pids = person.get('resourceName', [])
        etag = person.get('etag', [])
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            varnames.append(name)
            varpids.append(pids)
            varetag.append(etag)
            
    return {
        'statusCode': 200,
        'body': {
            'Names': varnames,
            'ResourceNames': varpids,
            'Etags': varetag
        }
    }        
         
