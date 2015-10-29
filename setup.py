import os
import setuptools
from s3s3.version import get_version

readme = open('README.rst').read()
requirements = open('requirements.txt').read().split('\n')

long_description = """
s3s3 %s
A microservice to move files from S3 APIs (Swift or Ceph) to other S3 APIs.

To install use `pip install s3s3`

----

%s

----

For more information, please see: https://github.com/lsst-sqre/s3s3
""" % (get_version('short'), readme)

setuptools.setup(
    name='s3s3',
    version=get_version('short'),
    author='jmatt',
    author_email='jmatt@lsst.org',
    description='A microservice to move files from S3 APIs (Swift or '
                'Ceph) to other S3 APIs.',
    long_description=long_description,
    url='https://github.com/lsst-sqre/s3s3',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
        'Topic :: System',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Systems Administration'
    ],
    data_files=[('extras', ['extras/s3s3.conf', 'extras/s3s3.ini.dist'])],
    entry_points={
        'console_scripts': [
            's3s3listen = s3s3.scripts.listen:main',
            's3s3bucket = s3s3.scripts.bucket:main',
            'echo_s3s3_ini_template = '
            's3s3.scripts.echo_s3s3_ini_template:main',
            'echo_s3s3_supervisord_conf = '
            's3s3.scripts.echo_s3s3_supervisord_conf:main'
        ]
    })
