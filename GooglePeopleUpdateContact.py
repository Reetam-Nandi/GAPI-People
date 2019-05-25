import json
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def lambda_handler(event, context):
    creds = Credentials(token=event['access_token'],
                        refresh_token=event['refresh_token'],
                        client_id=event['client_id'],
                        token_uri=event['token_uri'],
                        client_secret=event['client_secret'],
                        scopes=event['scope'])
    service = build('people', 'v1', credentials=creds, cache_discovery=False)
    event = { 
        "etag":"%s"%event['etag'],
        "nicknames":
                [
                {
                 "value":"%s"%event['nname'],
                },
                ],
        "organizations":
                [
                {
                 "name":"%s"%event['oname'],
                 "jobDescription":"%s"%event['odesc'],
                 "department":"%s"%event['odept']
                },
                ],        
        }
    contact2 = service.people().updateContact(resourceName="{}".format(event['resname']),updatePersonFields="nicknames,organizations",body=event)
    contact2.execute()
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }