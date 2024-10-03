import boto3
from functools import wraps


def forge_local(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # define LocalStack service URL
        localstack_url = 'http://localhost:4566'

        # function that wraps the boto3 client and redirects to LocalStack
        def patched_boto3_client(service_name, *args, **kwargs):
            kwargs['endpoint_url'] = localstack_url
            # call the original boto3 client with modified client
            return boto3.Session().client(service_name, *args, **kwargs)

        boto3.client = patched_boto3_client

        try:
            # execute the decorated function
            result = func(*args, **kwargs)
        except Exception as e:
            raise e

        return result

    return wrapper
