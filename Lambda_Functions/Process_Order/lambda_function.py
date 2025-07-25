import json
import boto3
import os

ses_client = boto3.client('ses')
sns_client = boto3.client('sns')

# !! IMPORTANT !! Change this to your verified SES email address
SENDER_EMAIL = 'raju@gmail.com'  # change this email with your verified email for successful compilation/deployment
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    order_details = event
    order_id = order_details.get('orderId', 'N/A')
    customer_email = order_details.get('customerEmail')

    if not customer_email:
        raise ValueError("customerEmail is a required field.")

    try:
        # Send email via SES
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [customer_email]},
            Message={
                'Subject': {'Data': f'Order Confirmation: {order_id}'},
                'Body': {'Text': {'Data': f'Thank you for your order! Your order ID is {order_id}.'}}
            }
        )
        # Publish notification to SNS
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=f'New order processed: Order ID {order_id} for customer {customer_email}.',
            Subject='New Order Processed'
        )
        return {'statusCode': 200, 'body': json.dumps(f'Successfully processed order {order_id}')}
    except Exception as e:
        print(f"Error processing order: {e}")
        raise e