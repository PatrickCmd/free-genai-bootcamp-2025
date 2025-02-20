from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from openai import OpenAI

def openai_chat_completion(model_name: str, messages: list[dict]) -> str:
    client = OpenAI(
        api_key="ollama", 
        base_url="http://localhost:8008/v1",
    )
    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=messages
    )
    return response.choices[0].message.content

def ollama_chat_completion(model_name: str, messages: list[dict]) -> str:
    llm = ChatOllama(
        model=model_name,
        temperature=0,
        base_url="http://localhost:8008"
    )

    response = llm.invoke(messages)
    return response.content

def chat_openai_langchain_ollama(model_name: str, messages: list[dict]) -> str:
    # Instantiate llm
    llm = ChatOpenAI(
        temperature=0,
        model_name=model_name,
        api_key="ollama", 
        base_url="http://localhost:8008/v1",
    )
    
    # Invoke chain
    result = llm.invoke(messages)
    return result.content


def chat_openai_langchain_ollama_prompt_chaining(model_name: str) -> str:
    # Instantiate llm
    llm = ChatOpenAI(
        temperature=0,
        model_name=model_name,
        api_key="ollama", 
        base_url="http://localhost:8008/v1",
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that translates {input_language} to {output_language}.",
            ),
            ("human", "{input}"),
        ]
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "input_language": "English",
            "output_language": "Jamaican Patois",
            "input": "I love programming.",
        }
    )
    return result.content

if __name__ == "__main__":
    model_name = "llama3.2:3b"
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that translates English to Jamaican Patois. Translate the user sentence.",
        },
        {"role": "user", "content": "How is the day going? Will you be able to help me with my homework?"},
    ]
    ai_msg = openai_chat_completion(model_name, messages)
    print(f"OpenAI Assistant Response: {ai_msg}")

    ai_msg = openai_chat_completion(model_name, messages=[{"role": "user", "content": "What are LLMs, Agents and RAG?"}])
    print(f"OpenAI Assistant Response: {ai_msg}\n")


    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to Jamaican Patois. Translate the user sentence.",
        ),
        ("human", "How is the day going? Will you be able to help me with my homework?"),
    ]

    ai_msg = chat_openai_langchain_ollama(model_name, messages)
    print(f"ChatOpenAI LangChain Ollama Assistant Response: {ai_msg}\n")

    ai_msg = chat_openai_langchain_ollama_prompt_chaining(model_name)
    print(f"ChatOpenAI LangChain Ollama Prompt Chaining Assistant Response: {ai_msg}\n")

    ai_msg = ollama_chat_completion(model_name, messages)
    print(f"Ollama Assistant Response: {ai_msg}")

