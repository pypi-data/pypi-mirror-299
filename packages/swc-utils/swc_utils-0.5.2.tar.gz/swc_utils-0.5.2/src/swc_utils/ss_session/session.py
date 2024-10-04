from redis import Redis
from flask import current_app
from flask_session import Session
from swc_utils.caching import CachingService


def get_current_redis_session(app=current_app) -> Redis:
    return app.config["SESSION_REDIS"]


def get_current_redis_cache(app=current_app) -> CachingService:
    return app.config["SESSION_REDIS_CACHE"]


class ServerSideSession:
    def __init__(self, app, host="127.0.0.1", port=6379, db=0, cache: CachingService = None):
        self.app = app
        self.host = host
        self.port = port
        self.db = db

        self.app.config["SESSION_TYPE"] = "redis"
        self.app.config["SESSION_SERIALIZATION_FORMAT"] = "json"
        self.app.config["SESSION_REDIS"] = Redis(host=host, port=port, db=db)
        self.app.config["SESSION_REDIS_CACHE"] = cache

        Session(app)
