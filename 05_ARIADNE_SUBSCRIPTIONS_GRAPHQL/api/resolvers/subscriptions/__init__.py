import asyncio
from ariadne import SubscriptionType
from api.store import queues
subscription = SubscriptionType()

@subscription.source("post")
async def posts_source(obj, info):
    queue = asyncio.Queue(maxsize=0)
    queues.append(queue)
    try:
        while True:
            post = await queue.get()
            queue.task_done()
            payload = {
                "post": post,
                "error": None
            }
            yield payload
    except asyncio.CancelledError:
        queues.remove(queue)
        raise

@subscription.field("post")
async def posts_resolver(payload, info):
    return payload