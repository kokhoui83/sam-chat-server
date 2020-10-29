import os
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
        
    user = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True, default=0)
    message = UnicodeAttribute()

    def as_dict(self):
        '''
        Takes the current model and reviews the attributes to then translate to a dict
        '''
        return {key: getattr(self, key) for key in self.get_attributes().keys()}


try:
    print(ChatModel.exists())
    if not ChatModel.exists():
        print('Creating table...')
        ChatModel.create_table(wait=True, billing_mode='PAY_PER_REQUEST')
except Exception as e:
    print('Failed to create table')
    print(e)

def retrieveChat(user, lastupdate):
    chats = []
    for chat in ChatModel.scan(ChatModel.timestamp > lastupdate):
        chats.append(chat.as_dict())

    return chats

def createChat(user, message):
    try:
        timestamp = int(datetime.utcnow().timestamp())
        chat = ChatModel(user, timestamp=timestamp, message=message)
        chat.save()
    except Exception as e:
        print(e)
        raise Exception('Failed to screate chat')

    return chat.as_dict()