# TTS microservice

## Provision the EC2 instance with terraform

The TTS microservice can be deployed on an AWS EC2 instance using Terraform. This automation simplifies the provisioning process and ensures consistent deployments.

### Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) (v1.0.0 or newer) installed
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured
- SSH keypair for accessing the EC2 instance
- Basic understanding of AWS and Terraform

### Configuration Steps

1. **Initialize Terraform in the project directory**

```bash
cd opea-comps/tts-microservice
terraform init
```

2. **Create your terraform.tfvars file**

Copy the example file to create your own variable file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Edit the `terraform.tfvars` file to customize your deployment:

```hcl
aws_region           = "us-east-1"        # Your preferred AWS region
instance_type        = "m7i.4xlarge"      # Recommended for speech models
ssh_public_key_path  = "~/.ssh/id_rsa.pub" # Path to your SSH public key
ssh_private_key_path = "~/.ssh/id_rsa"    # Path to your SSH private key
```

3. **Validate and plan the deployment**

```bash
terraform validate
terraform fmt -recursive
terraform plan
```

4. **Deploy the infrastructure**

```bash
terraform apply -auto-approve
```

After deployment completes, Terraform will output:
- The public IP address of your EC2 instance
- SSH connection command
- URL to access the TTS service

5. **SSH into the provisioned instance**

```bash
# Use the SSH command provided in the terraform output
ssh -i ~/.ssh/id_rsa ubuntu@<instance-ip>
```

### Infrastructure Details

The Terraform configuration creates:
- A VPC with public subnet
- Security group that allows SSH (port 22) and HTTP (port 80, 7055) access
- EC2 instance with Ubuntu and sufficient storage for the models
- SSH key pair automatically configured for access

### Cleanup Resources

When you're finished with the TTS microservice, you can destroy all created resources to avoid unnecessary AWS charges:

```bash
terraform destroy -auto-approve
```

## Setting Up the TTS Service

After provisioning the EC2 instance, you'll need to set up and configure the TTS service.

### SSH into the EC2 instance

Use SSH to connect to your newly provisioned EC2 instance. Replace the IP address with the one provided in your Terraform output:

```sh
ssh -i ~/.ssh/id_opea_docsum ubuntu@100.27.6.11
```

### Run the Speech T5 Server

Once connected to the instance, start the Speech T5 TTS server in the background:

```sh
# Start the TTS server in the background using nohup
nohup python3 speecht5_server.py --device=cpu &

# Test the server with a simple request
curl http://localhost:7055/v1/tts -XPOST -d '{"text": "Who are you?"}' -H 'Content-Type: application/json'
```

The `nohup` command allows the process to continue running even if you disconnect from the SSH session. The `--device=cpu` flag specifies to use CPU for inference instead of GPU.

### Retrieve Generated Audio Files

After generating audio files on the remote instance, you can copy them to your local machine for playback and analysis:

```sh
# Create a local directory for audio files if it doesn't exist
mkdir -p ./audio

# Copy MP3 file from the EC2 instance to your local machine
scp -i ~/.ssh/id_opea_docsum ubuntu@100.27.6.11:/home/ubuntu/speech.mp3 ./audio

# Copy WAV file from the EC2 instance to your local machine
scp -i ~/.ssh/id_opea_docsum ubuntu@100.27.6.11:/home/ubuntu/speech.wav ./audio
```

This allows you to retrieve both WAV (uncompressed) and MP3 (compressed) audio files for different use cases.

## Docker Deployment Options

The TTS service can also be deployed using Docker for easier management and portability.

### Build the Docker Image

Navigate to the repository root and build the TTS Docker image:

```sh
# Navigate to the repo root
cd ../../../

# Build the Docker image with proxy settings if needed
docker build -t opea/tts:latest --build-arg https_proxy=$https_proxy --build-arg http_proxy=$http_proxy -f comps/tts/src/Dockerfile .
```

### Run the TTS Service Container

Run the TTS service as a standalone Docker container:

```sh
# Get the current machine's IP address
ip_address=$(hostname -I | awk '{print $1}')

# Run the TTS service container
docker run -p 9088:9088 --ipc=host -e http_proxy=$http_proxy -e https_proxy=$https_proxy -e TTS_ENDPOINT=http://$ip_address:7055 opea/tts:latest
```

The `--ipc=host` flag is required for shared memory access, and `TTS_ENDPOINT` points to the Speech T5 server running on the host.

### Test the TTS Service API

Send a test request to the TTS service API to verify it's working correctly:

```sh
# Generate speech from text and save to a WAV file
curl http://localhost:9088/v1/audio/speech -XPOST -d '{"input":"Who are you?", "voice": "male"}' -H 'Content-Type: application/json' --output speech.wav
```

This will create a WAV file containing the synthesized speech in the current directory.

## Docker Compose Deployment

For more complex setups with multiple services, Docker Compose provides a better approach.

### Configure and Start the Services

```sh
# Choose which TTS backend to use
# For GPTSoVITS (recommended for better quality)
export TTS_ENDPOINT=http://$ip_address:9880

# For SpeechT5
# export TTS_ENDPOINT=http://$ip_address:7055

# Configure proxy settings if needed
export no_proxy=localhost,$no_proxy

# Start the TTS and GPTSoVITS services
docker compose -f ../deployment/docker_compose/compose.yaml up tts-gptsovits gptsovits-service -d
```

The `-d` flag runs the containers in detached mode (background).

### Testing the Composed Services

Send a more complex test to the TTS service deployed with Docker Compose:

```sh
# Generate speech from a longer text prompt
curl http://localhost:9088/v1/audio/speech -XPOST -d '{"input":"I am learning how to use the TTS service! I need to learn how to use the TTS service to generate speech from text."}' -H 'Content-Type: application/json' --output speech.wav
```

You can play the resulting WAV file with any audio player to hear the synthesized speech.

## Troubleshooting

- If you can't connect to the TTS service, check that the service is running and ports are open in your security group
- For audio quality issues, try switching between different TTS backends (SpeechT5 vs GPTSoVITS)
- If Docker containers fail to start, check the logs with `docker logs <container_id>`
