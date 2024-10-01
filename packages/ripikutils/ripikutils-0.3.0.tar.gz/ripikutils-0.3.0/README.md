# ripikutils

ripikutils is a Python package providing utility functions for MongoDB operations and AWS S3 interactions, specifically designed for internal use at Ripik Tech.

[![PyPI version](https://badge.fury.io/py/ripikutils.svg)](https://badge.fury.io/py/ripikutils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Creation of Secret Manager

Every secret manager added should follow these guidelines:

- ripikutils/{clientName}/{useCase}
- Data added inside the secret should atleast have these values
  - mongoURI
  - dbName
  - useCase
  - s3Bucket

## Installation

You can install ripikutils using pip:

```
pip install ripikutils
```

## Features

- MongoDB data filtering, inserting, updation, and deletion
- AWS S3 operations (upload, download)
- Temporary directory management for image processing

## Usage

### MongoDB Operations

#### Initialize Mongo Client

```python
from ripikutils.mongo import initialize_mongo

# Initialize a MongoDB client
mongo_client = initialize_mongo(client_name)
```

#### Apply Filter

```python
from ripikutils.mongo import apply_basic_filter

# Apply basic filter to your MongoDB query
filtered_data = apply_filter(collection, filter_params)
```

#### Insert Document

```python
from ripikutils.mongo import insert

# Insert a document into your MongoDB collection
insert(collection, document)
```

#### Update Document

```python
from ripikutils.mongo import update

# Update a document in your MongoDB collection
update(collection, filter_params, update_params)
```

#### Delete Document

```python
from ripikutils.mongo import delete

# Delete a document from your MongoDB collection
delete(collection, filter_params)
```

### AWS S3 Operations

#### Upload Object/File

```python
from ripikutils.aws import upload_s3_object

# Upload a file to S3
upload_s3_object(file_path, bucket_name, object_name)
```

#### Download Object/File

```python
from ripikutils.aws import download_s3_object

# Download a file from S3
download_s3_object(bucket_name, object_name, local_file_path)
```

#### Delete Object/File

```python
from ripikutils.aws import delete_s3_object

# Delete a file from S3
delete_s3_object(bucket_name, object_name)
```

#### Get Presigned URL

```python
from ripikutils.aws import get_presigned_url

# Get a presigned URL for a file in S3
presigned_url = get_presigned_url(bucket_name, object_name)
```

#### List Objects in S3 Bucket

```python
from ripikutils.aws import list_s3_objects

# List objects in a S3 bucket
objects = list_s3_objects(bucket_name)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or support, please contact the Ripik Tech team at [vaibhav@ripik.ai](mailto:vaibhav@ripik.ai).