"""
"""
import logging
import threading

import redis


class Listener(threading.Thread):
    def __init__(self, channels):
        threading.Thread.__init__(self)
        self.redis = redis.Redis()
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self, block):
        try:
            for message in self.pubsub.listen():
                if message['type'] == 'message':
                    block(message['data'])
        except redis.ConnectionError as ce:
            logging.warn(ce)

