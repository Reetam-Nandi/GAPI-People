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
    contact2 = service.people().createContact(body=event)
    contact2.execute()
    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }