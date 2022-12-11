from api.pubsub import pubsub
from ariadne import MutationType
mutation = MutationType()

@mutation.field("sendMessage")
async def sendMessage_resolver(obj, info, message):
    await pubsub.publish(channel="message", message=message)
    return message