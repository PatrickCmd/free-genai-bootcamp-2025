# Use the Conversation API to send a text message to Anthropic Claude.

import boto3
import os
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()


aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client(
    "bedrock-runtime", 
    region_name="us-east-1",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

# Set the model ID, e.g., Claude 3 Haiku.
model_id = "anthropic.claude-3-5-haiku-20241022-v1:0"

# Start a conversation with the user message.
user_message = "Describe the purpose of a 'hello world' program in one line."
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text.
    response_text = response["output"]["message"]["content"][0]["text"]
    print(response_text)

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)


