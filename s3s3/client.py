"""
Clients that use the config to provide access to the api.
"""
from functools import partial
import logging

from boto.s3.key import Key

from .api import create_connection, upload, duplicate_bucket
from .config import source, destinations
from .pubsub import get_listen


def on_notify(source_conn, dest_conns, s3_key):
    """
    Replicate the s3_key from a source s3 connection to s3 destinations.
    """
    # s3_key is of type bytes and boto requires a str.
    s3_key = s3_key.decode('utf-8')
    source_key = _get_key(source_conn.bucket, s3_key)
    if source_key.exists():
        dest_keys = []
        dest_keys_verify_md5 = False
        for dest_name, dest_conn in dest_conns.items():
            dest_key = _get_key(dest_conn.s3s3_bucket, s3_key)
            if not dest_key.exists():
                dest_keys.append(dest_key)
                dest_keys_verify_md5 |= dest_conn.s3s3_verify_md5
        upload(source_key,
               dest_keys,
               self.source_conn.s3s3_verify_md5 or dest_keys_verify_md5)
    else:
        logging.warn('s3_key: {0} does not exist in '
                     'source s3 bucket.'.format(s3_key))


class Client(object):
    """
    A base client that configures the source and destination connections.
    """

    def __init__(self):
        self.source_conn = create_connection(source)
        self.source_conn.s3s3_verify_md5 = source['verify_md5']
        self.source_conn.s3s3_bucket = _get_bucket(self.source_conn)
        self.dest_conns = {name: create_connection(d)\
                           for name, d in destinations.items()}
        for name, dc in self.dest_conns.items():
            dc.s3s3_bucket = _get_bucket(dc, name)
            dc.s3s3_verify_md5 = destinations[name]['verify_md5']


class ListenClient(Client):
    """
    A client to listen for 'backup' redis pubsub channels and call
    on_notify.
    """

    def listen(self):
        _listen = get_listen()
        _listen(partial(on_notify, self.source_conn, self.dest_conns))


class BucketClient(Client):
    """
    A client that uses the configuration to provide access
    to the duplicate_bucket API function.

    Duplicate all s3 objects in the config.source s3 bucket to
    all destination buckets.
    """

    def duplicate(self):
        """
        Duplicate the source s3 bucket in the destination s3 bucket.
        """
        try:
            source_bucket = self.source_conn.s3s3_bucket
            source_verify_md5 = self.source_conn.s3s3_verify_md5
            for _, dest_conn in self.dest_conns.items():
                dest_verify_md5 = dest_conn.s3s3_verify_md5
                duplicate_bucket(
                    source_bucket,
                    dest_conn.s3s3_bucket,
                    verify_md5=(source_verify_md5 or dest_verify_md5))
        except Exception as e:
            logging.error(e)
            return False
        return True


def _get_bucket(conn, name=None):
    """
    Return the bucket for the connection.

    If there is a name then it's a destination connection. Otherwise
    it is the source connection.
    """
    if name:
        return conn.get_bucket(destinations[name]['bucket_name'])
    else:
        return conn.get_bucket(source['bucket_name'])


def _get_key(bucket, s3_key):
    """
    Create a boto.s3.key.Key using the bucket and s3_key (name).
    """
    key = Key(bucket)
    key.key = s3_key
    return key
