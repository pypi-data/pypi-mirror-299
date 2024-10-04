def download_s3_object(s3Client, bucket_name, object_key, download_path):
    """Download an object from S3 to a local path."""
    s3 = s3Client
    try:
        s3.download_file(bucket_name, object_key, download_path)
        print(f"Downloaded {object_key} from {bucket_name} to {download_path}")
    except Exception as e:
        print(f"Error downloading {object_key}: {e}")