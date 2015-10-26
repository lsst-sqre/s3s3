"""
"""
from functools import partial
from .api import create_connection, upload
from .config import source, destinations
from .pubsub import listen as _listen


def on_notify(source_conn, dest_conns, s3_key):
    """
    Replicate the s3_key from a source s3 to multiple s3 destinations.
    """
    print(s3_key)
    source_bucket = source_conn.get_bucket(source['bucket_name'])
    source_key = source_bucket.get_key(s3_key)
    if source_key.exists():
        for name, dest_conn in dest_conns.items():
            print(name)
            print(destinations[name]['bucket_name'])
            dest_bucket = dest_conn.get_bucket(
                destinations[name]['bucket_name'])
            dest_key = dest_bucket.get_key(s3_key)
            if not dest_key or not dest_key.exists():
                upload(source_key, dest_key)
    else:
        logger.warn('s3_key does not exist in source s3 bucket.')


class Client:
    """
    """

    def __init__(self):
        self.source_conn = create_connection(source)
        self.dest_conns = {name: create_connection(d)\
                           for name, d in destinations.items()}

    def listen(self):
        _listen(partial(on_notify, self.source_conn, self.dest_conns))
