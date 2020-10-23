import json

from database import retrieveChat

def getChat(event, context):
    chats = retrieveChat()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "ok",
            "chats": chats
        })
    }

def postChat(event, context):
    return {
        "statusCode": 201,
        "body": json.dumps({
            "status": "ok"
        })
    }