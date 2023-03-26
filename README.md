# s3hive

A tool built on top of boto3 that allows you to easily manage your S3 buckets.

<!-- Python version bugde -->

<!-- [![Python Version](https://img.shields.io/pypi/pyversions/s3hive.svg)](https://pypi.org/project/s3hive/)
[![PyPI version](https://badge.fury.io/py/s3hive.svg)](https://badge.fury.io/py/s3hive)
[![Build Status](https://travis-ci.com/sotberd/s3hive.svg?branch=main)](https://travis-ci.com/sotberd/s3hive)
[![codecov](https://codecov.io/gh/sotberd/s3hive/branch/main/graph/badge.svg)](https://codecov.io/gh/sotberd/s3hive) -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

s3hive is a Python tool that provides a high-level interface for working with S3 buckets. With this tool, you can easily perform common operations on your S3 buckets such as creating, deleting, listing, uploading files, etc.

This tool uses the popular boto3 library to interact with the S3 API, making it simple and intuitive to use.

s3hive is designed to be easy to use, with a simple and consistent API that abstracts away many of the complexities of working with S3 buckets. Whether you're a seasoned developer or just getting started, s3hive can help you streamline your S3 operations and save time.

## Features

- Create a new S3 bucket
- Delete an existing S3 bucket
- Generate a presigned URL to share an S3 object
- List all S3 buckets
- Upload files to an S3 bucket
- Download files from an S3 bucket
- List files in an S3 bucket
- Delete files from an S3 bucket

This tool is a wrapper around the boto3 library. It provides a simple interface to manage your S3 buckets.

## Getting Started

### Installation

You can install s3hive using pip:

```bash
$ pip install s3hive
```

### Usage

Here's an example of how to use s3hive to list all your S3 buckets:

```python
import s3hive as s3
import os

ENDPOINT_URL = os.environ.get('ENDPOINT_URL')
REGION = os.environ.get('REGION')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3hive = s3.Bucket(
    endpoint_url=ENDPOINT_URL,
    region=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

buckets = s3hive.list_buckets()

print(buckets)

# Output:
# [{
#      'name': 'bucket1',
#      'creation_date': datetime.datetime(2020, 5, 1, 12, 0, 0, tzinfo=tzutc())
# }]

```

For more examples and detailed documentation, please visit our [GitHub repository](https://github.com/sotberd/s3hive/blob/main/example.py).

### Methods

| Method                                                                                               | Description                                                                                                                                                                                                                                                                                                                                                                      |
| :--------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_get_client()`                                                                                      | Get the S3 client. Returns a boto3 client object for the S3 service.                                                                                                                                                                                                                                                                                                             |
| `create_bucket(bucket: str, acl: str = "private")`                                                   | Create an S3 bucket in a specified region. bucket is the name of the bucket to create, and acl is the access control list. Returns True if the bucket was created successfully, or raises an exception if an error occurs.                                                                                                                                                       |
| `delete_bucket(bucket: str) `                                                                        | Delete an S3 bucket. bucket is the name of the bucket to delete. Returns True if the bucket was deleted successfully, or raises an exception if an error occurs.                                                                                                                                                                                                                 |
| `list_buckets(names_only: bool = False)`                                                             | List all buckets in the S3 account. If names_only is True, return only the bucket names. Otherwise, return a list of dictionaries, with each dictionary containing the bucket name and creation date. Raises an exception if an error occurs.                                                                                                                                    |
| `list_objects(bucket: str, keys_only: bool = False)`                                                 | List all objects in the specified bucket. If keys_only is True, return only the object keys. Otherwise, return a list of dictionaries, with each dictionary containing the object key, size, and last modified date. Raises an exception if an error occurs.                                                                                                                     |
| `create_presigned_url(bucket: str, key: str, expiration: int = 3600)`                                | Generate a presigned URL to share an S3 object. bucket is the name of the bucket containing the object, key is the object key, and expiration is the time in seconds for the presigned URL to remain valid. Returns the presigned URL as a string, or raises an exception if an error occurs.                                                                                    |
| `upload(bucket: str, file_name: str, key: str = None, extraArgs: dict = None, filesize: int = None)` | Upload an object to an S3 bucket. file_name is the path to the file to upload, bucket is the name of the bucket to upload to, key is the S3 object name. If not specified, then file_name is used. extraArgs is a dictionary of extra arguments that may be passed to the S3 API. Returns True if the file was uploaded successfully, or raises an exception if an error occurs. |
| `download(bucket: str, key: str, local_dir: str = ROOT_DIR)`                                         | Download an object from S3 bucket to local directory. key is the S3 object key, and local_dir is the local directory to download the file to (if local_dir not provided object will stored on the root folder). Returns True if the file was downloaded successfully, or raises an exception if an error occurs.                                                                 |
| `delete(bucket: str, key: str)`                                                                      | Delete an object from an S3 bucket. bucket is the name of the bucket containing the object, and key is the object key. Returns True if the object was deleted successfully, or raises an exception if an error occurs.                                                                                                                                                           |

## License

s3hive is licensed under the [MIT License](https://opensource.org/license/mit/).
