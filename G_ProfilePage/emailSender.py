import json
import boto3
import logging
from botocore.exceptions import ClientError

# Define the AWS region
AWS_REGION = "us-west-2"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create an SES client
ses_client = boto3.client('ses', region_name=AWS_REGION)

def lambda_handler(event, context):
    logger.info('Received event: %s', json.dumps(event))

    try:
        if 'body' not in event or not event['body']:
            raise ValueError("Missing body in the event")

        # Parse JSON body
        data = json.loads(event['body'])
        fullName = data['fullName']
        email = data['email']
        message = data['message']

        sender_email = "felipenogueraprieto@gmail.com"  # email verified in SES
        recipient_email = "felipenogueraprieto@gmail.com"  # Recipient's email address
        subject = "Message from {}".format(fullName)
        body = f"""
        You have received a new message from {fullName} ({email}):
        
        {message}
        """

        # Send the email
        response = ses_client.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Update this for production
            },
            'body': json.dumps({'message': 'Email sent successfully!'})
        }

    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Error sending the email'})
        }

    except KeyError as e:
        logger.error('Bad input data: Missing key %s', e)
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': f'Bad input data: Missing key {e}'})
        }

    except ValueError as e:
        logger.error('Bad request: %s', e)
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }