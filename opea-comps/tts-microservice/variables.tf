variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project, used for resource naming"
  type        = string
  default     = "opea-chatqna"
}

variable "vpc_cidr_block" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "m7i.4xlarge" # Recommended instance type for OPEA ChatQnA
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
  default     = "ami-04dd23e62ed049936" # Ubuntu as specified in OPEA docs
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_private_key_path" {
  description = "Path to the SSH private key file (for generating SSH config)"
  type        = string
  default     = "~/.ssh/id_rsa"
}

variable "root_volume_size" {
  description = "Size of the root volume in GB"
  type        = number
  default     = 100 # 100GB as specified in OPEA docs
}

variable "huggingface_token" {
  description = "Hugging Face API token for model access"
  type        = string
  sensitive   = true
}

variable "opea_release_version" {
  description = "OPEA release version to deploy"
  type        = string
  default     = "1.2" # Update with the latest version
} 