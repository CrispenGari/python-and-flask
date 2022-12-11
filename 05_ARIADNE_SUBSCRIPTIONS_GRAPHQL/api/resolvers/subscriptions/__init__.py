from api.pubsub import pubsub
from ariadne import SubscriptionType
subscription = SubscriptionType()

@subscription.source("newMessage")
async def source_message(_, info):
    async with pubsub.subscribe(channel="message") as subscriber:
        async for event in subscriber:
            yield event.message