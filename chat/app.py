import json

from database import retrieveChat

def getChats(event, context):
    chats = retrieveChat()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "chats": chats
        })
    }