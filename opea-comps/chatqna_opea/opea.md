# Getting Started with OPEA
In this document, we provide a tailored guide to deploying the ChatQnA application in OPEA GenAI Examples across multiple cloud platforms, including Amazon Web Services (AWS), Google Cloud Platform (GCP), IBM Cloud, Microsoft Azure and Oracle Cloud Infrastructure, enabling you to choose the best fit for your specific needs and requirements. For additional deployment targets, see the [ChatQnA](/tutorial/ChatQnA/ChatQnA_Guide.rst).

## Understanding OPEA's Core Components

Before moving forward, it's important to familiarize yourself with two key elements of OPEA: GenAIComps and GenAIExamples.

- GenAIComps is a collection of microservice components that form a service-based toolkit. This includes a variety of services such as llm (large language models), embedding, and reranking, among others.
- GenAIExamples provides practical and deployable solutions to help users implement these services effectively. Examples include ChatQnA and DocSum, which leverage the microservices for specific applications.


## Prerequisites

## Create and Configure a Virtual Server with AWS

**Step 1: Create Your Virtual Server**

1. Open the [AWS console](https://console.aws.amazon.com/console/home) and search for **EC2** in the search bar. 

2. Select **Launch instance** to start creating a virtual server.

3. Under **Name and tags**, name your virtual server in the **Name** field.

4. Under **Quick Start**, choose Ubuntu (`ami-id : ami-04dd23e62ed049936`) as the base OS.

5. In **Instance type**, select an instance for your Intel processor.

   >**Note**: We recommend `m7i.4xlarge` or larger instance for an Intel® 4th Gen Xeon© Scalable Processor. For more information on virtual servers on AWS, visit the [AWS and Intel page](https://aws.amazon.com/intel/).

6. Create a new key pair for SSH access by naming it, or select an existing key pair from the dropdown list.

7. Under **Network Settings**:

   -  Choose an existing security group, or
   -  Select **Create security group** and enable **Allow SSH traffic** and **Allow HTTP traffic**.

8. In **Storage**, set the size to 100 GiB.

9. Select **Launch instance** to launch your virtual server. A **Success** banner confirms the launch.

**Step 2: Connect and Configure Your Virtual Server**

1. Select **Connect**, and connect using your preferred connection method.

2. Search for **Security Groups** in the search bar and select the security group used when creating the instance.

3. Select **Edit inbound rules** on the right side of the window.

4. To add a rule, select **Add rule** and enter the following:

   -  Type: Custom TCP
   -  Port Range: 80
   -  Source: 0.0.0.0/0 

   >**Note**: To learn more, see [editing inbound or outbound rules](https://docs.aws.amazon.com/finspace/latest/userguide/step5-config-inbound-rule.html) from AWS documentation.

5. Select **Save rules** to commit your changes.


# Deploy the ChatQnA Solution
Use the command below to install docker:
```bash
wget https://raw.githubusercontent.com/opea-project/GenAIExamples/refs/heads/main/ChatQnA/docker_compose/install_docker.sh
chmod +x install_docker.sh
./install_docker.sh
```
Configure Docker to run as a non-root user by following these [instructions](https://docs.docker.com/engine/install/linux-postinstall/)

Clone the repo. It is recommended to checkout a specific release version (i.e. 1.0, 1.1, 1.2, etc):
```bash
export RELEASE_VERSION=<your-release-version>
git clone https://github.com/opea-project/GenAIExamples.git
cd GenAIExamples
git checkout tags/v${RELEASE_VERSION}
```

Set the required environment variables:
```bash
export host_ip="localhost"
export HUGGINGFACEHUB_API_TOKEN="Your_Huggingface_API_Token"
```

Set up proxies if you are behind a firewall:
```bash
export no_proxy=${your_no_proxy},$host_ip
export http_proxy=${your_http_proxy}
export https_proxy=${your_http_proxy}
```

Set up other specific use-case environment variables in `set_env.sh` before running it. For example, this is where you can change the model(s) to run with.
```bash
cd ChatQnA/docker_compose/intel/cpu/xeon/
source set_env.sh
```

Now we can start the services:
```bash
docker compose -f compose.yaml up -d
```
>**Note**: It takes a few minutes for the services to start. Check the logs for the services to ensure that ChatQnA is running before proceeding further.

For example to check the logs for the `vllm-service`:

```bash
docker logs vllm-service | grep Complete
```
Proceed further **only after** the output shows `Application startup complete.` as shown:
```bash
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

Run `docker ps -a` as an additional check to verify that all the services are running as shown. Notice the version of the docker images matches the RELEASE_VERSION you specified.

```bash
| CONTAINER ID | IMAGE                                                 | COMMAND                 | CREATED     | STATUS     | PORTS                                                                                 | NAMES                        |
|--------------|--------------------------------------------------------|------------------------|--------------|-------------|------------------------------------------------------------------------------------------|------------------------------|
| d992b34fda27 | opea/nginx:1.2                                         | "/docker-entrypoint.…" | 6 days ago | Up 6 days | 0.0.0.0:80->80/tcp, :::80->80/tcp                                                     | chatqna-xeon-nginx-server    |
| 2d297d595650 | opea/chatqna-ui:1.2                                    | "docker-entrypoint.s…" | 6 days ago | Up 6 days | 0.0.0.0:5173->5173/tcp, :::5173->5173/tcp                                             | chatqna-xeon-ui-server    |
| 0b9b2be1feef | opea/chatqna-without-rerank:1.2                        | "python chatqna.py -…" | 6 days ago | Up 6 days | 0.0.0.0:8888->8888/tcp, :::8888->8888/tcp                                             | chatqna-xeon-backend-server    |
| b64ba100723c | opea/dataprep:1.2                                      | "sh -c 'python $( [ …" | 6 days ago | Up 6 days | 0.0.0.0:6007->5000/tcp, [::]:6007->5000/tcp                                             | dataprep-redis-server    |
| a9b93207988d | opea/retriever:1.2                                     | "python opea_retriev…" | 6 days ago | Up 6 days | 0.0.0.0:7000->7000/tcp, :::7000->7000/tcp                                             | retriever-redis-server    |
| 4bf653d83cba | redis/redis-stack:7.2.0-v9                             | "/entrypoint.sh"       | 6 days ago | Up 6 days | 0.0.0.0:6379->6379/tcp, :::6379->6379/tcp, 0.0.0.0:8001->8001/tcp, :::8001->8001/tcp   | redis-vector-db    |
| b2774012be67 | ghcr.io/huggingface/text-embeddings-inference:cpu-1.5  | "text-embeddings-rou…" | 6 days ago | Up 6 days | 0.0.0.0:6006->80/tcp, [::]:6006->80/tcp                                             | tei-embedding-server    |
| 6407712b6f9b | opea/vllm:1.2                                          | "python3 -m vllm.ent…" | 6 days ago | Up 6 days | 0.0.0.0:9009->80/tcp, [::]:9009->80/tcp                                             | vllm-service    |
```

### Interact with ChatQnA

You can interact with ChatQnA via a browser interface:

* To view the ChatQnA interface, open a browser and navigate to the UI by inserting your public facing IP address in the following: `http://{public_ip}:80’.

>**Note:** For users running on ITAC, open a browser to localhost:80 if you are using port forwarding OR the virtual IP address of your load balancer.

We can go ahead and ask a sample question, say 'What is OPEA?'.

A snapshot of the interface looks as follows:

![Chat Interface](https://opea-project.github.io/latest/_images/chat_ui_response.png)

Given that any information about OPEA was not in the training data for the model, we see the model hallucinating and coming up with a response. We can upload a document (PDF) with information and observe how the response changes.

> **Note:** this example leverages the OPEA document for its RAG based content. You can download the [OPEA document](https://opea-project.github.io/latest/_downloads/41c91aec1d47f20ca22350daa8c2cadc/what_is_opea.pdf) and upload it using the UI.

![Chat Interface with RAG](https://opea-project.github.io/latest/_images/chat_ui_response_rag.png)