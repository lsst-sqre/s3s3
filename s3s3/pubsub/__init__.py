from .. import config
from .redis import Listener

def get_listen():
    if config.pubsub['redis']:
        listener = Listener('backup')
        return listener.run
    if config.pubsub['sns']:
        return None
