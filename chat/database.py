import os
# import boto3
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute

class ChatModel(Model):
    class Meta:
        table_name = 'chat-table'
        if 'AWS_SAM_LOCAL' in os.environ:
            if os.environ['AWS_SAM_LOCAL']:
                host = 'http://dynamodb-local:8000'
    user = UnicodeAttribute(hash_key=True)
    message = UnicodeAttribute()


try:
    ChatModel.create_table(wait=True, billing_mode='on_demand')
except:
    print('Failed to create table')

# if not os.environ['AWS_SAM_LOCAL']:
#     dynamodb = boto3.client('dynamodb')
# else:
#     dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

# response = dynamodb.create_table(
#     TableName = 'chats-table',
#     BillingMode = 'PAY_PER_REQUEST',
#     AttributeDefinitions = [
#         {
#             'AttributeName': 'user',
#             'AttributeType': 'S'
#         }
#     ],
#     KeySchema = [
#         {
#             'AttributeName': 'user',
#             'KeyType': 'HASH'
#         }
#     ]
# )
# print(response)

def retrieveChat(user):
    return { 'ali': 'hi!', 'boon': 'yo', 'rosy': 'hi hi' }

def createChat(user, message):
    chat = ChatModel(user, message=message)
    chat.save()
    print(ChatModel.count())
    print({ 'user': user, 'message': message })