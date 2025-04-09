def is_oss_valid(oss_config: dict) -> bool:
    """
    Validates the OSS (Object Storage Service) configuration.

    Args:
        oss_config (dict): A dictionary containing the OSS configuration with the following keys:
            - access_key_id (str): The access key ID for authentication.
            - access_key_secret (str): The secret key for authentication.
            - endpoint (str): The endpoint URL of the OSS service.
            - bucket_name (str): The name of the OSS bucket.

    Returns:
        bool: True if all required fields are non-empty, False otherwise.
    """
    access_key_id = oss_config['access_key_id']
    access_key_secret = oss_config['access_key_secret']
    endpoint = oss_config['endpoint']
    bucket_name = oss_config['bucket_name']
    return access_key_id is not None and len(access_key_id) > 0 and access_key_secret is not None and len(
        access_key_secret) > 0 and endpoint is not None and len(endpoint) > 0 and bucket_name is not None and len(
        bucket_name) > 0
