import boto3
from datetime import datetime
import pandas as pd 
import os 
import pathlib

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def upload_to_aws(local_file, bucket_name, s3_file):
    s3 = boto3.client("s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': os.environ['BUCKET_NAME'],
                'Key': s3_file
            },
            ExpiresIn=24 * 3600
        )

        print("Upload Successful", url)
        return url
    except FileNotFoundError:
        print("The file was not found")
        return None
    except ValueError:
        print("Credentials not available")
        return None

def lambda_handler(event,context):
    # df = event.get("file")
    # localFile = '/tmp/{}'.format(os.path.basename("out.csv"))
    # localFile = os.path.join(pathlib.Path(__file__).parent.resolve(), "out.csv")
    # print(localFile)
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_name =  'twitter-data-raw_'+dt_string +'.csv'
    url = upload_to_aws("./out.csv", "aws-data-pipeline-team3", csv_file_name)

    return url


lambda_handler("","")