from ...secrets.secrets_manager import get_secret
import boto3

class S3Client:
    def __init__(self, client_name: str, usecase: str = None):
        self.client_name = client_name
        self.usecase = usecase
        self.secrets = get_secret(f"ripikutils/{client_name}/{usecase}")
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.secrets['aws_access_key_id'],
            aws_secret_access_key=self.secrets['aws_secret_access_key'],
            region_name=self.secrets['region_name']
        )

    def upload_object(self, file_path, bucket_name, object_key):
        """Upload a file to S3."""
        try:
            self.s3.upload_file(file_path, bucket_name, object_key)
            print(f"Uploaded {file_path} to {bucket_name}/{object_key}")
        except Exception as e:
            print(f"Error uploading {file_path} to S3: {e}")

    def download_object(self, bucket_name, object_key, download_path):
        """Download an object from S3 to a local path."""
        try:
            self.s3.download_file(bucket_name, object_key, download_path)
            print(f"Downloaded {object_key} from {bucket_name} to {download_path}")
        except Exception as e:
            print(f"Error downloading {object_key}: {e}")

    def delete_object(self, bucket_name, object_key):
        """Delete an object from S3."""
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_key)
            print(f"Deleted {object_key} from {bucket_name}")
        except Exception as e:
            print(f"Error deleting {object_key} from {bucket_name}: {e}")

    def list_objects(self, bucket_name, prefix=None):
        """List objects in an S3 bucket."""
        try:
            response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            objects = [obj['Key'] for obj in response.get('Contents', [])]
            return objects
        except Exception as e:
            print(f"Error listing objects in {bucket_name}: {e}")
            return []

    def get_presigned_url(self, bucket_name, object_key, expiration=3600):
        """Generate a presigned URL to share an S3 object."""
        try:
            url = self.s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name, 'Key': object_key},
                                                  ExpiresIn=expiration)
            return url
        except Exception as e:
            print(f"Error generating presigned URL: {e}")
            return None

def initialize_s3(client_name: str, usecase: str = None):
    return S3Client(client_name, usecase)