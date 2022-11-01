import requests
import os
import json
import csv
import boto3
from time import time
import signal, logging
# To set your enviornment variables in your terminal run the following line:
# aws ssm put-parameter --name /twitter-data-pipeline/bearer_token --value <your bearer token value> --type SecureString --overwrite

# SSM_PARAMETER_PREFIX = os.getenv("SSM_PARAMETER_PREFIX")
bearer_token = '/data-pipeline-team3/bearer_token'
SSM = boto3.client('ssm')
def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    parameter_names = [
            bearer_token,
    ]
    result = SSM.get_parameters(
        Names=parameter_names,
        WithDecryption=True
    )

    if result['InvalidParameters']:
        raise RuntimeError(
            'Could not find expected SSM parameters containing Twitter API keys: {}'.format(parameter_names))


    param_lookup = {param['Name']: param['Value'] for param in result['Parameters']}
    r.headers["Authorization"] = f"Bearer {param_lookup[bearer_token]}"
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
    print(json.dumps(response.json()))
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
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "music", "tag": "music genre"},
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
    print(json.dumps(response.json()))


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
    header = ['id', 'text']
    logging.info("there are {} seconds left".format(int(context.get_remaining_time_in_millis() / 1000) - 1))
    while int(context.get_remaining_time_in_millis() / 1000) - 1 > 0:
        try: 
            logging.info('Testing stuff')
            # Do work


            with open(dir + 'out.csv', 'w',encoding='UTF8') as f:
                writer = csv.writer(f)

                # write the header
                writer.writerow(header)

                # write the data
                for response_line in response.iter_lines():
                    if response_line:
                        json_response = json.loads(response_line)
                        obj = json.dumps(json_response, indent=4, sort_keys=True)
                        l.append(obj)
                        data = [json_response["data"]["id"],json_response["data"]["text"]]
                        writer.writerow(data)
        except TimeoutError:
            logging.info("time is up!")

    print("file dir exists:", os.path.isfile(dir + 'out.csv'))
    # signal.alarm(0)# This line fixed the issue above!
    return {'statusCode': 200, 'body': l[0]["text"]}


