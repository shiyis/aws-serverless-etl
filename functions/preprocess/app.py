from preprocess import df_apply
import json
import signal 
def lambda_handler(event, context):
    return df_apply(event)
