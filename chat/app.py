import json

from database import retrieveChat

def lambda_handler(event, context):
    chats = retrieveChat()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "chats": chats
        })
    }