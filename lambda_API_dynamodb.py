import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    body = None
    status_code = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        if event['routeKey'] == "DELETE /items/{id}":
            response = dynamodb.delete_item(
                TableName="crud-table",
                Key={
                    'id': {'S': event['pathParameters']['id']}
                }
            )
            body = f"Deleted item {event['pathParameters']['id']}"
        elif event['routeKey'] == "GET /items/{id}":
            response = dynamodb.get_item(
                TableName="crud-table",
                Key={
                    'id': {'S': event['pathParameters']['id']}
                }
            )
            body = response
        elif event['routeKey'] == "GET /items":
            response = dynamodb.scan(TableName="crud-table")
            body = response
        elif event['routeKey'] == "PUT /items":
            request_json = json.loads(event['body'])
            response = dynamodb.put_item(
                TableName="crud-table",
                Item={
                    'id': {'S': request_json['id']},
                    'price': {'S': request_json['price']},
                    'name': {'S': request_json['name']}
                }
            )
            body = f"Put item {request_json['id']}"
        else:
            raise Exception(f"Unsupported route: {event['routeKey']}")
    except Exception as e:
        status_code = 400
        body = str(e)
    finally:
        body = json.dumps(body)

    return {
        'statusCode': status_code,
        'body': body,
        'headers': headers
    }
