#cloud-config
package_update: true
package_upgrade: true

packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg
  - lsb-release
  - git
  - wget

write_files:
  # Script to download and run the OPEA Docker installation script
  - path: /home/ubuntu/setup_docker.sh
    owner: ubuntu:ubuntu
    permissions: '0755'
    content: |
      #!/bin/bash
      cd /home/ubuntu
      wget https://raw.githubusercontent.com/opea-project/GenAIExamples/refs/heads/main/ChatQnA/docker_compose/install_docker.sh
      chmod +x install_docker.sh
      ./install_docker.sh
      
      # Configure Docker to run as a non-root user
      sudo usermod -aG docker ubuntu
  
  - path: /home/ubuntu/deploy_chatqna.sh
    owner: ubuntu:ubuntu
    permissions: '0755'
    content: |
      #!/bin/bash
      
      export RELEASE_VERSION=${opea_release_version}
      export host_ip="localhost"
      export HUGGINGFACEHUB_API_TOKEN="${huggingface_token}"

      # Clone the repository
      git clone https://github.com/opea-project/GenAIExamples.git
      cd GenAIExamples
      git checkout tags/v$${RELEASE_VERSION}

      # Navigate to the ChatQnA directory
      cd ChatQnA/docker_compose/intel/cpu/xeon/

      # Source the environment variables
      source set_env.sh

      # Start the services
      docker compose -f compose.yaml up -d

      # Wait for services to start
      echo "Waiting for services to start..."
      while ! docker logs vllm-service 2>&1 | grep -q "Application startup complete."; do
        sleep 10
        echo "Still waiting for vllm-service to start..."
      done

      echo "ChatQnA deployment complete! Access the application at http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):80"

runcmd:
  - chmod +x /home/ubuntu/setup_docker.sh
  - chmod +x /home/ubuntu/deploy_chatqna.sh
  - su - ubuntu -c "/home/ubuntu/setup_docker.sh"
  - su - ubuntu -c "/home/ubuntu/deploy_chatqna.sh"
  - echo "ChatQnA deployment initiated at $(date)" > /home/ubuntu/deployment_status.txt

final_message: "The system is finally up, after $UPTIME seconds" 