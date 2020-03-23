import os
import logging

aws_access_key = os.environ.get("AWS_ACCESS_KEY", "")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
aws_access_token = os.environ.get("AWS_SESSION_TOKEN", "")
aws_region = os.environ.get("AWS_REGION", "us-west-2")
aws_host = os.environ.get("AWS_HOST", "")
aws_profile_name = os.environ.get("AWS_PROFILE_NAME", "")
aws_api_endpoint = os.environ.get("AWS_API_ENDPOINT", "")

logger = logging.getLogger(__name__)
logger.info(f"config.py, aws_access_key: {aws_access_key}")
logger.info(f"         aws_api_endpoint: {aws_api_endpoint}")
