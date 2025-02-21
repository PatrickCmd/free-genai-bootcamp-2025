# OPEA Ollama
1. [opea.dev](https://opea.dev/)
2. [Opea Project](https://github.com/opea-project)
3. [Opea Comps](https://github.com/opea-project/GenAIComps)
4. [Opea Project Comps](https://opea-project.github.io/latest/GenAIComps/README.html)

## Setting Up Ollama locally
See APIs [here](../ollama-models/README.md)

### Getting the Host IP

Get your IP address

Here are a few simple commands to get your IP address on macOS terminal:

For your local IP address:
```bash
ipconfig getifaddr en0  # For WiFi
ipconfig getifaddr en1  # For Ethernet
```

For all network interfaces:
```bash
ifconfig
```

For just your public/external IP address:
```bash
curl ifconfig.me
```
or
```bash 
curl ipecho.net/plain
```

The first two options show your local network IP, while the curl commands show your public IP address that's visible to the internet. The `ifconfig` command gives you detailed information about all network interfaces.

```sh
HOST_IP=$(curl ifconfig.me)
echo "HOST_IP: $HOST_IP"
```

```sh
NO_PROXY=localhost
LLM_ENDPOINT_PORT=9000
LLM_MODEL_ID="llama3.2:3b"
```

```sh
host_ip=$HOST_IP no_proxy=$NO_PROXY LLM_MODEL_ID=$LLM_MODEL_ID docker-compose up -d
```

OR

```sh
host_ip=$HOST_IP no_proxy=$NO_PROXY LLM_ENDPOINT_PORT=$LLM_ENDPOINT_PORT LLM_MODEL_ID=$LLM_MODEL_ID docker-compose up -d
```

### Download/pull the model

```sh
curl http://localhost:8008/api/pull -d '{ "model": "llama3.2:3b" }'
```

or

```sh
docker exec -it ollama-server ollama pull llama3.2:3b
```

### List models

#### Request

```sh
curl http://localhost:8008/api/tags | python -m json.tool
```

#### Response

```json
{
    "models": [
        {
            "name": "llama3.2:3b",
            "model": "llama3.2:3b",
            "modified_at": "2025-02-20T12:36:19.297875645Z",
            "size": 2019393189,
            "digest": "a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72",
            "details": {
                "parent_model": "",
                "format": "gguf",
                "family": "llama",
                "families": [
                    "llama"
                ],
                "parameter_size": "3.2B",
                "quantization_level": "Q4_K_M"
            }
        }
    ]
}
```

OR


```sh
docker exec -it ollama-server ollama list
```

```
NAME           ID              SIZE      MODIFIED
llama3.2:3b    a80c4f17acd5    2.0 GB    About a minute ago
```


### Generate Response

```sh
curl -X POST http://localhost:8008/api/generate -H "Content-Type: application/json" -d '{"model": "llama3.2:3b", "prompt": "Why is the sky blue?"}'
```

Sample Response

```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 10706818083,
  "load_duration": 6338219291,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 130079000,
  "eval_count": 259,
  "eval_duration": 4232710000
}
```

#### Request (No streaming)
Request
A response can be received in one reply when streaming is off.

```sh
curl http://localhost:8008/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Why is the sky blue?",
  "stream": false
}' | python -m json.tool
```

#### Response

If stream is set to false, the response will be a single JSON object:

```json
{
  "model": "llama3.2",
  "created_at": "2023-08-04T19:22:45.499127Z",
  "response": "The sky is blue because it is the color of the sky.",
  "done": true,
  "context": [1, 2, 3],
  "total_duration": 5043500667,
  "load_duration": 5025959,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 325953000,
  "eval_count": 290,
  "eval_duration": 4709213000
}
```

### Generate a chat completion
#### No streaming

```sh
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "Why is the sky blue?"}],
  "stream": false
}' | python -m json.tool
```

#### Response

```json
{
    "model": "llama3.2:3b",
    "created_at": "2025-02-20T12:55:12.803987408Z",
    "message": {
        "role": "assistant",
        "content": "The sky appears blue because of a phenomenon called Rayleigh scattering, named after the British physicist Lord Rayleigh, who first described it in the late 19th century.\n\nHere's what happens:\n\n1. Sunlight enters Earth's atmosphere and encounters tiny molecules of gases such as nitrogen (N2) and oxygen (O2).\n2. These molecules scatter the light in all directions, but they scatter shorter (blue) wavelengths more than longer (red) wavelengths.\n3. This is because the smaller molecules are more effective at scattering the shorter wavelengths due to their smaller size and higher surface area.\n4. As a result, the blue light is scattered in all directions and reaches our eyes from all parts of the sky, making it appear blue.\n5. The red light, on the other hand, continues to travel in a straight line and doesn't get scattered as much, which is why we see it as less intense.\n\nDuring sunrise and sunset, the sky can take on hues of orange, pink, and red because the sunlight has to travel through more of Earth's atmosphere to reach our eyes, scattering off more molecules and particles. This scatters the shorter blue wavelengths even further, allowing the longer red wavelengths to dominate the scene.\n\nSo, in short, the sky appears blue because of Rayleigh scattering, which makes blue light more visible to us than other colors!"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 28842545447,
    "load_duration": 34789034,
    "prompt_eval_count": 31,
    "prompt_eval_duration": 335000000,
    "eval_count": 275,
    "eval_duration": 28470000000
}
```


```sh
curl http://localhost:8008/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [{"role": "user", "content": "What are LLMs, Agents and RAG?"}],
  "stream": false
}' | python -m json.tool
```

#### Response

```json
{
    "model": "llama3.2:3b",
    "created_at": "2025-02-20T16:05:24.324253789Z",
    "message": {
        "role": "assistant",
        "content": "LLMs (Large Language Models), Agents, and RAG are all related concepts in the field of Artificial Intelligence (AI) and Natural Language Processing (NLP). Here's a brief overview:\n\n1. **LLMs (Large Language Models)**: Large Language Models are a type of neural network designed to process and generate human-like language. They're trained on massive amounts of text data, which enables them to learn patterns and relationships in language. LLMs are typically used for tasks such as language translation, text summarization, sentiment analysis, and more.\n2. **Agents**: In the context of AI, an Agent is a software system that perceives its environment, takes actions, and learns from feedback. Agents can be used to control robots, drones, or other autonomous systems, or to interact with humans in various domains such as customer service, healthcare, or finance. The goal of an agent is to maximize some objective function, such as maximizing rewards or minimizing costs.\n3. **RAG (Reasoning and Abstraction Generator)**: RAG is a type of AI model that combines the strengths of Large Language Models with those of reasoning engines. It's designed to generate human-like explanations for complex concepts, rather than just producing text summaries or answers. RAGs use a combination of natural language processing (NLP) and symbolic reasoning to generate explanations that are both coherent and informative.\n\nIn summary:\n\n* LLMs are powerful NLP models for generating human-like language.\n* Agents are software systems that interact with their environment, learn from feedback, and optimize objectives.\n* RAGs combine the strengths of LLMs with those of reasoning engines to generate human-like explanations for complex concepts.\n\nThese three concepts are interconnected and are being explored in various AI applications."
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": 83143571850,
    "load_duration": 36057011197,
    "prompt_eval_count": 36,
    "prompt_eval_duration": 2376000000,
    "eval_count": 357,
    "eval_duration": 44701000000
}
```


### Testing the API with LangChain and OpenAI

```sh
python chatopenai_langchain_ollama.py
``` 
