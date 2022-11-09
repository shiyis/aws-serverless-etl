from preprocess import df_apply
import json
<<<<<<< HEAD
import signal 
def lambda_handler(event, context):
    return df_apply(event)
=======

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": df_apply(event) # invoke layer function
        }),
    }
>>>>>>> main
