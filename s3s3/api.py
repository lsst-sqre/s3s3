"""
The API for s3s3.
"""
import logging
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

import redis


r = redis.Redis()


def create_connection(connection_args):
    connection_args = connection_args.copy()
    connection_args.pop('bucket_name')
    return S3Connection(**connection_args)


def upload(source_key, dest_keys):
    """
    `source_key` The source boto s3 key.
    `dest_keys` A list of the destination boto s3 keys.
    """
    # Use the same name if no destination key is passed.
    if not dest_keys or not source_key:
        raise Exception(
            'The source_key and dest_keys parameters are required.')
    with tempfile.NamedTemporaryFile() as data:
        source_key.get_contents_to_file(data)
        data.file.flush()
        for dest_key in dest_keys:
            dest_key.set_contents_from_filename(data.name)
            try:
                r.set(u'backup=>' + dest_key.key, True)
            except redis.ConnectionError:
                logging.warn('Unable to connect to redis')


def duplicate_bucket(source_bucket, dest_bucket):
    for source_key in source_bucket.get_all_keys():
        dest_key = Key(dest_bucket)
        dest_key.key = s3_key
        if not dest_key.exists():
            upload(source_key, [dest_key])
        _update_md5([source_key, dest_key])
        if source_key.md5 != dest_key.md5:
            upload(source_key, [dest_key])
            logging.info('Uploaded {0} to {1} in bucket {2}.'.format(
                dest_key.key,
                dest_key.bucket.connection.host,
                dest_key.bucket.name))


def _update_md5(keys):
    for key in keys:
        if not key.md5:
            with tempfile.NamedTemporaryFile() as data:
                dest_key.get_contents_to_file(data)
                data.file.flush()
                logging.info('Updated md5 for {0} to'
                             ' {1} in bucket {2}.'.format(
                                 key.key,
                                 key.bucket.connection.host,
                                 key.bucket.name))
