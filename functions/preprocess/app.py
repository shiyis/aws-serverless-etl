from preprocess import df_apply
import json
import signal 

def lambda_handler(event, context):
    timeout  = signal.alarm((context.get_remaining_time_in_millis() / 1000) - 1)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": df_apply(event) # invoke layer function
        }),
    }
