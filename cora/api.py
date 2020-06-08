import os
import json
import requests
from typing import Text, Union
from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Response
from cora import config
import logging

from cora.models import UserRecord, SurveyResponse
from cora.responses import UserRecordResponse

SIGV4_HEADERS: AWSRequestsAuth = AWSRequestsAuth(
    aws_access_key=config.aws_access_key,
    aws_secret_access_key=config.aws_secret_access_key,
    aws_host=config.aws_host,
    aws_region=config.aws_region,
    aws_service="execute-api",
)

API_ENDPOINT = config.aws_api_endpoint

logger = logging.getLogger(__name__)
logger.info(f"api.py, aws_access_key: {config.aws_access_key}")
logger.info(f"api.py, API_ENDPOINT: {API_ENDPOINT}")


def get_user_records(user_id: Text) -> Union[Response, UserRecordResponse]:
    response: Response = requests.get(
        API_ENDPOINT + "/users" + "?userId={}".format(user_id), auth=SIGV4_HEADERS
    )
    if response.status_code == 200:
        return UserRecordResponse().load_from_model(response.json())
    else:
        return response


def put_user_record(record: UserRecord) -> Response:
    print(json.dumps(record.to_dynamo_model()))
    return requests.post(
        API_ENDPOINT + "/users", json=record.to_dynamo_model(), auth=SIGV4_HEADERS
    )


def put_survey_response(response: SurveyResponse) -> Response:
    print(json.dumps(response.to_dynamo_model()))
    return requests.post(
        API_ENDPOINT + "/surveys", json=response.to_dynamo_model(), auth=SIGV4_HEADERS
    )


if __name__ == "__main__":
    from cora.models import Symptom

    user_record = UserRecord(
        "14252210134",
        1500000000,
        "+14252210134",
        26,
        "98028",
        1500000000,
        "Male",
        True,
        True,
        False,
        [
            Symptom(
                "Fever",
                1500000000,
                None,
                8,
                "I have chills and my temperature is 100.3",
            )
        ],
    )

    print(put_user_record(user_record).text)
    print(get_user_records(user_record.user_id).data[0].symptoms[0].description)
