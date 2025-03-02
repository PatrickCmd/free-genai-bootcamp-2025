variable "project_name" {
  description = "Name of the project, used for resource naming"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  type        = string
}

variable "subnet_id" {
  description = "ID of the subnet to launch the instance in"
  type        = string
}

variable "security_group_id" {
  description = "ID of the security group for the instance"
  type        = string
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key file"
  type        = string
}

variable "ssh_private_key_path" {
  description = "Path to the SSH private key file (for generating SSH config)"
  type        = string
}

variable "root_volume_size" {
  description = "Size of the root volume in GB"
  type        = number
}

variable "huggingface_token" {
  description = "Hugging Face API token for model access"
  type        = string
  sensitive   = true
}

variable "opea_release_version" {
  description = "OPEA release version to deploy"
  type        = string
}

variable "host_os" {
  description = "Operating system of the host machine (linux or windows)"
  type        = string
  default     = "linux"
}