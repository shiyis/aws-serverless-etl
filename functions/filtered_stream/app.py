import requests
import os
import json
import pandas as pd
import boto3
from time import time 

# To set your enviornment variables in your terminal run the following line:
# aws ssm put-parameter --name /twitter-data-pipeline/bearer_token --value <your bearer token value> --type SecureString --overwrite
# SSM_PARAMETER_PREFIX = os.getenv("SSM_PARAMETER_PREFIX")
# bearer_token = '/{}/bearer_token'.format(SSM_PARAMETER_PREFIX)
# SSM = boto3.client('ssm')
bearer_token = os.getenv("BEARER_TOKEN")
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
    r.headers["Authorization"] = f"Bearer {bearer_token}"
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


def get_stream(set, end=int(time())+3):
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
    df = pd.DataFrame(columns=["id", "text"])
    
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            obj = json.dumps(json_response, indent=4, sort_keys=True)
            print(json_response["data"]["id"])
            item = {
                "id": json_response["data"]["id"],
                "text": json_response["data"]["text"],
            }
            df = df.append(item, ignore_index=True)
            l.append(json_response)
            df.to_csv("out.csv")
            break

    return l

def lambda_handler(event, context):
    client = boto3.client("lambda")

    rules = get_rules()
    set = set_rules(rules)
    data = get_stream(set)

    # file = pd.read_csv("./out.csv")
    # inputParams = {
    #     "file": file
    # }

    # response = client.invoke(
    #     FunctionName = 'arn:aws:lambda:<region>:<account id>:function:preprocess',
    #     InvocationType = 'RequestResponse',
    #     Payload = json.dumps(inputParams)
    # )
    
    # responseFromChild = json.laod(response['Payload'])
    
    # client.invoke(
    #     FunctionName = 'arn:aws:lambda:<region>:<account id>:function:load_data',
    #     InvocationType = 'Event',
    #     Payload = json.dumps(responseFromChild["file"])
    # )
    return data