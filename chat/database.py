import os
# import boto3
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, NumberAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection

class ChatModel(Model):
    class Meta:
        table_name = 'chat-table'
        if 'AWS_SAM_LOCAL' in os.environ and os.environ['AWS_SAM_LOCAL']:
            print('using local dynamodb')
            host = 'http://dynamodb-local:8000'
    
    class TimeStampIndex(GlobalSecondaryIndex):
        class Meta:
            index_name = 'timestamp-index'
            read_capacity_units = 2
            write_capacity_units = 1
            projection = AllProjection()
        timestamp = NumberAttribute(hash_key=True)
    
    user = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True, default=0)
    message = UnicodeAttribute()
    timestamp_index = TimeStampIndex()

    def as_dict(self):
        '''
        Takes the current model and reviews the attributes to then translate to a dict
        '''
        return {key: getattr(self, key) for key in self.get_attributes().keys()}


try:
    print(ChatModel.exists())
    if not ChatModel.exists():
        print('creating table...')
        ChatModel.create_table(wait=True, billing_mode='PAY_PER_REQUEST')
except Exception as e:
    print('Failed to create table')
    print(e)

# if 'AWS_SAM_LOCAL' in os.environ and os.environ['AWS_SAM_LOCAL']:
#     dynamodb = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000')
# else:
#     dynamodb = boto3.client('dynamodb')

# try:
#     response = dynamodb.create_table(
#         TableName = 'chat-table',
#         BillingMode = 'PAY_PER_REQUEST',
#         AttributeDefinitions = [
#             {
#                 'AttributeName': 'user',
#                 'AttributeType': 'S'
#             }
#         ],
#         KeySchema = [
#             {
#                 'AttributeName': 'user',
#                 'KeyType': 'HASH'
#             }
#         ]
#     )
#     print(response)
# except dynamodb.exceptions.ResourceInUseException:
#     print('table already exist')
#     pass
# except Exception as e:
#     print('fail to create table')
#     print(e)

# def retrieveAllChatDb(user):
#     response = dynamodb.scan(
#         TableName = 'chat-table'
#     )
#     print(response)

# def createChatDb(user, message):
#     response = dynamodb.put_item(
#         TableName = 'chat-table',
#         ReturnConsumedCapacity = 'TOTAL',
#         Item = {
#             'user': { 'S': user },
#             'message': { 'S': message }
#         }
#     )
#     print(response)

def retrieveChat(user, lastupdate):
    # print({ user, lastupdate })
    chats = []
    for chat in ChatModel.scan(ChatModel.timestamp > lastupdate):
        chats.append(chat.as_dict())

    return chats

def createChat(user, message):
    try:
        timestamp = int(datetime.utcnow().timestamp())
        chat = ChatModel(user, timestamp=timestamp, message=message)
        print(chat.as_dict())
        chat.save()
    except Exception as e:
        print(e)
        raise Exception('Failed to save chat')
    # print(ChatModel.count())

    return chat.as_dict()