#!/bin/bash

# Test script for the Chat Completion API service
# This sends a request to the chat service running on port 8888

# Set variables
HOST="localhost"
PORT="8888"
ENDPOINT="/v1/chatqna"
URL="http://${HOST}:${PORT}${ENDPOINT}"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}Testing Chat Completion API at ${URL}${NC}"
echo "---------------------------------------"

# JSON payload for the request - mimicking OpenAI API format
# Adjust parameters as needed based on your implementation
read -r -d '' PAYLOAD << EOM
{
  "model": "llama3.2:3b",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "What is OPEA?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 150,
  "stream": false
}
EOM

# Make the curl request
echo "Sending request..."
echo -e "${GREEN}Request payload:${NC}"
echo "$PAYLOAD" | jq . 2>/dev/null || echo "$PAYLOAD"
echo "---------------------------------------"

# Execute the curl command with error handling
RESPONSE=$(curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

# Check if curl executed successfully
if [ $? -ne 0 ]; then
  echo -e "${RED}Error: Failed to connect to the service.${NC}"
  echo "Make sure the service is running at ${URL}"
  exit 1
fi

# Print the response
echo -e "${GREEN}Response:${NC}"
echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"

# Check if the response is empty or contains an error
if [[ -z "$RESPONSE" ]]; then
  echo -e "${RED}Error: Empty response received.${NC}"
  exit 1
fi

if [[ "$RESPONSE" == *"error"* ]]; then
  echo -e "${RED}Error detected in response.${NC}"
fi

echo "---------------------------------------"
echo -e "${GREEN}Test completed.${NC}" 