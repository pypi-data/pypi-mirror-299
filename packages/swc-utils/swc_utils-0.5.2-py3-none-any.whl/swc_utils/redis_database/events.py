import pickle
import threading
from uuid import uuid4
from hashlib import md5
from functools import wraps
from flask import current_app
from swc_utils.caching import CachingService
from swc_utils.ss_session import get_current_redis_session, get_current_redis_cache


def redis_event_listener(channel):
    with current_app.app_context():
        redis_client = get_current_redis_session()

        def decorator(func, *args, **kwargs):
            @wraps(func)
            def wrapper(app):
                pubsub = redis_client.pubsub()
                pubsub.subscribe(channel)

                for message in pubsub.listen():
                    if message["type"] != "message":
                        continue

                    message = pickle.loads(message["data"])
                    message_uuid = message.get("uuid")
                    message_data = message.get("data")

                    app.logger.info(f"REDIS [{channel}] {message_data}")

                    with app.app_context():
                        resp_obj = pickle.dumps(
                            current_app.ensure_sync(func)(message_data, *args, **kwargs)
                        )

                    redis_client.publish(f"resp-{message_uuid}-{channel}", resp_obj)

            threading.Thread(target=wrapper, args=(current_app._get_current_object(),), daemon=True).start()

        return decorator


def get_redis_data(channel: str, data: any, cache: CachingService = None):
    """Get data from a Redis event."""

    cache = cache or get_current_redis_cache()
    cache = cache.get_cache("redis_response_cache", dict) if cache else None

    message_uuid = str(uuid4())
    message_sign = md5(pickle.dumps(data)).hexdigest()
    message = {"uuid": message_uuid, "data": data}

    if cache is not None:
        cache.clear_expired(10)
        if message_sign in cache:
            return cache[message_sign]

    redis_client = get_current_redis_session()
    redis_client.publish(channel, pickle.dumps(message))

    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"resp-{message_uuid}-{channel}")

    for message in pubsub.listen():
        if message["type"] == "message":
            resp_data = pickle.loads(message["data"])
            if cache is not None:
                cache[message_sign] = resp_data
            return resp_data
