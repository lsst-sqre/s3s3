"""
Logging for s3s3.
"""
import logging


format = '%(asctime)s %(name)s-%(levelname)s '\
         '[%(pathname)s %(lineno)d] %(message)s'


PATHS = ['/var/log/s3s3/s3s3.log',
         '/tmp/s3s3.log']


def get_filename():
    """
    Try to open log files from the PATHS list, the first log file
    path that is successful is returned.
    """
    for path in PATHS:
        try:
            with open(path, 'a+') as f:
                return path
        except Exception:
            pass
    Exception('Unable to create logfile.')


logging.basicConfig(level=logging.INFO,
                    format=format,
                    filename=get_filename(),
                    filemode='a+')


logger = logging.getLogger()
