def delete_s3_object(s3Client, bucket_name, object_key):
    """Delete an object from S3."""
    s3 = s3Client
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        print(f"Deleted {object_key} from {bucket_name}")
    except Exception as e:
        print(f"Error deleting {object_key} from {bucket_name}: {e}")