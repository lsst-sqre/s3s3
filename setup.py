import os
import setuptools
from s3s3.version import get_version

readme = open('README.md').read()
requirements = open('requirements.txt').read().split('\n')

long_description = """
s3s3 %s
A microservice to move files from S3 APIs (Swift or Ceph) to other S3 APIs.

To install use `pip install s3s3`

----

%s

----

For more information, please see: https://github.com/Deca-Technologies/purpurite
""" % (get_version('short'), readme)

setuptools.setup(
    name='s3s3',
    version=get_version('short'),
    author='jmatt',
    author_email='jmatt@lsst.org',
    description="A microservice to move files from S3 APIs (Swift or Ceph) to other S3 APIs.",
    long_description=long_description,
    url="https://github.com/lsst-sqre/s3s3",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: System",
        "Topic :: System :: Archiving :: Backup",
        "Topic :: System :: Systems Administration"
    ],
    entry_points={
        'console_scripts': [
            's3s3listen = s3s3.scripts.listen:main',
            's3s3bucket = s3s3.scripts.bucket:main'
        ]
    })
