s3s3
====

A microservice to move files from S3 APIs (Swift or Ceph) to other S3 APIs. Messages notify the s3s3 service when new objects are created. Then the service will upload the new object to other S3 services. This service can also be used to move objects to AWS Galcier. This is done through AWS S3's lifecyce feature which transitions the objects from AWS S3 to AWS Glacier.

# LICENSE #

See the [LICENSE file](/LICENSE).
