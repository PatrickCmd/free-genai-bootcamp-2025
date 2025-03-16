## Ollama Setup

See steps setting up ollama in the [README](../README.md)


## Running the Mega Service

```sh
python app.py
```

```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": "What is Deep Learning?"
  }' \
  -o response.json
```

```sh
curl -X POST http://localhost:8000/v1/example-service \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": "What is Deep Learning?"
  }' | python -m json.tool
```

```sh
curl -X POST http://localhost:8000/v1/example-service \
    -H "Content-Type: application/json" \
    -d '{
        "messages": [
        {
            "role": "user",
            "content": "Hello, this is a test message"
        }
        ],
        "model": "test-model",
        "max_tokens": 1000,
        "temperature": 0.7
    }'
```

## OpenTelemetry Errors

These errors indicate that the OpenTelemetry exporter is attempting to send traces to `localhost:4318` but there's nothing running on that port to receive them. If you want to *completely* disable telemetry (tracing) so that OpenTelemetry does not try to export anything, you can do so by disabling the OpenTelemetry SDK at runtime.

---

### Quick Fix: Disable the OTel SDK at startup

One of the easiest ways is to tell OpenTelemetry to disable itself entirely. You can do this with an environment variable *before* your code initializes any tracing. For example:

### Via the command line

```bash
export OTEL_SDK_DISABLED=true
python your_app.py
```

### Or within your Python code (very early in the program)

```python
import os

os.environ["OTEL_SDK_DISABLED"] = "true"

# Then proceed to import and run the rest of your application
```

When `OTEL_SDK_DISABLED` is set to `true`, the OpenTelemetry instrumentation and exporters are effectively shut off.

---

### Alternative: Disable just the trace exporter

If you only want to disable the trace exporter (and not necessarily all telemetry, like metrics), you can set:

```bash
export OTEL_TRACES_EXPORTER=none
python your_app.py
```

Or in Python:

```python
import os

os.environ["OTEL_TRACES_EXPORTER"] = "none"
```

This tells OpenTelemetry not to export any trace data.

---

### Why `TELEMETRY_ENDPOINT` alone isn't enough

Setting `TELEMETRY_ENDPOINT` to an empty string may not affect OpenTelemetry defaults—because OpenTelemetry often uses its own environment variables (like `OTEL_EXPORTER_OTLP_ENDPOINT` or `OTEL_TRACES_EXPORTER`) rather than a generic `TELEMETRY_ENDPOINT`. If the application or library you're using is wired into OpenTelemetry, it's likely reading those OTel-specific variables (or using built-in defaults) instead of your custom `TELEMETRY_ENDPOINT`.

Hence, to fully prevent those `ConnectionRefusedError` messages, you'll want to either:

1. **Disable** OpenTelemetry with `OTEL_SDK_DISABLED=true`, or  
2. **Override** the exporter settings with `OTEL_TRACES_EXPORTER=none`.

Either approach will stop the SDK from making a connection to `localhost:4318`.


### Outcomes
- The mega service is running but not sending responses to the client.
- I still need to figure out how streaming works with the mega service and the ollama service may be try switching it off.
- I still need to figure out how to get the telemetry working.
- I think I'm close.


## Testing the Chat Service

A test script is provided in the `bin` directory to test the chat service. 

### Prerequisites

- Make sure the chat service is running on port 8888
- Install `curl` if not already available
- Install `jq` for JSON formatting (optional but recommended)

### Ollama Server Configuration

The chat service connects to an Ollama server for LLM inference. Here are important details about the configuration:

#### Port Configuration
- Ollama's default internal port is **11434**
- In the docker-compose.yaml file, this is mapped to port **9000** (external)
- The environment variable `LLM_SERVER_PORT` must match the internal port (11434)

### Docker Networking
The docker-compose.yaml file sets up a custom network called `opea-network` to ensure the containers can communicate with each other. The service references the Ollama server using its service name (`ollama-server`).

#### Troubleshooting Connection Issues

If you encounter connection errors like:
```
Cannot connect to host ollama-server:9000 ssl:default [Connect call failed ('172.18.0.2', 9000)]
```

Check these common issues:
1. Ensure the Ollama server is running (`docker ps`)
2. Verify the port mappings in docker-compose.yaml
3. Check that the environment variables for the chat service are correctly set
4. Ensure both services are on the same Docker network

For direct connection testing:
```bash
# Test connection from inside the chat service container
docker exec -it chatmegaservice curl -v ollama-server:11434
```

#### Disabling OpenTelemetry Errors

The docker-compose.yaml file includes the `OTEL_SDK_DISABLED=true` environment variable to prevent the OpenTelemetry errors seen in the logs.

### Environment Variables Set up

```sh
HOST_IP=$(curl -4 ifconfig.me)
echo "HOST_IP: $HOST_IP"
```

```sh
NO_PROXY=localhost
LLM_ENDPOINT_PORT=9000
LLM_SERVER_PORT=11434
LLM_MODEL_ID="llama3.2:3b"
LLM_MODEL="llama3.2:3b"
```

### Docker and docker compose

```sh
host_ip=$HOST_IP \
no_proxy=$NO_PROXY \
LLM_ENDPOINT_PORT=$LLM_ENDPOINT_PORT \
LLM_SERVER_PORT=$LLM_SERVER_PORT \
LLM_MODEL_ID=$LLM_MODEL_ID \
LLM_MODEL=$LLM_MODEL \
docker-compose up -d --build
```

### Download and pull the model

```sh
docker exec -it ollama-server ollama pull llama3.2:3b
```

### Running the Test

```bash
# Make the script executable (if needed)
chmod +x bin/test_chat.sh

# Run the test script
./bin/test_chat.sh
```


### Example cURL Command

If you prefer to test manually, you can use this cURL command:

```bash
curl -X POST "http://localhost:8888/v1/chatqna" \
  -H "Content-Type: application/json" \
  -d '{
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
    "max_tokens": 150
  }'
```

The chat service endpoint mimics the OpenAI API structure, accepting parameters like:
- `model`: The model name to use for generation
- `messages`: Array of message objects with `role` and `content`
- `temperature`: Controls randomness (higher = more random)
- `max_tokens`: Maximum number of tokens to generate

### Testing Ollama LLM Service directly

```sh
curl http://localhost:9000/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "What are LLMs, Agents and RAG?"}],
  "stream": false
}' | python -m json.tool
```
