"""
The API for s3s3.
"""
import tempfile

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from . import config
from .log import logger


if config.pubsub['redis']:
    import redis
    r = redis.Redis()
else:
    Exception('Only redis is supported right now.')


def create_connection(connection_args):
    """
    Create a boto s3 connection using the connection_args dictionary.
    ``connection_args`` A dictionary of connection arguments.
    """
    connection_args = connection_args.copy()
    # bucket name is an invalid connection argument.
    connection_args.pop('bucket_name')
    connection_args.pop('verify_md5')
    return S3Connection(**connection_args)


def upload(source_key, dest_keys, verify_md5=False, force=False):
    """
    Download from the source s3 key to a named temporary file
    and upload to the destination s3 key, if the key doesn't exist.
    ``source_key`` The source boto s3 key.
    ``dest_keys`` A list of the destination boto s3 keys.
    ``verify_md5`` Verify md5 values when uploading. Source is always
    considered authoritative.
    ``force`` Force upload to dest_key, even if it exists.
    """
    if not dest_keys or not source_key:
        raise Exception(
            'The source_key and dest_keys parameters are required.')
    with tempfile.NamedTemporaryFile() as data:
        for dest_key in dest_keys:
            if force or not dest_key.exists():
                source_key.get_contents_to_file(data)
                data.file.flush()
                dest_key.set_contents_from_filename(data.name)
            _upload_verify_md5(verify_md5, source_key, dest_key)
            try:
                r.set(u'backup=>' + dest_key.key, True)
            except redis.ConnectionError:
                logger.warning('Unable to connect to redis')


def duplicate_bucket(source_bucket, dest_bucket, verify_md5=False):
    """
    Duplicate the source s3 bucket in the destination bucket.
    ``source_bucket`` The source boto s3 bucket.
    ``dest_bucket`` The destination boto s3 bucket.
    ``verify_md5`` Verify md5 values when duplicating. Source always
                   is considered authoritative. If md5 is missing this
                   will fetch the file to compute the md5 and make the
                   comparison.
    """
    for source_key in source_bucket.get_all_keys():
        dest_key = Key(dest_bucket)
        dest_key.key = source_key.key
        if not dest_key.exists():
            upload(source_key, [dest_key])
        if verify_md5:
            _update_md5([source_key, dest_key])
            if source_key.md5 != dest_key.md5:
                upload(source_key, [dest_key])
                logger.info('Uploaded {0} to {1} in bucket {2}.'.format(
                    dest_key.key,
                    dest_key.bucket.connection.host,
                    dest_key.bucket.name))


def _update_md5(keys):
    """
    If the md5 does not exist then retrieve the file so the md5 can be
    computed. This is required because some s3 clones do not provide
    md5 values.

    ``keys`` boto.s3.key.Key objects which may not have md5 hashes.
    """
    for key in keys:
        if not key.md5:
            with tempfile.NamedTemporaryFile() as data:
                key.get_contents_to_file(data)
                data.file.flush()
                logger.info('Updated md5 for {0} to'
                            ' {1} in bucket {2}.'.format(
                                key.key,
                                key.bucket.connection.host,
                                key.bucket.name))


def _upload_verify_md5(verify_md5, source_key, dest_key):
    """
    If verify_md5 is True then log a message about the inconsistency.

    Don't raise an exception because it'll interrupt the blocking pubsub
    listen.
    """
    if verify_md5 and source_key.md5 != dest_key.md5:
        _update_md5([source_key, dest_key])
        logger.warning('md5 hash does not match for {0} to'
                       ' {1} in bucket {2}.'.format(
                           dest_key.key,
                           dest_key.bucket.connection.host,
                           dest_key.bucket.name))
