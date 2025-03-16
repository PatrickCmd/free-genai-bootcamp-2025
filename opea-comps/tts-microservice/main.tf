terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region  = var.aws_region
  profile = "sunbirdai"
}

module "network" {
  source = "./modules/network"

  project_name   = var.project_name
  vpc_cidr_block = var.vpc_cidr_block
  aws_region     = var.aws_region
}

module "ec2" {
  source = "./modules/ec2"

  project_name         = var.project_name
  instance_type        = var.instance_type
  ami_id               = var.ami_id
  subnet_id            = module.network.public_subnet_id
  security_group_id    = module.network.security_group_id
  ssh_public_key_path  = var.ssh_public_key_path
  ssh_private_key_path = var.ssh_private_key_path
  root_volume_size     = var.root_volume_size
  huggingface_token    = var.huggingface_token
  opea_release_version = var.opea_release_version
  host_os              = "linux"
}
