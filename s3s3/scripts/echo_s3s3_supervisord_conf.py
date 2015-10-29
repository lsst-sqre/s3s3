#!/usr/bin/env python
"""
Echo the s3s3 supervisord configuration file.
"""
from pkg_resources import Requirement, resource_string


def try_resource(location):
    """
    Try to get the resource in ``location``.
    """
    try:
        return resource_string(Requirement.parse('s3s3'), location)
    except FileNotFoundError:
        return ''


def echo():
    """
    Echo the s3s3 supervisord configuration file.

    Use pkg_resources module to try to find the s3s3.conf supervisord
    configuration file. The file is located in a different location
    depending on if it's a sdist or bdist_wheel install.
    """
    try:
        conf = try_resource('extras/s3s3.conf')  # sdist
        if not conf:
            conf = try_resource('../../../extras/s3s3.conf')  # bdist
        print(conf.decode('utf-8'))
        return True
    except Exception as e:
        return False


def main():
    if echo():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
