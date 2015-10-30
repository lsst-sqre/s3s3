"""
Redis pubsub.
"""
import threading

import redis

from ..log import logger


class Listener(threading.Thread):
    """
    A class to encapsulate redis pubsub.
    """
    def __init__(self, channels):
        threading.Thread.__init__(self)
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self, method):
        """
        A blocking function.
        ``method`` A method that takes the message data field as a parameter.
        """
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    method(message['data'])
        except redis.ConnectionError as ce:
            logger.warning(ce)
