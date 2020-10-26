import json

from database import retrieveChat, createChat

def getChat(event, context):
    qs = event['queryStringParameters']

    if qs is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing query string parameter'
            })
        }

    if not 'user' in qs:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing query string parameter user'
            })
        }

    user = qs['user']

    chats = retrieveChat(user)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'ok',
            'chats': chats
        })
    }

def postChat(event, context):
    body = event['body']

    if body is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing body'
            })
        }

    data = json.loads(body)

    if not 'user' in data or not 'message' in data:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing parameter user or message'
            })
        }

    user = data['user']
    message = data['message']

    createChat(user, message)

    return {
        'statusCode': 201,
        'body': json.dumps({
            'status': 'ok'
        })
    }