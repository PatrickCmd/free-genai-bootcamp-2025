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

These errors indicate that the OpenTelemetry exporter is attempting to send traces to `localhost:4318` but there’s nothing running on that port to receive them. If you want to *completely* disable telemetry (tracing) so that OpenTelemetry does not try to export anything, you can do so by disabling the OpenTelemetry SDK at runtime.

---

## Quick Fix: Disable the OTel SDK at startup

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

## Alternative: Disable just the trace exporter

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

## Why `TELEMETRY_ENDPOINT` alone isn’t enough

Setting `TELEMETRY_ENDPOINT` to an empty string may not affect OpenTelemetry defaults—because OpenTelemetry often uses its own environment variables (like `OTEL_EXPORTER_OTLP_ENDPOINT` or `OTEL_TRACES_EXPORTER`) rather than a generic `TELEMETRY_ENDPOINT`. If the application or library you’re using is wired into OpenTelemetry, it’s likely reading those OTel-specific variables (or using built-in defaults) instead of your custom `TELEMETRY_ENDPOINT`.

Hence, to fully prevent those `ConnectionRefusedError` messages, you’ll want to either:

1. **Disable** OpenTelemetry with `OTEL_SDK_DISABLED=true`, or  
2. **Override** the exporter settings with `OTEL_TRACES_EXPORTER=none`.

Either approach will stop the SDK from making a connection to `localhost:4318`.


## Outcomes
- The mega service is running but not sending responses to the client.
- I still need to figure out how streaming works with the mega service and the ollama service may be try switching it off.
- I still need to figure out how to get the telemetry working.
- I think I'm close.