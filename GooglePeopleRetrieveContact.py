import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def lambda_handler(event, context):
    creds = Credentials(token=event['access_token'],
                        refresh_token=event['refresh_token'],
                        client_id=event['client_id'],
                        token_uri=event['token_uri'],
                        client_secret=event['client_secret'])
    service = build('people', 'v1', credentials=creds, cache_discovery=False)

    results = service.people().connections().list(resourceName='people/me',pageSize=2000,sortOrder='FIRST_NAME_ASCENDING',personFields='metadata,names,phoneNumbers').execute()
    connections = results.get('connections', [])
    for person in connections:
        pids = person.get('resourceName', [])
        names = person.get('names', [])
        if names:
            name = names[0].get('displayName')
            print(name)
            print(pids)
            
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }        
         
