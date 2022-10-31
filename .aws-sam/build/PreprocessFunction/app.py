from preprocess import df_apply
import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": df_apply() # invoke layer function
        }),
    }
