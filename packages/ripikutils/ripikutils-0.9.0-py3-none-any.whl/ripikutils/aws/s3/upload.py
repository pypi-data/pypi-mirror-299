def upload_s3_object(s3Client, file_path, bucket_name, object_key):
    """Upload a file to S3."""
    s3 = s3Client
    try:
        s3.upload_file(file_path, bucket_name, object_key)
        print(f"Uploaded {file_path} to {bucket_name}/{object_key}")
    except Exception as e:
        print(f"Error uploading {file_path} to S3: {e}")