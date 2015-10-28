#!/usr/bin/env python
"""
Echo the s3s3 supervisord configuration file.
"""
import logging
import os


def echo():
    """
    Echo the s3s3 supervisord configuration file in
    the relative diretory `../../extras/s3s3.conf`
    """
    try:
        conf = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.path.pardir, os.path.pardir, 'extras/s3s3.conf'))
        print(open(conf).read())
        return True
    except Exception:
        return False


def main():
    if echo():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
