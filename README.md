s3s3
====

s3s3 is a microservice to move files from one S3 compliant service to another (Swift, Ceph, AWS).

s3s3 has two services. `s3s3.scripts.listen` subscribes and listens to a redis pubsub channel waiting for s3 object names. When notified it calls `s3s3.api.upload` and uploads that S3 object from the source to destination(s). `s3s3.scripts.bucket` uploads all keys in one s3 bucket to another.

`s3s3.scripts.listen` is meant to be a real-time daemon.

`s3s3.scripts.bucket` is meant to run periodically as a cron job. Anything missed by `s3s3.scirpts.listen` will be handled by this service.

## Summary ##

s3s3 is required because Ceph and Swift are not feature complete with AWS S3. Many available libraries that work well with AWS S3 do not work with Ceph and Swift.

Some examples: `key.size` and `key.md5` do not work with Ceph S3 without fetching the contents of the key (or s3 object). Multipart uploads are not reliable with Ceph S3. V4 signatures are not supported by Ceph S3.

## Configuration ##

s3s3 must be configured. Configuration can be found in the `s3s3.config` module. A source, destination and pubsub section are required. Multiple destination connections are supported but there was minimal testing. To signify a section is a destination connection it must start with `'dest'`.

Example template: https://github.com/jmatt/s3s3/blob/master/s3s3/s3s3.ini.dist

```conf
[source]
     aws_access_key_id = {YOUR_AWS_ACCESS_KEY_ID}
     aws_secret_access_key = {YOUR_AWS_SECRET_ACCESS_KEY}
     bucket_name = {YOUR_S3_BUCKET}
     host = {YOUR_CEPH_S3_ENDPOINT}
     verify_md5 = False # Verify md5 during s3 operations. 
     is_secure = True # Optional
     calling_format = OrdinaryCallingFormat # Optional
[destination]
     aws_access_key_id = {YOUR_AWS_ACCESS_KEY_ID}
     aws_secret_access_key = {YOUR_AWS_SECRET_ACCESS_KEY}
     bucket_name = {YOUR_S3_BUCKET}
     verify_md5 = False # Verify md5 during s3 operations. 
     is_secure = True # Optional
```
## Install ##

s3s3 requires python3 and redis. It was tested with python3.4 and python3.5. And redis 3.x.
```bash
pip install s3s3
```
Pip install s3s3.

```bash
s3s3listen --config /path/to/s3s3.ini
```
This will use the configuration to build source and destination boto connections, connect to redis and start listening on the `backup` channel. Any messages pushed to that channel will be considered source s3 key names and will attempt to be uploaded to the destination connection(s).

```bash
s3s3bucket --config /path/pto/s3s3.ini
```
This will use the configuration to build source and destination boto connections and duplicate the source bucket in the destination bucket.

## Client ##

There are two clients. One for each service. `s3s3.client.ListenClient` is a client to listen to the `'backup'` redis pubsub channel and call `s3s3.client.on_notify`. `s3s3.client.BucketClient` is a client that uses the configuration to provide access to the duplicate_bucket API function.

## API ##

The API can be found in `s3s3.api` module.

```python
def create_connection(connection_args):
``` 
Creates a boto connection from the `connection_args` dictionary.

```python
def upload(source_key, dest_key, verify_md5=False):
```
Upload the source key (S3 object) to the destination key. If `verify_md5` is true then verify md5s match.

```python
def duplicate_bucket(source_bucket, dest_bucket, verify_md5=False):
````
Duplicate the source bucket to the destination bucket. If `verify_md5` is true then verify md5s match. If the md5 is not availabe compute it and verify it matches.

## Deploy ##

s3s3 requires redis, python3 and supervisord.

```bash
mkdir -p /opt/env
cd /opt/env
virtualenv -p python3 s3s3
. /opt/env/s3s3/bin/activate
pip install s3s3
echo_s3s3_supervisord_conf > /etc/supervisor/conf.d/s3s3.conf
service supervisor restart # or... start
```

## LICENSE ##

See the [LICENSE file](/LICENSE).
