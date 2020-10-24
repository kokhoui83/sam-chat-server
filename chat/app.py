import json

from database import retrieveChat, createChat

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
    body = event['body']

    data = json.loads(body)
    user = data['user']
    message = data['message']

    createChat(user, message)

    return {
        "statusCode": 201,
        "body": json.dumps({
            "status": "ok"
        })
    }