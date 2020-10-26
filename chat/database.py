import os
import boto3
# from pynamodb.models import Model
# from pynamodb.attributes import UnicodeAttribute

# class ChatModel(Model):
#     class Meta:
#         table_name = 'chat-table'
#         if 'AWS_SAM_LOCAL' in os.environ and os.environ['AWS_SAM_LOCAL']:
#             print('using local dynamodb')
#             host = 'http://dynamodb-local:8000'
#     user = UnicodeAttribute(hash_key=True)
#     message = UnicodeAttribute()

# try:
#     ChatModel.create_table(wait=True, billing_mode='on_demand')
# except:
#     print('Failed to create table')

if 'AWS_SAM_LOCAL' in os.environ and os.environ['AWS_SAM_LOCAL']:
    dynamodb = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')
else:
    dynamodb = boto3.client('dynamodb')

try:
    response = dynamodb.create_table(
        TableName = 'chats-table',
        BillingMode = 'PAY_PER_REQUEST',
        AttributeDefinitions = [
            {
                'AttributeName': 'user',
                'AttributeType': 'S'
            }
        ],
        KeySchema = [
            {
                'AttributeName': 'user',
                'KeyType': 'HASH'
            }
        ]
    )
    print(response)
except dynamodb.exceptions.ResourceInUseException:
    print('table already exist')
    pass
except Exception as e:
    print('fail to create table')
    print(e)

def retrieveAllChatDb(user):
    response = dynamodb.scan(
        TableName = 'chats-table'
    )
    print(response)

def createChatDb(user, message):
    response = dynamodb.put_item(
        TableName = 'chats-table',
        ReturnConsumedCapacity = 'TOTAL',
        Item = {
            'user': { 'S': user },
            'message': { 'S': message }
        }
    )
    print(response)

def retrieveChat(user):
    retrieveAllChatDb(user)
    return { 'ali': 'hi!', 'boon': 'yo', 'rosy': 'hi hi' }

def createChat(user, message):
    # chat = ChatModel(user, message=message)
    # chat.save()
    # print(ChatModel.count())
    createChatDb(user, message)
    print({ 'user': user, 'message': message })