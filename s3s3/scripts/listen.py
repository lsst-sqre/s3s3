#!/usr/bin/env python
"""
Listens for s3 object names through the redis pubsub 'backup' channel.
When notified call the s3s3.api.upload function.

Configuration template:
https://github.com/lsst-squre/s3s3/blob/master/s3s3/s3s3.ini.dist

Also: https://github.com/lsst-sqre/s3s3
"""
import argparse
import logging

from s3s3.client import ListenClient
from s3s3.config import initialize


def listen():
    """
    Subscribe to 'backup' redis pubsub channel and listen (a
    blocking call).
    """
    try:
        c = ListenClient()
        c.listen()
    except KeyboardInterrupt:
        return True
    except Exception as e:
        logging.warn(e)
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=str,
                        help='Configuration file to use.')
    args = parser.parse_args()
    if args.config:
        initialize(args.config)
    if listen():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
