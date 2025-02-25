import os
import json
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_client():
    """
    Initialize and return an AWS Bedrock client
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    
    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not found. Please set the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
    
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

def generate_vocabulary(theme, count, model="anthropic.claude-3-sonnet", temperature=0.7, max_tokens=2000):
    """
    Generate vocabulary items using AWS Bedrock models
    
    Args:
        theme (str): The theme or category for vocabulary generation
        count (int): Number of vocabulary items to generate
        model (str): AWS Bedrock model to use
        temperature (float): Creativity parameter (0.0 to 1.0)
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        list: List of vocabulary items
    """
    client = get_client()
    
    prompt = f"""
    You are a language expert specializing in Jamaican Patois. Your task is to generate vocabulary items for learning Jamaican Patois based on the theme: {theme}.

    For each vocabulary item, provide:
    1. The Jamaican Patois word or phrase
    2. The English translation
    3. Part of speech (noun, verb, adjective, phrase, etc.)
    4. (Optional) Usage notes or context

    Generate {count} vocabulary items that are authentic, commonly used, and appropriate for language learners.

    Format your response as a JSON array with the following structure for each item:
    {{
      "jamaican_patois": "word/phrase",
      "english": "translation",
      "parts": {{
        "type": "part of speech",
        "usage": "usage notes (optional)"
      }}
    }}
    """
    
    try:
        # Different models have different request formats
        if model.startswith("anthropic.claude"):
            # Claude models
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "system": "You are a Jamaican Patois language expert.",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        elif model.startswith("cohere"):
            # Cohere models
            request_body = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
        elif model.startswith("amazon.titan"):
            # Amazon Titan models
            request_body = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature
                }
            }
        else:
            raise ValueError(f"Unsupported model: {model}")
        
        response = client.invoke_model(
            modelId=model,
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        
        # Extract content based on model type
        if model.startswith("anthropic.claude"):
            content = response_body['content'][0]['text']
        elif model.startswith("cohere"):
            content = response_body['generations'][0]['text']
        elif model.startswith("amazon.titan"):
            content = response_body['results'][0]['outputText']
        else:
            content = str(response_body)
        
        return content
        
    except Exception as e:
        raise Exception(f"Error generating vocabulary with AWS Bedrock: {str(e)}") 