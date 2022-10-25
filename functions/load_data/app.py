import boto3
import csv
from io import StringIO
from datetime import datetime
import filtered_stream

def upload_to_aws(local_file, bucket_name, s3_file):
    s3 = boto3.client('s3')

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
    df = event.get("file")
    df.to_csv("out.csv")
    localFile = '/tmp/{}'.format(os.path.basename("out.csv"))
    dt_string = datetime.now().strftime("%Y-%m-%d_%H%M")
    csv_file_name =  'trending-tickers_'+dt_string +'.csv'
    upload_to_aws(localFile, "aws-data-pipeline",csv_file_name)
