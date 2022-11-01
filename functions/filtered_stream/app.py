from filtered_stream import get_rules,set_rules,get_stream
import json
def lambda_handler(event, context):
    rules = get_rules()
    set = set_rules(rules)
    data = get_stream(set, context=context dir=event['dir'])
    return {
            "statusCode": 200,
            "body": json.dumps({
                "message": data # invoke layer function
            }),
    }
