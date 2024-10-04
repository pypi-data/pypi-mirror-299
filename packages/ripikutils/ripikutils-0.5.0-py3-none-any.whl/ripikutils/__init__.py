from .mongo import initialize_mongo
from .mongo import example_usage as example_usage_mongo
from .aws.s3 import initialize_s3
from .aws.s3 import example_usage as example_usage_s3

__all__ = [
    'aws',
    'mongo',
]

__version__ = "0.5.0"

# AWS submodule
class aws:
    initialize = initialize_s3 
    check = example_usage_s3.check

# Mongo submodule
class mongo:
    initialize = initialize_mongo
    check = example_usage_mongo.check