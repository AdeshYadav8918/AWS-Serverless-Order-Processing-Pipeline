import json
def lambda_handler(event, context):
    print("Heartbeat — Scheduler Triggered")
    return {'statusCode': 200, 'body': json.dumps("Heartbeat message logged.")}