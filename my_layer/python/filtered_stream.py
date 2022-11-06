import requests
import os
import json
import boto3
from time import time
# To set your enviornment variables in your terminal run the following line:
# aws ssm put-parameter --name /twitter-data-pipeline/bearer_token --value <your bearer token value> --type SecureString --overwrite
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
# SSM_PARAMETER_PREFIX = os.getenv("SSM_PARAMETER_PREFIX")
# bearer_token = '/data-pipeline-team3/bearer_token'
SSM = boto3.client('ssm', region_name="us-east-1")
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    # parameter_names = [
    #         bearer_token,
    # ]
    # result = SSM.get_parameters(
    #     Names=parameter_names,
    #     WithDecryption=True
    # )

    # if result['InvalidParameters']:
    #     raise RuntimeError(
    #         'Could not find expected SSM parameters containing Twitter API keys: {}'.format(parameter_names))


    # param_lookup = {param['Name']: param['Value'] for param in result['Parameters']}
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))
    return response.json()


def get_all_rules(rules):
    if rules is None or "data" not in rules:
        return None
    sample_rulees = [
        {"value": "artist", "tag": "music artist"},
    ]

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": sample_rulees}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # print(json.dumps(response.json()))


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    # print(json.dumps(response.json()))

def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "music -(has:links OR is:retweet) lang:en", "tag": "music genre"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    # print(json.dumps(response.json()))


def get_stream(set, context=None, dir="../output/"):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    l = []
    count = 0
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            data = tuple((json_response["data"]["id"], json_response["data"]["text"]))
            l.append(data)
            count += 1
            if count >= 5:
                break
    return l