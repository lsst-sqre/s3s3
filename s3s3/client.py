"""
"""
from functools import partial
import logging

from boto.s3.key import Key

from .api import create_connection, upload
from .config import source, destinations
from .pubsub import listen as _listen


def on_notify(source_conn, dest_conns, s3_key):
    """
    Replicate the s3_key from a source s3 to multiple s3 destinations.
    """
    print(s3_key)
    source_bucket = source_conn.get_bucket(source['bucket_name'])
    source_key = Key(source_bucket)
    source_key.key = s3_key
    if source_key.exists() and dest_conns:
        dest_keys = []
        for name, dest_conn in dest_conns.items():
            print(name)
            print(destinations[name]['bucket_name'])
            dest_bucket = dest_conn.get_bucket(
                destinations[name]['bucket_name'])
            dest_key = Key(dest_bucket)
            dest_key.key = s3_key
            if not dest_key.exists():
                dest_keys.append(dest_key)
        upload(source_key, dest_keys)
    else:
        logging.warn('s3_key: {0} does not exist in source s3 bucket.'.format(s3_key))


class Client:
    """
    """

    def __init__(self):
        self.source_conn = create_connection(source)
        self.dest_conns = {name: create_connection(d)\
                           for name, d in destinations.items()}

    def listen(self):
        _listen(partial(on_notify, self.source_conn, self.dest_conns))
