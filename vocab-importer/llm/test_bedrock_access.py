import boto3
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def test_model_access(model_id):
    """
    Test if we can access a specific model in AWS Bedrock
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    if not aws_access_key or not aws_secret_key:
        print("AWS credentials not found. Please set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return False
    
    # Create a Bedrock runtime client
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    try:
        # Test with a simple prompt
        if model_id.startswith("amazon."):
            # Claude models use the converse API
            inference_config = {
                "maxTokens": 100,
                "temperature": 0.7
            }
            
            messages = [
                {
                    "role": "user",
                    "content": [{"text": "Hello, can you hear me?"}]
                }
            ]
            
            response = client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig=inference_config
            )
            print(f"✅ Successfully accessed {model_id}")
            return True
            
        elif model_id.startswith("anthropic."):
            # Amazon models use the invoke_model API
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps({
                    "inputText": "Hello, can you hear me?",
                    "textGenerationConfig": {
                        "maxTokenCount": 100,
                        "temperature": 0.7
                    }
                })
            )
            print(f"✅ Successfully accessed {model_id}")
            return True
            
        else:
            print(f"❓ Unknown model type: {model_id}")
            return False
            
    except Exception as e:
        print(f"❌ Cannot access {model_id}: {str(e)}")
        return False

if __name__ == "__main__":
    # Test the models you're interested in
    models_to_test = [
        "anthropic.claude-3-5-haiku-20241022-v1:0",
        "amazon.nova-micro-v1:0",
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-instant-v1"
    ]
    
    print("Testing AWS Bedrock model access:")
    print("=" * 50)
    
    accessible_models = []
    
    for model in models_to_test:
        if test_model_access(model):
            accessible_models.append(model)
    
    print("\nAccessible models:")
    for model in accessible_models:
        print(f"- {model}") 