import boto3
import pandas as pd
import os
import pathlib


def upload_to_aws(local_file, bucket_name, s3_file):
    s3 = boto3.client("s3")
    try:
        s3.upload_file(local_file, bucket_name, s3_file)
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': "aws-data-pipeline-team3",
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
