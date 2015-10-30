#!/usr/bin/env python
"""
Duplicate a source s3 bucket to destination s3 buckets.

Configuration template:
https://github.com/lsst-squre/s3s3/blob/master/s3s3/s3s3.ini.dist

Also: https://github.com/lsst-sqre/s3s3
"""
import argparse

from s3s3.client import BucketClient
from s3s3.config import initialize
from s3s3.log import logger


def duplicate():
    """
    Subscribe to 'backup' redis pubsub channel and listen (a
    blocking call).
    """
    try:
        bc = BucketClient()
        bc.duplicate()
    except KeyboardInterrupt:
        return True
    except Exception as e:
        logger.warning(e)
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=str,
                        help='Configuration file to use.')
    args = parser.parse_args()
    if args.config:
        initialize(args.config)
    if duplicate():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
