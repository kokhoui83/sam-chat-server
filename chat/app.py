import json
from datetime import datetime
from database import retrieveChat, createChat, getChatCount

def getChat(event, context):
    qs = event['queryStringParameters']

    # return error 400 if missing parameter
    if qs is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing query string parameter'
            })
        }

    # return error 400 if missing user param
    if not 'user' in qs:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing query string parameter user'
            })
        }

    user = qs['user']

    # get lastupdate parameter, else use current time
    if 'lastupdate' in qs:
        lastupdate = int(qs['lastupdate'])
    else:
        lastupdate = int(datetime.utcnow().timestamp())

    # store current query time
    current = int(datetime.utcnow().timestamp())
    # get all chat since lastupdate
    chats = retrieveChat(user, lastupdate)

    return {
        'statusCode': 200,
        'body': json.dumps({
            'status': 'ok',
            'chats': chats,
            'lastupdate': current
        })
    }

def postChat(event, context):
    body = event['body']

    # return error 400 if no post body
    if body is None:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing body'
            })
        }

    data = json.loads(body)

    # return error 400 if missing user or message in post body
    if not 'user' in data or not 'message' in data:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'error': 'missing parameter user or message'
            })
        }

    user = data['user']
    message = data['message']

    try:
        chat = createChat(user, message)

        return {
            'statusCode': 201,
            'body': json.dumps({
                'status': 'ok',
                'chat': chat
            })
        }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'server error - failed to create chat message'
            })
        }

def chatCount(event, context):
    try:
        count = getChatCount()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'total': count['value']
            })
        }
    except Exception:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'server error - failed to get chat count'
            })
        }