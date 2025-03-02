import argparse
import json
import os
import re

from comps import ServiceOrchestrator, ServiceRoleType, ServiceType, MicroService, MegaServiceEndpoint
from comps.cores.mega.utils import handle_message
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest, 
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo,
)
from fastapi import Request
from comps.cores.proto.docarray import LLMParams
from fastapi.responses import StreamingResponse
from langchain_core.prompts import PromptTemplate

MEGA_SERVICE_PORT = int(os.getenv("MEGA_SERVICE_PORT", 8888))
LLM_SERVER_HOST_IP = os.getenv("LLM_SERVER_HOST_IP", "0.0.0.0")
LLM_SERVER_PORT = int(os.getenv("LLM_SERVER_PORT", 80))
LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")


class Chat:
    def __init__(self):
        print('init')

        self.megaservice = ServiceOrchestrator()
        self.endpoint = str(MegaServiceEndpoint.CHAT_QNA)
        self.host = '0.0.0.0'
        self.port = 8888
    
    def add_remote_services(self):
        print('add_remote_services')

        llm = MicroService(
            name="llm",
            host=LLM_SERVER_HOST_IP,
            port=LLM_SERVER_PORT,
            endpoint="/api/chat",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(llm)
        # self.megaservice.flow_to(llm)

    def start(self):
        print('start')
        print(f"endpoint: {self.endpoint}")
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

    async def handle_request(self, request: Request):
        print('handle_request')
        print(f"LLM_SERVER_HOST_IP: {LLM_SERVER_HOST_IP}")
        print(f"LLM_SERVER_PORT: {LLM_SERVER_PORT}")
        print(f"LLM_MODEL: {LLM_MODEL}")
        print(f"MEGA_SERVICE_PORT: {MEGA_SERVICE_PORT}")

        data = await request.json()
        stream_opt = data.get("stream", True)
        chat_request = ChatCompletionRequest.model_validate(data)
        print(f"chat_request: {chat_request}")

        prompt = handle_message(chat_request.messages)
        print(f"prompt: {prompt}")

        parameters = LLMParams(
            max_tokens=chat_request.max_tokens if chat_request.max_tokens else 1024,
            top_k=chat_request.top_k if chat_request.top_k else 10,
            top_p=chat_request.top_p if chat_request.top_p else 0.95,
            temperature=chat_request.temperature if chat_request.temperature else 0.01,
            frequency_penalty=chat_request.frequency_penalty if chat_request.frequency_penalty else 0.0,
            presence_penalty=chat_request.presence_penalty if chat_request.presence_penalty else 0.0,
            repetition_penalty=chat_request.repetition_penalty if chat_request.repetition_penalty else 1.03,
            stream=stream_opt,
            chat_template=chat_request.chat_template if chat_request.chat_template else None,
        )
        result_dict, runtime_graph = await self.megaservice.schedule(
            initial_inputs={"text": prompt},
            llm_parameters=parameters,
            # retriever_parameters=retriever_parameters,
        )
        print(f"parameters: {parameters}")
        print(f"result_dict: {result_dict}")
        print(f"runtime_graph: {runtime_graph}")

        choices = [ChatCompletionResponseChoice(
            index=0,
            message=ChatMessage(
                role="assistant",
                content="Hello, how are you?"
            ),
            finish_reason="stop",
        )]
        usage = UsageInfo()

        return ChatCompletionResponse(model="chatqna", choices=choices, usage=usage)


if __name__ == '__main__':
    print('main')
    chat = Chat()
    chat.add_remote_services()
    chat.start()