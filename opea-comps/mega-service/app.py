from fastapi import HTTPException
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo
)
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps import MicroService, ServiceOrchestrator
import os

EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = os.getenv("EMBEDDING_SERVICE_PORT", 6000)
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = os.getenv("LLM_SERVICE_PORT", 9000)


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        print('hello')
        os.environ["TELEMETRY_ENDPOINT"] = ""
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        #embedding = MicroService(
        #    name="embedding",
        #    host=EMBEDDING_SERVICE_HOST_IP,
        #    port=EMBEDDING_SERVICE_PORT,
        #    endpoint="/v1/embeddings",
        #    use_remote_service=True,
        #    service_type=ServiceType.EMBEDDING,
        #)
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        #self.megaservice.add(embedding).add(llm)
        #self.megaservice.flow_to(embedding, llm)
        self.megaservice.add(llm)
    
    def start(self):

        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])

        self.service.start()
    
    async def handle_request(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        try:
            print(f"request messages: {request.messages}")
            # Format the request for Ollama
            ollama_request = {
                "model": request.model or "llama3.2:3b",  # or whatever default model you're using
                "messages": [
                    {
                        "role": "user",
                        "content": request.messages  # assuming messages is a string
                    }
                ],
                "stream": False  # disable streaming for now
            }
            
            # Schedule the request through the orchestrator
            result = await self.megaservice.schedule(ollama_request)
            
            # Extract the actual content from the response
            if isinstance(result, tuple) and len(result) > 0:
                print(f"result: {result}")
                llm_response = result[0].get("llm") or result[0].get('llm/MicroService')
                print(f"llm_response: {llm_response}")
               
                if hasattr(llm_response, 'body_iterator'):
                    # Read and process the response
                    response_body = b""
                    async for chunk in llm_response.body_iterator:
                        response_body += chunk
                    content = response_body.decode('utf-8')
                else:
                    content = "No response content available"
            else:
                content = "Invalid response format"

            # Create the response
            response = ChatCompletionResponse(
                model=request.model or "example-model",
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=ChatMessage(
                            role="assistant",
                            content=content
                        ),
                        finish_reason="stop"
                    )
                ],
                usage=UsageInfo(
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0
                )
            )
            
            return response
            
        except Exception as e:
            # Handle any errors
            raise HTTPException(status_code=500, detail=str(e))

example = ExampleService()
example.add_remote_service()
example.start()