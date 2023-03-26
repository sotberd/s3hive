import s3hive as s3
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
ENDPOINT_URL = os.getenv('ENDPOINT_URL')
REGION = os.getenv('REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

# Instantiate a Bucket object
s3hive = s3.Bucket(
    endpoint_url=ENDPOINT_URL,
    region=REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


# List all buckets
buckets = s3hive.list_buckets()
print(buckets)

# List all objects in a bucket
objects = s3hive.list_objects('my-bucket')
print(objects)

# Create a presigned URL
url = s3hive.create_presigned_url('my-bucket', 'my-object')
print(url)

# Upload an object
uploaded = s3hive.upload('my-bucket', 'my-object.yml', 'my-file.yml')
print(uploaded)

# Download an object
downloaded = s3hive.download('my-bucket', 'my-file.yml', )
print(downloaded)

# Delete an object
marker, metadata = s3hive.delete('my-bucket', 'my-file.yml')
print(marker, metadata)

