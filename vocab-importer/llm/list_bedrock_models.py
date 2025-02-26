import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def list_available_models():
    """
    List all available models in AWS Bedrock for the current account
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    if not aws_access_key or not aws_secret_key:
        print("AWS credentials not found. Please set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        return
    
    # Create a Bedrock client
    bedrock = boto3.client(
        service_name='bedrock',  # Note: this is 'bedrock', not 'bedrock-runtime'
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    
    try:
        # List foundation models
        response = bedrock.list_foundation_models()
        
        print("Available models in AWS Bedrock:")
        print("=" * 50)
        
        for model in response.get('modelSummaries', []):
            model_id = model.get('modelId', 'Unknown')
            provider = model.get('providerName', 'Unknown')
            status = model.get('modelLifecycle', {}).get('status', 'Unknown')
            
            # Check if the model is available for use
            if status == 'ACTIVE':
                print(f"✅ {model_id} (Provider: {provider})")
            else:
                print(f"❌ {model_id} (Provider: {provider}, Status: {status})")
        
        print("\nNote: You can only use models marked with ✅")
        
    except Exception as e:
        print(f"Error listing models: {str(e)}")

if __name__ == "__main__":
    list_available_models() 