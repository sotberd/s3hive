import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
import os
from typing import List, Tuple, Dict

# Root directory of the project (used for relative paths)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

class Bucket:
    """
    The Bucket class is a wrapper for the boto3 S3 client.
    It contains methods for listing objects, downloading files, uploading files, deleting objects, etc from the bucket.
    The class is initialized with the endpoint URL, region, AWS access key ID, and AWS secret access key. 
    These credentials are required to authenticate requests to the S3 bucket. 
    The class is designed to provide a simple and intuitive interface for working with S3 buckets, while hiding the complexity of the underlying API calls.
    """
    def __init__(
        self,
        endpoint_url: str,
        region: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
    ) -> None:
        """
        Initialize the S3 bucket.

        :param endpoint_url: Endpoint URL for the S3 service.
        :param region: The AWS region the S3 bucket is located in.
        :param aws_access_key_id: The AWS access key ID for authentication.
        :param aws_secret_access_key: The AWS secret access key for authentication.
        """
        self.endpoint_url = endpoint_url
        self.region = region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def _get_client(self) -> boto3.client:
        """
        Returns a boto3 client object for the S3 service.

        :return: A boto3 client object.
        """
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            region_name=self.region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
    
    def _client_error(self, e: ClientError)->None:
        """
        Raise exception if error occurs in boto3 client

        :param e: ClientError
        :return: None
        """
        raise Exception(e.response)

    def create_bucket(self, bucket:str, acl:str="private") -> bool:
        """
        Create an S3 bucket in a specified region

        :param bucket: Bucket to create
        :param acl: Access control list. Default is private
        :return: True if bucket was created, else raise an exception
        """
        s3_client = self._get_client()
        try:
            response = s3_client.create_bucket(
                Bucket=bucket,
                CreateBucketConfiguration={"LocationConstraint": self.region},
                ACL=acl,
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return True
            
        except ClientError as e:
            self._client_error(e)
    
    def delete_bucket(self, bucket:str) -> bool:
        """
        Delete an S3 bucket

        :param bucket: Bucket to delete
        :return: True if bucket was deleted, else raise an exception
        """

        s3_client = self._get_client()
        try:
            reponse = s3_client.delete_bucket(Bucket=bucket)
            if reponse["ResponseMetadata"]["HTTPStatusCode"] == 204:
                return True
            
        except ClientError as e:
            self._client_error(e)
        
    def list_buckets(self, names_only:bool = False) -> List:
        """
        List buckets in S3 account that you have access to by your credentials
        
        :param names_only: if True return only bucket names
        :return: list of buckets. If error, else raise an exception
        """

        s3_client = self._get_client()
        try:
            response = s3_client.list_buckets()
            if not names_only:
                return response["Buckets"]
            return [bucket["Name"] for bucket in response["Buckets"]]
        
        except ClientError as e:
            self._client_error(e)
        
    def list_objects(self,bucket:str, keys_only=False) -> List:
        """
        List objects in bucket
        
        :param keys_only: if True return only keys of objects
        :return: list of objects. If error, raise an exception 
        """
        client = self._get_client()
        try:
            response = client.list_objects_v2(Bucket=bucket)

            if not keys_only:
                return response["Contents"]
            
            return [obj["Key"] for obj in response["Contents"]]

        except ClientError as e:
           self._client_error(e)
                
    def create_presigned_url(self,bucket:str, key:str, expiration:int=3600) -> str:
        """
        Generate a presigned URL to share an S3 object

        :param bucket: The bucket name.
        :param key: The object key.
        :param expiration: Time in seconds for the presigned URL to remain valid. Default is 3600 seconds.
        :return: Presigned URL as string. else raise an exception
        """

        # Generate a presigned URL for the S3 object
        s3_client = self._get_client()
        try:
            return s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket,
                                                                'Key': key},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            self._client_error(e)
    
    def upload(self,bucket:str, file_name:str, key:str=None, extra_args: Dict[str, str] = None,filesize:int=None) -> bool:
        """
        Upload an object to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param key: S3 object name. If not specified then file_name is used
        :param extraArgs: Extra arguments that may be passed to the S3 API
        :return: True if file was uploaded, else raise an exception
        """
        s3_client = self._get_client()

        # If S3 key was not specified, use file_name
        if key is None:
            key = os.path.basename(file_name)

        # Calculate the size of the file
        if filesize is None:
            try: 
                file_size = os.path.getsize(file_name)
            except FileNotFoundError:
                pass

        # Upload the file
        try:
            with tqdm(
                total=file_size,
                desc=f"Uploading {file_name} to {bucket}",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                colour="cyan",
                bar_format="{l_bar}{bar:10}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
            ) as pbar:
               response = s3_client.upload_file(
                    file_name,
                    bucket,
                    key,
                    Callback=lambda bytes_transferred: pbar.update(bytes_transferred),
                    ExtraArgs=extra_args,
                )

            if response is None:
                return True

        except ClientError as e:
           self._client_error(e)

    def download(self, bucket:str, key: str, local_dir: str=ROOT_DIR) -> bool:
        """
        Download an object from S3 bucket to local directory
        
        :param key: S3 object key
        :param local_dir: local directory to download the file to
        :return: True if file was uploaded, else raise an exception
        """
        client = self._get_client()

        # create local directory if not exists
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        try:
            response = client.head_object(
                Bucket=bucket,
                Key=key,
                ExpectedBucketOwner=self.aws_access_key_id,
            )
            total_size = response["ContentLength"] / 1024 / 1024

            # get local file path to download to
            local_file = os.path.join(local_dir, os.path.basename(key))

            with tqdm(
                total=round(total_size, 2),
                desc=f"Downloading to {local_file}",
                unit="MB",
                colour="cyan",
                bar_format="{l_bar}{bar:10}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
            ) as pbar:
               response =  client.download_file(
                    bucket,
                    key,
                    local_file,
                    Callback=lambda bytes_transferred: pbar.update(
                        round(bytes_transferred / 1024 / 1024, 2)
                    ),
                )
               
            if response is None:
                return True
            
        except ClientError as e:
            self._client_error(e)

    def delete(self, bucket:str, key:str) -> Tuple[bool, dict]:
        """
        Delete an object from an S3 bucket

        :param key: S3 object key
        :return: A tuple of (marker, metada) if object was deleted succefully, else raise an exception
        """
        s3_client = self._get_client()

        try:
           response =  s3_client.delete_object(Bucket=bucket, Key=key)
           if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
            marker = response["DeleteMarker"] if "DeleteMarker" in response else False
            metadata = response["ResponseMetadata"]
            return marker, metadata
            
        except ClientError as e:
            self._client_error(e)
        

