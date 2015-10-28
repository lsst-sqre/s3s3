import configparser
from distutils.util import strtobool
import importlib
import logging
import os


required_sections = ['source',
                     'destinations',
                     'pubsub']
source = None
destinations = None
pubsub = None
config_files = ['/usr/local/etc/s3s3.ini',
                os.path.join(os.path.dirname(__file__), 's3s3.ini'),
                os.path.join(os.pardir, 's3s3.ini'),
                os.path.join(os.curdir, 's3s3.ini')]


def get_source_connection(config):
    return {k: v for k, v in config['source'].items()}


def get_dest_connections(config):
    destinations = {}
    for section_name in config.sections():
        if section_name.startswith('dest'):
            destinations[section_name] =\
                {k: v for k, v in config[section_name].items()}
    return destinations


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
            if conn.get('verify_md5'):
                conn['verify_md5'] = bool(strtobool(conn['verify_md5']))
            else:
                conn['verify_md5'] = False
            if conn.get('is_secure'):
                conn['is_secure'] = bool(strtobool(conn['is_secure']))
            if conn.get('calling_format'):
                conn['calling_format'] =\
                get_calling_format(conn['calling_format'])


def get_pubsub(config):
    if config.has_section('pubsub'):
        pubsub = {k: v for k, v in config['pubsub'].items()}
        pubsub['redis'] = bool(strtobool(pubsub.get('redis')))
        pubsub['sns'] = bool(strtobool(pubsub.get('sns')))
        if (pubsub.get('redis') ^ pubsub.get('sns')):
            return pubsub
        else:
            logging.warn('Use either redis or sns for pubsub but not both.')
            raise Exception('Use either redis or sns for pubsub but not both.')
    else:
        return {'redis': False, 'sns': False}


def has_required_sections(config):
    sections = config.sections()
    for section in required_sections:
        if not (section in sections):
            return False
    return True


def initialize(config_file=None):
    global source, destinations, pubsub
    config = configparser.ConfigParser()
    if config_file:
        config_files.append(os.path.expanduser(config_file))
    files_read = config.read(config_files)
    if has_required_sections(config):
        logging.warn('Missing required sections: {0}'.format(
            required_sections))
    source = get_source_connection(config)
    destinations = get_dest_connections(config)
    pubsub = get_pubsub(config)
    connection_fixup({'source': source}, destinations)


initialize()
