import configparser
from distutils.util import strtobool
import importlib
import logging
import os


config = configparser.ConfigParser()
config.read(['/usr/local/etc/s3s3.ini',
             os.path.join(os.path.dirname(__file__), 's3s3.ini'),
             os.path.join(os.pardir, 's3s3.ini'),
             os.path.join(os.curdir, 's3s3.ini')])


source = {k: v for k, v in config['source'].items()}


def get_dest_connections():
    destinations = {}
    for section_name in config.sections():
        if section_name.startswith('dest'):
            destinations[section_name] =\
                {k: v for k, v in config[section_name].items()}
    return destinations


destinations = get_dest_connections()


def get_calling_format(name):
    """
    Get the calling format class from the boto.s3.connection module
    and return an instance of it.
    """
    botos3connection = importlib.import_module('boto.s3.connection')
    calling_format_class = getattr(botos3connection, name)
    return calling_format_class()


def connection_fixup(source, destinations):
    """
    Fix the configuration connection dictionaries so they
    can be passed in to boto to create valid boto s3 connections.
    """
    for conn_dicts in [source, destinations]:
        for _, conn in conn_dicts.items():
            if conn.get('is_secure'):
                conn['is_secure'] = bool(strtobool(conn['is_secure']))
            if conn.get('calling_format'):
                conn['calling_format'] =\
                get_calling_format(conn['calling_format'])


connection_fixup({'source': source}, destinations)


def get_pubsub():
    pubsub = {k: v for k, v in config['pubsub'].items()}
    pubsub['redis'] = bool(strtobool(pubsub.get('redis')))
    pubsub['sns'] = bool(strtobool(pubsub.get('sns')))
    if (pubsub.get('redis') ^ pubsub.get('sns')):
        return pubsub
    else:
        logging.warn('Use either redis or sns for pubsub but not both.')
        raise Exception('Use either redis or sns for pubsub but not both.')


pubsub = get_pubsub()
