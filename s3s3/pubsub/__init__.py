from .. import config


if config.pubsub['redis']:
    from .redis import Listener
    listener = Listener('backup')
    listen = listener.run


if config.pubsub['sns']:
    listen = None
