# LLM module initialization
from . import openai, anthropic, groq, bedrock

def generate_vocabulary(theme, count, provider, model, temperature=0.7, max_tokens=2000):
    """
    Generate vocabulary using the specified LLM provider
    
    Args:
        theme (str): The theme or category for vocabulary generation
        count (int): Number of vocabulary items to generate
        provider (str): LLM provider (OpenAI, Anthropic, Groq, AWS Bedrock)
        model (str): Model name for the selected provider
        temperature (float): Creativity parameter (0.0 to 1.0)
        max_tokens (int): Maximum tokens in the response
        
    Returns:
        list: List of vocabulary items
    """
    if provider == "OpenAI":
        return openai.generate_vocabulary(theme, count, model, temperature, max_tokens)
    elif provider == "Anthropic":
        return anthropic.generate_vocabulary(theme, count, model, temperature, max_tokens)
    elif provider == "Groq":
        return groq.generate_vocabulary(theme, count, model, temperature, max_tokens)
    elif provider == "AWS Bedrock":
        return bedrock.generate_vocabulary(theme, count, model, temperature, max_tokens)
    else:
        raise ValueError(f"Unsupported provider: {provider}")

def check_api_status():
    """
    Check the status of all LLM API connections
    
    Returns:
        dict: Status of each provider (True if connected, False otherwise)
    """
    status = {}
    
    # Check OpenAI
    try:
        openai.get_client()
        status["OpenAI"] = True
    except Exception:
        status["OpenAI"] = False
    
    # Check Anthropic
    try:
        anthropic.get_client()
        status["Anthropic"] = True
    except Exception:
        status["Anthropic"] = False
    
    # Check Groq
    try:
        groq.get_client()
        status["Groq"] = True
    except Exception:
        status["Groq"] = False
    
    # Check AWS Bedrock
    try:
        bedrock.get_client()
        status["AWS Bedrock"] = True
    except Exception:
        status["AWS Bedrock"] = False
    
    return status 