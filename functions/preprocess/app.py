# from preprocess import df_apply
import json
import signal 
from . import preprocess
def lambda_handler(event, context):
    return preprocess.df_apply(event.Paylaod.stream_results)
