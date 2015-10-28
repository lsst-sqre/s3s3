#!/usr/bin/env python
"""
Echo the s3s3 configuration template.
"""
import logging
from os.path import abspath, join, dirname, pardir


def echo():
    """
    Echo the s3s3 supervisord configuration file in
    the relative diretory `../../extras/s3s3.ini.dist`
    """
    try:
        conf = abspath(join(dirname(__file__),
                            pardir, pardir, 'extras/s3s3.ini.dist'))
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
